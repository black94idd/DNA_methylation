import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os

class PCA_analysis:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.delta_beta_mean_values_path = os.path.join(self.base_dir, "csv/delta_beta_mean_values.csv")
        self.delta_beta_mean_values = None

        self.dmp_data_path = os.path.join(self.base_dir, "csv/DMP_result_TC.csv")
        self.dmp_data = None

        self.normalization_data_path = os.path.join(self.base_dir, "csv/all_beta_normalized.csv")
        self.normalization_data = None

        self.significant_CpGs = None
        self.pca = None
        self.pca_result = None
        self.pca_df = None
        self.data_for_pca = None

    def load_data(self):
        self.delta_beta_mean_values = pd.read_csv(self.delta_beta_mean_values_path, index_col=0, encoding='utf-8')
        self.dmp_data = pd.read_csv(self.dmp_data_path, index_col=0, encoding='utf-8')
        self.normalization_data = pd.read_csv(self.normalization_data_path, index_col=0, encoding='utf-8')

    def filt_significant_CpGs(self):                        #把非常顯著的位點標記出來
        self.significant_CpGs = self.dmp_data[
                                            (self.dmp_data['N_to_C.adj.P.Val'] < 0.05) &
                                            (abs(self.delta_beta_mean_values['Delta_Beta_Mean']) > 0.2)
                                            ].index.tolist()
        
        print(f"篩選出了 {len(self.significant_CpGs)} 個顯著 CpG！")
        return self.significant_CpGs

    def prepare_data_for_pca(self):
        # 因為 sklearn 的 PCA 要求「Row 是樣本，Column 是基因」，所以必須轉置 (.T)
        self.data_for_pca = self.normalization_data.loc[self.significant_CpGs].T

    def run_pca(self):
        self.prepare_data_for_pca()
        self.pca = PCA(n_components=2)
        self.pca_result = self.pca.fit_transform(self.data_for_pca)

    def identify_groups(self):
        self.run_pca()
        self.pca_df = pd.DataFrame(data=self.pca_result, columns=['PC1', 'PC2'])
        self.pca_df['Sample_Name'] = self.data_for_pca.index
        
        sample_sheet = pd.read_csv(os.path.join(self.base_dir, "processing_data/Sample_sheet.csv"))
        self.pca_df = self.pca_df.merge(sample_sheet[['Sample_Name', 'Sample_Group']], on='Sample_Name')

    def run(self):
        self.load_data()
        self.filt_significant_CpGs()
        self.identify_groups()
        return self.pca_df
    
    def make_plt_pdf(self):
        # 可視化 PCA 結果
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='PC1', y='PC2', hue='Sample_Group', data=self.pca_df, s=100, alpha=0.7)
        plt.title('PCA of Significant CpGs')
        plt.xlabel(f'Principal Component 1 ({self.pca.explained_variance_ratio_[0]*100:.2f}%)')
        plt.ylabel(f'Principal Component 2 ({self.pca.explained_variance_ratio_[1]*100:.2f}%)')
        plt.grid(True)
        
        output_path = os.path.join(self.base_dir, "PCA_of_Significant_CpGs_AM.pdf")
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        print(f"圖表已儲存至: {output_path}")
        plt.show()
        
        

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'
    pca_analysis = PCA_analysis(base_dir)
    pca_analysis.run()
    # print(pca_analysis.significant_CpGs)
    print(pca_analysis.pca_df.head())
    pca_analysis.make_plt_pdf()


    # significant_CpGs = pca_analysis.filt_significant_CpGs()
    # print(significant_CpGs)
    # delta_beta_mean_values = pd.read_csv(base_dir + "/csv/delta_beta_mean_values.csv", index_col=0, encoding='utf-8')
    # print(delta_beta_mean_values['Delta_Beta_Mean'])
    # dmp_data = pd.read_csv(base_dir + "/csv/DMP_result_TC.csv", index_col=0, encoding='utf-8')
    # print(dmp_data['N_to_C.adj.P.Val'])