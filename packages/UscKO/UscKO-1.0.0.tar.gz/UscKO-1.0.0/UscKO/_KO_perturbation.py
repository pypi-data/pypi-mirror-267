from scipy.stats import entropy
import pandas as pd

class KO_perturbation():
    def __init__(self, adata=None, Condition="A2B"):
        """
        Extracting Virtual Knockout Results Tool.

        Arguments:
        - adata (AnnData, required): An AnnData object obtained through "Virtual_KO_A2B" or "Virtual_KO_B2A".
        - Condition(str, required): Specifies the direction of virtual KO condition transformation. "A2B" or "B2A", default is "A2B".
        """
        self.epsilon = 1e-10
        self.gene_index = adata.var_names
        self.V_KO = None
        self.V = None
        
        #if not self.gene_index:
        if self.gene_index.empty:
            raise ValueError("Gene index is empty. Please provide a valid adata with gene information.")

        if Condition == "A2B":
            self.V_KO = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_KO_A2B"].X.T)
            self.V = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_A2B"].X.T) + self.epsilon
        elif Condition == "B2A":
            self.V_KO = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_KO_B2A"].X.T)
            self.V = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_B2A"].X.T) + self.epsilon
        else:
            raise ValueError("Invalid Condition. Supported values: 'A2B' or 'B2A'.")
        
        self.KO_results = self.calculate_kl_divergence()
        
    def calculate_kl_divergence(self):
        KL_value = pd.DataFrame(index=self.gene_index, columns=['KL_value','Virtual_KO_expression',
                                                                "Virtual_expression","Perturbation_Direction"])
        
        for index, row in self.V_KO.iterrows():
            kl_value = entropy(row.values, self.V.loc[index].values)
            KL_value.at[self.gene_index[index], 'KL_value'] = kl_value
            
            V_KO_mean = row.mean()
            KL_value.at[self.gene_index[index], 'Virtual_KO_expression'] = V_KO_mean
            
            V_mean = (self.V.loc[index] - self.epsilon).mean()
            KL_value.at[self.gene_index[index], 'Virtual_expression'] = V_mean
            
            PD = V_KO_mean - V_mean
            
            if PD > 0:
                KL_value.at[self.gene_index[index], 'Perturbation_Direction'] = 'Up'
            elif PD < 0:
                KL_value.at[self.gene_index[index], 'Perturbation_Direction'] = 'Down'
            else:
                KL_value.at[self.gene_index[index], 'Perturbation_Direction'] = 'None'
                
        KL_value.sort_values(by='KL_value', ascending=False, inplace=True)
        
        return KL_value