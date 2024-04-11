import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import itertools
import datetime
import time
import sys
from sklearn.model_selection import train_test_split


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.optim.lr_scheduler import LambdaLR
from torch.distributions import Normal
from torch.distributions import kl_divergence as kl

import numpy as np
import random
from lightning.pytorch import seed_everything

from ._model_framework import *

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True

class UNST(nn.Module):
    def __init__(self, adata = None, task_name=None, conditionA=None, conditionB=None,
                 n_epochs=100, decay_start_epoch = 20, 
                 n_hidden=256, 
                 n_latent=50,
                 n_layers=5, n_shared_block=1, n_layers_D=3,
                 all_lambda=[10, 0.1, 100, 0.1, 100, 0.001], 
                 lr=0.0002,
                 beta=[0.5,0.999], 
                 batch_size=1,
                 val_rate=0.1,
                 Dropout=0.2,
                ):
        super(UNST, self).__init__()
        """
        UscKO: Unsupervised Single Cell RNA-seq virtual perturbation KnockOut tools. UscKO is an unsupervised virtual perturbation and knockout tool for scRNA-seq, which can be used for style transfer and simulating gene KO experiments on scRNA-seq data.
        
        Unsupervised scRNA-seq Style Transfer Trainer(UNST)
        
        Arguments:
        - adata (AnnData, required): An AnnData object generated form 'Preparation'. 
        - task_name (str, required): Name of the training task and the saved weights.
        - conditionA (str, required): The original condition of scRNA-seq. Specified as the condition in 'adata.obs['Condition']'.
        - conditionB (str, required): The target condition of scRNA-seq. Specified as the condition in 'adata.obs['Condition']'.
        - n_epochs (int, required): Number of training epochs. Default is 100.
        - decay_start_epoch (int, required): Epoch from which to start learning rate decay. Default is 20.
        - n_hidden (int, required): Number of nodes per hidden layer in the neural networks. Default is 256.
        - n_latent (int, required): Dimensionality of the latent space. Default is 50.
        - n_layers (int, required): Number of hidden layers used for the encoder neural networks. Default is 5.
        - n_shared_block (int, required): Number of shared layers used for encoder and decoder neural networks. Default is 1.
        - n_layers_D (int, required): Number of hidden layers used for discriminator neural networks. Default is 4.
        - all_lambda (list, required): Loss weights for different components. Default is [10, 0.1, 100, 0.1, 100, 0.001].
        - lr (float, required): Learning rate for the Adam optimizer. Default is 0.00002.
        - beta (list, required): Decay rates of first and second order momentum of gradients for the Adam optimizer. Default is [0.5, 0.999].
        - batch_size (int, required): Batch size for training. Default is 1.
        - val_rate (float, optional):Proportion of cells in the training set used as the validation set, ranging from 0 to 1. Default is 0.1.
        - Dropout (float, optional): Dropout rate for neural networks, ranging from 0 to 1. Default is 0.2.
        """
        #########################
        # Device detected
        #########################
        if torch.cuda.is_available():
            print("CUDA device detected. Using GPU for computations.")
        else:
            print("Warning: No CUDA device detected. Using CPU for computations.")
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        #################################
        # Create checkpoint directories
        #################################
        self.task_name = task_name
        if self.task_name is None:
            raise ValueError("Task name must be provided")

        self.save_models_dir = "./saved_models/%s/" % self.task_name
        os.makedirs(self.save_models_dir, exist_ok=True)
        
        self.save_models_dir = self.save_models_dir
        
        #########################
        # LOSSES
        #########################
        self.criterion_GAN = torch.nn.MSELoss()
        self.criterion_VAE = torch.nn.L1Loss()
        
        # base settings
        self.adata = adata.adata_Train
        self.data_size = self.adata.X.shape[1]
        self.n_epochs = n_epochs
        self.decay_start_epoch = decay_start_epoch
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.n_latent = n_latent
        self.n_layers_D = n_layers_D
        self.conditionA = conditionA
        self.conditionB = conditionB
        self.batch_size = batch_size
        self.val_rate = val_rate
        self.Test_loss = float('inf')
        self.n_shared_block= n_shared_block
        self.Dropout = Dropout
        
        if self.conditionA not in self.adata.obs['Condition'].values or self.conditionB not in self.adata.obs['Condition'].values:
            raise ValueError(f"'conditionA or conditionB is not in the {self.adata.obs['Condition']}.")
        
        
        seed = 666
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        
        
        # Initialize generator and discriminator
        self.shared_E = SharedLayers_E(features=self.n_hidden, 
                                       Dropout=self.Dropout, 
                                       n_shared_block=self.n_shared_block)
        
        self.shared_G = SharedLayers_G(features=self.n_hidden, 
                                       n_latent=self.n_latent, 
                                       n_shared_block=self.n_shared_block)
        
        self.shared_block_mu = SharedLayers_G_mu(features=self.n_hidden, 
                                              n_shared_block=self.n_shared_block)
        self.shared_block_theta = SharedLayers_G_theta(features=self.n_hidden,
                                                       n_shared_block=self.n_shared_block)
        self.shared_block_dropout = SharedLayers_G_dropout(features=self.n_hidden,
                                                      n_shared_block=self.n_shared_block)
        
        self.E1 = Encoder(data_size=self.data_size, 
                          n_hidden=self.n_hidden, 
                          n_latent=self.n_latent, 
                          n_layers=self.n_layers,
                          shared_block=self.shared_E,
                          Dropout=self.Dropout)
        
        self.E2 = Encoder(data_size=self.data_size, 
                          n_hidden=self.n_hidden, 
                          n_latent=self.n_latent, 
                          n_layers=self.n_layers,
                          shared_block=self.shared_E,
                          Dropout=self.Dropout)
        
        self.G1 = Generator(n_latent=self.n_latent, 
                            n_hidden=self.n_hidden, 
                            data_size=self.data_size,
                            shared_block=self.shared_G,
                            shared_block_mu=self.shared_block_mu,
                            shared_block_theta=self.shared_block_theta,
                            shared_block_dropout=self.shared_block_dropout, 
                            Dropout=self.Dropout)
        
        
        self.G2 = Generator(n_latent=self.n_latent, 
                            n_hidden=self.n_hidden, 
                            data_size=self.data_size,
                            shared_block=self.shared_G,
                            shared_block_mu=self.shared_block_mu,
                            shared_block_theta=self.shared_block_theta,
                            shared_block_dropout=self.shared_block_dropout, 
                            Dropout=self.Dropout)
        
        
        self.D1 = Discriminator(data_size=self.data_size, 
                                n_hidden=self.n_hidden,
                                n_latent=self.n_latent,
                                n_layers_D=self.n_layers_D,
                                Dropout=self.Dropout)
        
        
        self.D2 = Discriminator(data_size=self.data_size, 
                                n_hidden=self.n_hidden,
                                n_latent=self.n_latent,
                                n_layers_D=self.n_layers_D,
                                Dropout=self.Dropout)
        
        # device to cuda or cpu
        self.E1.to(self.device)
        self.E2.to(self.device)
        self.G1.to(self.device)
        self.G2.to(self.device)
        self.D1.to(self.device)
        self.D2.to(self.device)
        self.criterion_GAN.to(self.device)
        self.criterion_VAE.to(self.device)
        
        # Loss weights lambda
        self.all_lambda = all_lambda
        self.lambda_0 = self.all_lambda[0] # GAN
        self.lambda_1 = self.all_lambda[1] # KL (encoded scrna-seq)
        self.lambda_2 = self.all_lambda[2] # recon
        self.lambda_3 = self.all_lambda[3] # KL (encoded translated scrna-seq)
        self.lambda_4 = self.all_lambda[4] # Cycle
        self.lambda_5 = self.all_lambda[5] # NLL for ZINB
        
        # Optimizers
        self.lr = lr
        self.b1 = beta[0]
        self.b2 = beta[1]
        
        
        self.optimizer_G = torch.optim.Adam(
            itertools.chain(self.E1.parameters(), self.E2.parameters(), self.G1.parameters(), self.G2.parameters()),
            lr=self.lr,
            betas=(self.b1,self.b2),
        )
        self.optimizer_D1 = torch.optim.Adam(self.D1.parameters(), lr=self.lr, betas=(self.b1, self.b2))
        self.optimizer_D2 = torch.optim.Adam(self.D2.parameters(), lr=self.lr, betas=(self.b1, self.b2))
        
        # Learning rate update schedulers
        self.lr_scheduler_G = LambdaLR(
            self.optimizer_G, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step
        )
        
        
        # Learning rate update schedulers
        self.lr_scheduler_G = LambdaLR(
            self.optimizer_G, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step
        )

        self.lr_scheduler_D1 = LambdaLR(
            self.optimizer_D1, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step
        )
        
        self.lr_scheduler_D2 = LambdaLR(
            self.optimizer_D2, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step
        )
        
        # scRNA-seq data processing
        self.scRNA_1 = self.adata[(self.adata.obs["Condition"] == self.conditionA)]
        self.scRNA_2 = self.adata[(self.adata.obs["Condition"] == self.conditionB)]
        
        self.scRNA_1, self.scRNA_1_test= train_test_split(self.scRNA_1, test_size=self.val_rate)
        self.scRNA_2, self.scRNA_2_test= train_test_split(self.scRNA_2, test_size=self.val_rate)
        
        self.scRNA_1.X = self.scRNA_1.X.toarray()
        self.scRNA_2.X = self.scRNA_2.X.toarray()
        self.scRNA_1_test.X = self.scRNA_1_test.X.toarray()
        self.scRNA_2_test.X = self.scRNA_2_test.X.toarray()
    
        self.num_cells_1 = self.scRNA_1.X.shape[0]
        self.num_cells_2 = self.scRNA_2.X.shape[0]
        
        del self.adata
        
        # Create Data_Loader
        self.data_loader = self.create_data_loader()
        self.test_data_loader = self.create_test_data_loader()

    #########################
    # Save model weight 
    #########################
    def save_model_weight(self, save_models_dir, epoch):
        
        save_path = os.path.join(self.save_models_dir, f"{self.task_name}_Best_Weights.pth")
        
        epochs = epoch
        torch.save({
            'E1_state_dict': self.E1.state_dict(),
            'E2_state_dict': self.E2.state_dict(),
            'G1_state_dict': self.G1.state_dict(),
            'G2_state_dict': self.G2.state_dict()
        }, save_path)
        print(f"Model saved at {save_models_dir} for epoch {epochs}\n")
    
    
    #########################
    # Data Loader for Training
    #########################
    def create_data_loader(self):
        class MyDataset(Dataset):
            def __init__(self, scRNA_1, scRNA_2):
                self.scRNA_1 = scRNA_1.X.toarray()
                self.scRNA_2 = scRNA_2.X.toarray()
                self.num_cells_1 = self.scRNA_1.shape[0]
                self.num_cells_2 = self.scRNA_2.shape[0]
                self.max_cells = max(self.num_cells_1, self.num_cells_2)
                self.shuffle_indices()
            
            def shuffle_indices(self):
                self.indices_A = list(range(self.num_cells_1))
                self.indices_B = list(range(self.num_cells_2))
                random.shuffle(self.indices_A)
                random.shuffle(self.indices_B)
                
            def __len__(self):
                return self.max_cells
            
            def __getitem__(self, idx):
                idx_A = self.indices_A[idx % self.num_cells_1]
                idx_B = self.indices_B[idx % self.num_cells_2]
                X1 = self.scRNA_1[idx_A]
                X2 = self.scRNA_2[idx_B]
                return X1, X2
        
        my_dataset = MyDataset(self.scRNA_1, self.scRNA_2)
        
        data_loader = DataLoader(my_dataset, batch_size=self.batch_size, shuffle=True, drop_last=True)
        self.data_loader = data_loader
        del self.scRNA_1, self.scRNA_2
        return data_loader
    
    #########################
    # Data Loader for Testing
    #########################
    def create_test_data_loader(self):
        class MyDataset(Dataset):
            def __init__(self, scRNA_1_test, scRNA_2_test):
                self.scRNA_1_test = scRNA_1_test.X.toarray()
                self.scRNA_2_test = scRNA_2_test.X.toarray()
                self.num_cells_1 = self.scRNA_1_test.shape[0]
                self.num_cells_2 = self.scRNA_2_test.shape[0]
                self.max_cells = max(self.num_cells_1, self.num_cells_2)
                self.shuffle_indices()
            
            def shuffle_indices(self):
                self.indices_A = list(range(self.num_cells_1))
                self.indices_B = list(range(self.num_cells_2))
                random.shuffle(self.indices_A)
                random.shuffle(self.indices_B)
                
            def __len__(self):
                return self.max_cells
            
            def __getitem__(self, idx):
                idx_A = self.indices_A[idx % self.num_cells_1]
                idx_B = self.indices_B[idx % self.num_cells_2]
                X1 = self.scRNA_1_test[idx_A]
                X2 = self.scRNA_2_test[idx_B]
                return X1, X2
        my_dataset = MyDataset(self.scRNA_1_test, self.scRNA_2_test)
        
        test_data_loader = DataLoader(my_dataset, batch_size=self.batch_size, shuffle=False, drop_last=True)
        self.test_data_loader = test_data_loader
        del self.scRNA_1_test, self.scRNA_2_test
        return test_data_loader
        
    #########################
    # Test evaluation
    #########################
    def Test(self):
        self.E1.eval()
        self.E2.eval()
        self.G1.eval()
        self.G2.eval()
        
        with torch.no_grad():
            total_loss_G = 0.0
            num_batches = 0
            
            for i,batch in enumerate(self.test_data_loader):
                self.X1, self.X2 = batch

                self.X1 = self.X1.to(self.device)
                self.X2 = self.X2.to(self.device)
                
                self.valid_1 = torch.ones((self.X1.size(0), self.D1.shape2))
                self.fake_1 = torch.zeros((self.X1.size(0), self.D1.shape2))
                
                self.valid_2 = torch.ones((self.X2.size(0), self.D2.shape2))
                self.fake_2 = torch.zeros((self.X2.size(0), self.D2.shape2))
                
                self.valid_1 = self.valid_1.to(self.device)
                self.valid_2 = self.valid_2.to(self.device)
                self.fake_1 = self.fake_1.to(self.device)
                self.fake_2 = self.fake_2.to(self.device)
                
                
                #########################
                #  Train E and G
                #########################
                self.optimizer_G.zero_grad()
                
                # Get shared latent representation
                self.qz1, _, _, self.Z1 = self.E1(self.X1)
                self.qz2, _, _, self.Z2 = self.E2(self.X2)
                
                # Reconstruct scRNA-seq
                self.recon_pz1, _, self.recon_X1, self.recon_X1_log_prob = self.G1(self.Z1, self.X1)
                self.recon_pz2, _, self.recon_X2, self.recon_X2_log_prob = self.G2(self.Z2, self.X2)

                # Translate scRNA-seq
                self.fake_pz1, _, self.fake_X1, self.fake_X1_log_prob = self.G1(self.Z2, self.X2)
                self.fake_pz2, _, self.fake_X2, self.fake_X2_log_prob = self.G2(self.Z1, self.X1)
                
                # Cycle translation
                self.qz1_, _, _, self.Z1_ = self.E1(self.fake_X1)
                self.qz2_, _, _, self.Z2_ = self.E2(self.fake_X2)
                
                self.cycle_pz1, self.cycle_X1_px, self.cycle_X1, self.cycle_X1_log_prob = self.G1(self.Z2_, self.X1)
                self.cycle_pz2, self.cycle_X2_px, self.cycle_X2, self.cycle_X1_log_prob = self.G2(self.Z1_, self.X2)
                
                
                self.Z1 = self.Z1.to(self.device)
                self.Z2 = self.Z2.to(self.device)
                
                self.recon_X1 = self.recon_X1.to(self.device)
                self.recon_X2 = self.recon_X2.to(self.device)
                
                self.fake_X1 = self.fake_X1.to(self.device)
                self.fake_X2 = self.fake_X2.to(self.device)
                
                self.Z1_ = self.Z1_.to(self.device)
                self.Z2_ = self.Z2_.to(self.device)
                
                self.cycle_X1 = self.cycle_X1.to(self.device)
                self.cycle_X2 = self.cycle_X2.to(self.device)
                

                # Losses
                self.loss_GAN_1 = self.lambda_0 * self.criterion_GAN(self.D1(self.fake_X1), self.valid_1)
                self.loss_GAN_2 = self.lambda_0 * self.criterion_GAN(self.D2(self.fake_X2), self.valid_2)
                
                self.loss_KL_1 = self.lambda_1 * kl(self.qz1, self.recon_pz1).sum(dim=1).mean(dim=0)
                self.loss_KL_2 = self.lambda_1 * kl(self.qz2, self.recon_pz2).sum(dim=1).mean(dim=0)

                self.loss_recon_1 = self.lambda_2 * self.criterion_VAE(self.recon_X1, self.X1)
                self.loss_recon_2 = self.lambda_2 * self.criterion_VAE(self.recon_X2, self.X2)
                
                self.loss_KL_1_ = self.lambda_3 * kl(self.qz1_, self.cycle_pz1).sum(dim=1).mean(dim=0)
                self.loss_KL_2_ = self.lambda_3 * kl(self.qz2_, self.cycle_pz2).sum(dim=1).mean(dim=0)
                
                self.loss_cyc_1 = self.lambda_4 * self.criterion_VAE(self.cycle_X1, self.X1)
                self.loss_cyc_2 = self.lambda_4 * self.criterion_VAE(self.cycle_X2, self.X2)
                
                # NNL for ZINB
                self.loss_recon_X1_log_prob = self.lambda_5 * -self.recon_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_recon_X2_log_prob = self.lambda_5 * -self.recon_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X1_log_prob = self.lambda_5 * -self.fake_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X2_log_prob = self.lambda_5 * -self.fake_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X1_log_prob = self.lambda_5 * -self.cycle_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X2_log_prob = self.lambda_5 * -self.cycle_X2_log_prob.sum(dim=1).mean(dim=0)
                
                
                # Total loss
                self.loss_G = (
                    self.loss_GAN_1 + self.loss_GAN_2
                    + self.loss_KL_1 + self.loss_KL_2 
                    + self.loss_recon_1 + self.loss_recon_2 
                    + self.loss_KL_1_ + self.loss_KL_2_ 
                    + self.loss_cyc_1 + self.loss_cyc_2 
                    + self.loss_recon_X1_log_prob + self.loss_recon_X2_log_prob
                    + self.loss_fake_X1_log_prob + self.loss_fake_X2_log_prob
                    + self.loss_cycle_X1_log_prob + self.loss_cycle_X2_log_prob
                )
                total_loss_G += self.loss_G.item()
                num_batches += 1*self.test_data_loader.batch_size
                
        Test_loss = total_loss_G / num_batches
        
        print("Test Loss: {:.3e}\n".format(Test_loss))
            
        self.E1.train()
        self.E2.train()
        self.G1.train()
        self.G2.train()
        
        return Test_loss
    
    
    #########################
    #  Training
    #########################
    def train(self):
        Test_iterator = iter(self.test_data_loader)
        best_Test_loss = float('inf')
        self.prev_time = time.time()
        
        for epoch in range(1, self.n_epochs + 1):
            Test_losses = []
            
            mini_batch_count = 0
            cum_loss_G = 0.0
            cum_loss_D1 = 0.0
            cum_loss_D2 = 0.0         
            
            
            for i, batch in enumerate(self.data_loader):
                self.X1, self.X2 = batch
                
                self.X1 = self.X1.to(self.device)
                self.X2 = self.X2.to(self.device)
                
                try:
                    Test_batch = next(Test_iterator)
                except StopIteration:
                    Test_iterator = iter(self.test_data_loader)
                    Test_batch = next(Test_iterator)
                
                self.valid_1 = torch.ones((self.X1.size(0), self.D1.shape2))
                self.fake_1 = torch.zeros((self.X1.size(0), self.D1.shape2))
                
                self.valid_2 = torch.ones((self.X2.size(0), self.D2.shape2))
                self.fake_2 = torch.zeros((self.X2.size(0), self.D2.shape2))
                
                self.valid_1 = self.valid_1.to(self.device)
                self.valid_2 = self.valid_2.to(self.device)
                self.fake_1 = self.fake_1.to(self.device)
                self.fake_2 = self.fake_2.to(self.device)
                
                
                #########################
                #  Train E and G
                #########################
                self.optimizer_G.zero_grad()
                
                # Get shared latent representation
                self.qz1, _, _, self.Z1 = self.E1(self.X1)
                self.qz2, _, _, self.Z2 = self.E2(self.X2)
                
                
                # Reconstruct scRNA-seq
                self.recon_pz1, _, self.recon_X1, self.recon_X1_log_prob = self.G1(self.Z1, self.X1)
                self.recon_pz2, _, self.recon_X2, self.recon_X2_log_prob = self.G2(self.Z2, self.X2)
                
                
                # Translate scRNA-seq
                self.fake_pz1, _, self.fake_X1, self.fake_X1_log_prob = self.G1(self.Z2, self.X2)
                self.fake_pz2, _, self.fake_X2, self.fake_X2_log_prob = self.G2(self.Z1, self.X1)

                
                # Cycle translation
                self.qz1_, _, _, self.Z1_ = self.E1(self.fake_X1)
                self.qz2_, _, _, self.Z2_ = self.E2(self.fake_X2)
                
                self.cycle_pz1, self.cycle_X1_px, self.cycle_X1, self.cycle_X1_log_prob = self.G1(self.Z2_, self.X1)
                self.cycle_pz2, self.cycle_X2_px, self.cycle_X2, self.cycle_X2_log_prob = self.G2(self.Z1_, self.X2)

                
                self.Z1 = self.Z1.to(self.device)
                self.Z2 = self.Z2.to(self.device)
                self.recon_X1 = self.recon_X1.to(self.device)
                self.recon_X2 = self.recon_X2.to(self.device)
                self.fake_X1 = self.fake_X1.to(self.device)
                self.fake_X2 = self.fake_X2.to(self.device)
                self.Z1_ = self.Z1_.to(self.device)
                self.Z2_ = self.Z2_.to(self.device)
                self.cycle_X1 = self.cycle_X1.to(self.device)
                self.cycle_X2 = self.cycle_X2.to(self.device)
                

                # Losses
                self.loss_GAN_1 = self.lambda_0 * self.criterion_GAN(self.D1(self.fake_X1), self.valid_1)
                self.loss_GAN_2 = self.lambda_0 * self.criterion_GAN(self.D2(self.fake_X2), self.valid_2)

                self.loss_KL_1 = self.lambda_1 * kl(self.qz1, self.recon_pz1).sum(dim=1).mean(dim=0)
                self.loss_KL_2 = self.lambda_1 * kl(self.qz2, self.recon_pz2).sum(dim=1).mean(dim=0)

                self.loss_recon_1 = self.lambda_2 * self.criterion_VAE(self.recon_X1, self.X1)
                self.loss_recon_2 = self.lambda_2 * self.criterion_VAE(self.recon_X2, self.X2)

                self.loss_KL_1_ = self.lambda_3 * kl(self.qz1_, self.cycle_pz1).sum(dim=1).mean(dim=0)
                self.loss_KL_2_ = self.lambda_3 * kl(self.qz2_, self.cycle_pz2).sum(dim=1).mean(dim=0)
                
                self.loss_cyc_1 = self.lambda_4 * self.criterion_VAE(self.cycle_X1, self.X1)
                self.loss_cyc_2 = self.lambda_4 * self.criterion_VAE(self.cycle_X2, self.X2)
                
                ### NNL for ZINB
                self.loss_recon_X1_log_prob = self.lambda_5 * -self.recon_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_recon_X2_log_prob = self.lambda_5 * -self.recon_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X1_log_prob = self.lambda_5 * -self.fake_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X2_log_prob = self.lambda_5 * -self.fake_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X1_log_prob = self.lambda_5 * -self.cycle_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X2_log_prob = self.lambda_5 * -self.cycle_X2_log_prob.sum(dim=1).mean(dim=0)
                
                # Total loss
                self.loss_G = (
                    self.loss_GAN_1 + self.loss_GAN_2
                    + self.loss_KL_1 + self.loss_KL_2 
                    + self.loss_recon_1 + self.loss_recon_2 
                    + self.loss_KL_1_ + self.loss_KL_2_ 
                    + self.loss_cyc_1 + self.loss_cyc_2
                    + self.loss_recon_X1_log_prob + self.loss_recon_X2_log_prob
                    + self.loss_fake_X1_log_prob + self.loss_fake_X2_log_prob
                    + self.loss_cycle_X1_log_prob + self.loss_cycle_X2_log_prob
                )
                self.loss_G = self.loss_G.float()
                cum_loss_G += self.loss_G.item()
                
                self.loss_G.backward()
                self.optimizer_G.step()
                
                torch.cuda.empty_cache()
                
                #########################
                #  Train Discriminator 1
                #########################
                self.optimizer_D1.zero_grad()

                self.loss_D1 = self.criterion_GAN(self.D1(self.X1), self.valid_1) + self.criterion_GAN(self.D1(self.fake_X1), self.fake_1)
                
                cum_loss_D1 += self.loss_D1.item()
                
                self.loss_D1.backward()
                self.optimizer_D1.step()
                
                #########################
                #  Train Discriminator 2
                #########################
                self.optimizer_D2.zero_grad()
                
                self.loss_D2 = self.criterion_GAN(self.D2(self.X2), self.valid_2) + self.criterion_GAN(self.D2(self.fake_X2), self.fake_2)
                
                cum_loss_D2 += self.loss_D2.item()
                
                self.loss_D2.backward()
                self.optimizer_D2.step()

                #########################
                #  Log Progress
                #########################
                mini_batch_count += 1*self.data_loader.batch_size
                ave_loss_G = cum_loss_G / mini_batch_count
                ave_loss_D1 = cum_loss_D1 / mini_batch_count
                ave_loss_D2 = cum_loss_D2 / mini_batch_count
                
                # Determine approximate time left
                self.batches_done = epoch * len(self.data_loader) + i
                self.batches_left = self.n_epochs * len(self.data_loader) - self.batches_done
                if self.batches_left > 0:
                    self.time_left = datetime.timedelta(seconds=self.batches_left * (time.time() - self.prev_time))
                else:
                    self.time_left = datetime.timedelta(seconds=0)

                self.prev_time = time.time()
                eta_str = str(self.time_left).split('.')[0]
                
                sys.stdout.write(
                    "\r[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f] ETA: %s"
                    % (epoch, self.n_epochs, i, len(self.data_loader), ((self.loss_D1 + self.loss_D2)/self.data_loader.batch_size).item(), (self.loss_G.sum()/self.data_loader.batch_size).item(), eta_str))
            
            print(f"\n[Epoch {epoch}/{self.n_epochs}] [Ave_D loss: {ave_loss_D1 + ave_loss_D2:.3e}] [Ave_G loss: {ave_loss_G:.3e}]")
            
            Test_loss = self.Test()
            Test_losses.append(Test_loss)
            
            if epoch > 20:
                if Test_loss <= best_Test_loss:
                    best_Test_loss = Test_loss
                    self.Test_loss = Test_loss
                    self.save_model_weight(self.save_models_dir, epoch)
            
            # Update learning rates
            self.lr_scheduler_G.step()
            self.lr_scheduler_D1.step()
            self.lr_scheduler_D2.step()