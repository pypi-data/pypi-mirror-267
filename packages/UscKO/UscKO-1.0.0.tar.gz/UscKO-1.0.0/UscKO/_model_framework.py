import torch

import torch.nn as nn
import torch.nn.functional as F

from torch.distributions import Distribution, constraints, Normal, Gamma, Poisson as PoissonTorch
from torch.distributions.utils import broadcast_all, logits_to_probs

import numpy as np

from typing import Optional, Union

#########################
# Learning Rate Scheduler
#########################
class LambdaLR2:
    def __init__(self, n_epochs, decay_start_epoch):
        assert (n_epochs - decay_start_epoch) > 0, "Decay must start before the training session ends!"
        self.n_epochs = n_epochs
        self.decay_start_epoch = decay_start_epoch
        
    def step(self, epoch):
        return 1.0 - max(0, epoch - self.decay_start_epoch) / (self.n_epochs - self.decay_start_epoch)

#########################
# FC Block
#########################
class FC_Block(nn.Module):
    def __init__(self, feature, Dropout=0.2):
        super(FC_Block, self).__init__()
        
        layers = []
        
        layers += [
                nn.Linear(feature, feature),
                nn.LayerNorm(feature),
                nn.LeakyReLU(0.2),
                nn.Dropout(Dropout),
            ]
        
        self.model_blocks = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = self.model_blocks(x)
        return x

######################
# shared_block E
######################
class SharedLayers_E(nn.Module):
    def __init__(self, n_shared_block=1, features=None, Dropout=0.2):
        super(SharedLayers_E, self).__init__()
        
        layers = []
        
        for _ in range(n_shared_block):
            layers += [
                FC_Block(feature=features, Dropout=Dropout)
            ]

        self.Shared = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = x.float()
        x = self.Shared(x)
        return x

######################
# shared_block G
######################
class SharedLayers_G(nn.Module):
    def __init__(self, n_shared_block=1, features=None, n_latent=None):
        super(SharedLayers_G, self).__init__()
        
        layers = []
        
        layers += [
            nn.Linear(n_latent, features)
        ]
        
        for _ in range(n_shared_block):
            layers += [
                nn.Linear(features, features),
                nn.LayerNorm(features),
            ]

        self.Shared = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = x.float()
        x = self.Shared(x)
        return x
    
######################
# shared_block G_mu G_theta G_dropout
######################
class SharedLayers_G_mu(nn.Module):
    def __init__(self, n_shared_block=1, features=None):
        super(SharedLayers_G_mu, self).__init__()
        
        layers = []
        for _ in range(n_shared_block):
            layers += [
                nn.Linear(features, features),
            ]

        self.Shared = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = x.float()
        x = self.Shared(x)
        return x

class SharedLayers_G_theta(nn.Module):
    def __init__(self, n_shared_block=1, features=None):
        super(SharedLayers_G_theta, self).__init__()
        
        layers = []
        for _ in range(n_shared_block):
            layers += [
                nn.Linear(features, features),
            ]

        self.Shared = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = x.float()
        x = self.Shared(x)
        return x

class SharedLayers_G_dropout(nn.Module):
    def __init__(self, n_shared_block=1, features=None):
        super(SharedLayers_G_dropout, self).__init__()
        
        layers = []
        for _ in range(n_shared_block):
            layers += [
                nn.Linear(features, features),
            ]

        self.Shared = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = x.float()
        x = self.Shared(x)
        return x

#########################
# Encoder
#########################
def _identity(x):
    return x

class Encoder(nn.Module):
    def __init__(self, 
                 data_size, 
                 n_hidden=256, 
                 n_latent=50,
                 n_layers=5, 
                 shared_block=None, 
                 Dropout=0.2
                ):
        super(Encoder, self).__init__()

        # MLP
        layers = []  
        
        layers += [
            nn.Linear(data_size, n_hidden),
        ]
        
        for _ in range(n_layers - 1):
            layers += [
                FC_Block(feature=n_hidden, Dropout=Dropout)
            ]
        
        layers += [
            nn.Linear(n_hidden, n_hidden),
        ]
        
        self.model_blocks = nn.Sequential(*layers).float()
        self.shared_block = shared_block
        
        # reparameterization
        self.mean = nn.Linear(n_hidden, n_latent)
        self.var = nn.Linear(n_hidden, n_latent)
        self.z_transformation = _identity
        
        self.var_activation = torch.exp

    def reparameterization(self, m, var):
        Tensor = torch.cuda.FloatTensor if m.is_cuda else torch.FloatTensor 
        dist = Normal(m, var.sqrt())
        z = self.z_transformation(dist.rsample())
        return z
    
    def forward(self, x):
        x = x.float()
        x = self.model_blocks(x)
        x = self.shared_block(x)
        z_m = self.mean(x)
        z_var = self.var_activation(self.var(x))
        # reparameterization
        dist = Normal(z_m, z_var.sqrt())
        z = self.reparameterization(z_m, z_var)
        return dist, z_m, z_var, z

#########################
# Generator
#########################
class ZINB(Distribution):
    
    arg_constraints = {
        "mu": constraints.greater_than_eq(0),
        "theta": constraints.greater_than_eq(0),
        "zi_logits": constraints.real,
        "scale": constraints.greater_than_eq(0),
    }
    support = constraints.nonnegative_integer

    def __init__(
        self,
        mu: Optional[torch.Tensor] = None,
        theta: Optional[torch.Tensor] = None,
        zi_logits: Optional[torch.Tensor] = None,
        scale: Optional[torch.Tensor] = None,
        validate_args=False,
    ):
        self.mu = mu
        self.theta = theta
        self.zi_logits = zi_logits
        self.validate_args = validate_args
        self.scale = scale
        self.eps=1e-8
        super().__init__()
        
        self.zi_logits, self.mu, self.theta = broadcast_all(self.zi_logits, self.mu, self.theta)
    
    @staticmethod
    def _gamma(theta, mu):
        concentration = theta
        rate = theta / mu
        # Important remark: Gamma is parametrized by the rate = 1/scale!
        gamma_d = Gamma(concentration=concentration, rate=rate)
        return gamma_d
    
    def zi_probs(self) -> torch.Tensor:
        return logits_to_probs(self.zi_logits, is_binary=True)
    
    def log_prob(self, value: torch.Tensor) -> torch.Tensor:
        """Log probability."""
        return self.log_zinb_positive(value, self.mu, self.theta, self.zi_logits, self.eps)
    
    def log_zinb_positive(self, x: torch.Tensor,mu: torch.Tensor, theta: torch.Tensor, pi: torch.Tensor,eps=1e-8):
        if self.theta.ndimension() == 1:
            theta = self.theta.view(1, self.theta.size(0))

        # Uses log(sigmoid(x)) = -softplus(-x)
        softplus_pi = F.softplus(-self.zi_logits)
        log_theta_eps = torch.log(theta + eps)
        log_theta_mu_eps = torch.log(theta + self.mu + eps)
        pi_theta_log = -self.zi_logits + theta * (log_theta_eps - log_theta_mu_eps)

        case_zero = F.softplus(pi_theta_log) - softplus_pi
        mul_case_zero = torch.mul((x < eps).type(torch.float32), case_zero)

        case_non_zero = (
            -softplus_pi
            + pi_theta_log
            + x * (torch.log(self.mu + eps) - log_theta_mu_eps)
            + torch.lgamma(x + theta)
            - torch.lgamma(theta)
            - torch.lgamma(x + 1)
        )
        mul_case_non_zero = torch.mul((x > eps).type(torch.float32), case_non_zero)

        res = mul_case_zero + mul_case_non_zero
        return res
    
    def Rsample(
        self,
        sample_shape: Optional[Union[torch.Size, tuple]] = None,
    ) -> torch.Tensor:
        """Sample from the distribution."""
        sample_shape = sample_shape or torch.Size()
        with torch.no_grad():
            gamma_d = self._gamma(self.theta, self.mu)
            
            p_means = gamma_d.sample(sample_shape)
            nan_mask = torch.isnan(p_means)
            p_means = torch.where(nan_mask, torch.zeros_like(p_means), p_means)

            l_train = torch.clamp(p_means, max=1e8, min=0)
            counts = PoissonTorch(l_train).sample()
            is_zero = torch.rand_like(counts) <= self.zi_probs()
            samp = torch.where(is_zero, torch.zeros_like(counts), counts)
            
        return samp


class Decoder_G(nn.Module):
    def __init__(
        self,
        data_size=None,
        n_hidden = 256,
        n_latent=50,
        #n_layers=4,
        shared_block=None,
        shared_block_mu=None,
        shared_block_theta=None,
        shared_block_dropout=None,
        Dropout=0
    ):
        super().__init__()
        
        #self.data_size = data_size
        #self.n_latent = n_latent
        self.shared_block = shared_block
        self.shared_mu = shared_block_mu
        self.shared_theta = shared_block_theta
        self.shared_dropout = shared_block_dropout

        # mean gamma
        self.px_scale_decoder = nn.Sequential(
            nn.Linear(n_hidden, data_size),
            nn.Softmax(dim=1), # or dim=-1
        )

        self.px_r_decoder = nn.Sequential(
            nn.Linear(n_hidden, data_size),
            nn.Softplus(),
        )

        # dropout
        self.px_dropout_decoder = nn.Sequential(
            nn.Linear(n_hidden, 3 * n_hidden),
            nn.Linear(3 * n_hidden, data_size)
        )
        
    def forward(
        self,
        z: torch.Tensor,
        x: torch.Tensor # adata.X
    ): 
        library = torch.log(x.sum(1)).unsqueeze(1)
        px = self.shared_block(z)

        px_scale = self.shared_mu(px)
        px_scale = self.px_scale_decoder(px_scale)
        
        px_dropout = self.shared_dropout(px)
        px_dropout = self.px_dropout_decoder(px_dropout)
        
        px_rate = torch.exp(library) * px_scale
        
        px_r = self.shared_theta(px)
        px_r = self.px_r_decoder(px_r)
        
        return px_scale, px_r, px_rate, px_dropout
    

class Generator(nn.Module):
    def __init__(self, 
                 n_hidden=256, 
                 n_latent=50,
                 #n_layers=4, 
                 shared_block=None, 
                 shared_block_mu=None,
                 shared_block_theta=None,
                 shared_block_dropout=None,
                 data_size=None, 
                 Dropout=0.2, 
                ):
        super(Generator, self).__init__()
        
        self.shared_block = shared_block
        self.shared_block_mu = shared_block_mu
        self.shared_block_theta = shared_block_theta
        self.shared_block_dropout = shared_block_dropout
        
        self.n_latent = n_latent
        self.data_size = data_size
        self.n_hidden = n_hidden
        #self.n_layers = n_layers
        
        self.Decoder_G = Decoder_G(data_size=self.data_size, 
                                   n_hidden=self.n_hidden,
                                   n_latent=self.n_latent, 
                                   #n_layers=self.n_layers,
                                   shared_block=self.shared_block,
                                   shared_block_mu=self.shared_block_mu,
                                   shared_block_theta=self.shared_block_theta,
                                   shared_block_dropout=self.shared_block_dropout,
                                   Dropout=0)

    def forward(self, z, x):
        pz = Normal(torch.zeros_like(z), torch.ones_like(z))
        
        px_scale, px_r, px_rate, px_dropout = self.Decoder_G(z, x)
        
        px_r = torch.exp(px_r)
        px = ZINB(mu=px_rate, 
                  theta=px_r, 
                  zi_logits=px_dropout, 
                  scale=px_scale)
        
        px_log_prob = px.log_prob(x)
        
        px_sample = px.Rsample(
            sample_shape=None,
        )
        return pz, px, px_sample, px_log_prob

#########################
# Discriminator
#########################
class Discriminator(nn.Module):
    def __init__(self, 
                 data_size=None, 
                 n_hidden=256, 
                 n_latent=50, 
                 n_layers_D=3, 
                 Dropout=0.2):
        super(Discriminator, self).__init__()
        
        self.shape2 = n_latent # for valid_1, valid_2, fake_1 and fake_2
        
        layers = []
        
        layers += [nn.Linear(data_size, n_hidden)]
        
        for _ in range(n_layers_D - 1):
            layers += [
                FC_Block(feature=n_hidden, Dropout=Dropout)
            ]
        
        layers += [nn.Linear(n_hidden, n_latent)]
        
        self.model_blocks = nn.Sequential(*layers)
        
    def forward(self, x):
        x = x.float()
        out = self.model_blocks(x)
        return out.float()