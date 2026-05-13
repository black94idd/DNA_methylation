import pandas as pd
import os

class NormalizedDMPFilter:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.Normalization_path = os.path.join(self.base_dir, "csv/all_beta_normalized.csv")
        self.DMP_path = os.path.join(self.base_dir, "csv/DMP_result_TC.csv")
        self.Sample_Sheet_path = os.path.join(self.base_dir, "processing_data/Sample_sheet.csv")

        self.Normalization = None
        self.DMP = None
        self.Sample_Sheet = None

        self.filtered_Normalization = None
        self.EG = None
        self.CG = None

    def load_data(self):
        self.Normalization = pd.read_csv(self.Normalization_path, index_col=0, encoding='utf-8')
        self.DMP = pd.read_csv(self.DMP_path, index_col=0, encoding='utf-8')
        self.Sample_Sheet = pd.read_csv(self.Sample_Sheet_path, encoding='utf-8')
        print("資料讀取完成")

    def filter_data(self):
        common_CpG = self.Normalization.index.intersection(self.DMP.index)
        print(f"共有 {len(common_CpG)} 筆相同的 ID 資料。")

        self.filtered_Normalization = self.Normalization.loc[common_CpG]
        self.filtered_Normalization.index.name = 'CpG_ID'
        print(f"篩選完成！共保留了 {len(self.filtered_Normalization)} 筆相同的 ID 資料。")

    def split_groups(self):
        self.Sample_Sheet['Sample_Name'] = self.Sample_Sheet['Sample_Name'].astype(str)

        ckd_samples = self.Sample_Sheet[self.Sample_Sheet['Sample_Group'] == 'C']['Sample_Name'].tolist()
        normal_samples = self.Sample_Sheet[self.Sample_Sheet['Sample_Group'] == 'N']['Sample_Name'].tolist()
        print(f"在 Sample Sheet 中找到 {len(ckd_samples)} 個 CKD 樣本，{len(normal_samples)} 個 Normal 樣本。")

        ckd_cols = [col for col in ckd_samples if col in self.filtered_Normalization.columns]
        normal_cols = [col for col in normal_samples if col in self.filtered_Normalization.columns]

        self.EG = self.filtered_Normalization[ckd_cols]
        self.CG = self.filtered_Normalization[normal_cols]
    
    def save_results(self):
        self.EG.to_csv(os.path.join(self.base_dir, "csv", "EG_filtered.csv"), encoding='utf-8') # 實驗組的輸出檔名
        self.CG.to_csv(os.path.join(self.base_dir, "csv", "CG_filtered.csv"), encoding='utf-8') # 對照組的輸出檔名
        print("結果已儲存")
    
    def run(self):
        self.load_data()
        self.filter_data()
        self.split_groups()
        self.save_results()
        return self.CG, self.EG
    
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'
    filter = NormalizedDMPFilter(base_dir)
    CG, EG = filter.run()
    

#base_dir = os.path.dirname(os.path.abspath(__file__))
#
#Normal = pd.read_csv(os.path.join(base_dir, "csv/all_beta_normalized.csv"), index_col=0, encoding='utf-8')
#DMP = pd.read_csv(os.path.join(base_dir, "csv/DMP_result_TC.csv"), index_col=0, encoding='utf-8')
#
#common_CpG = Normal.index.intersection(DMP.index)
#print(f"共有 {len(common_CpG)} 筆相同的 ID 資料。")
##print("共同欄位名稱:", common_CpG.tolist())
#
#filtered_Normal = Normal.loc[common_CpG]
#filtered_Normal.index.name = 'CpG_ID'
#
##output_path = os.path.join(base_dir, "csv", "Normal_filtered.csv") # 新的輸出檔名
##filtered_Normal.to_csv(output_path, encoding='utf-8')
#
#print(f"篩選完成！共保留了 {len(filtered_Normal)} 筆相同的 ID 資料。")
##print(f"檔案已儲存至：{output_path}")
#
#
##------------------------------分成實驗組與對照組------------------------------#
#
#Sample_Sheet = pd.read_csv(os.path.join(base_dir, "processing_data/Sample_sheet.csv"), encoding='utf-8')
#Sample_Sheet['Sample_Name'] = Sample_Sheet['Sample_Name'].astype(str)
#
#ckd_samples = Sample_Sheet[Sample_Sheet['Sample_Group'] == 'CKD']['Sample_Name'].tolist()
#normal_samples = Sample_Sheet[Sample_Sheet['Sample_Group'] == 'Normal']['Sample_Name'].tolist()
#print(f"在 Sample Sheet 中找到 {len(ckd_samples)} 個 CKD 樣本，{len(normal_samples)} 個 Normal 樣本。")
#
#ckd_cols = [col for col in ckd_samples if col in filtered_Normal.columns]
#normal_cols = [col for col in normal_samples if col in filtered_Normal.columns]
#
#output_EG = filtered_Normal[ckd_cols]
#output_CG = filtered_Normal[normal_cols]
#
#output_EG.to_csv(os.path.join(base_dir, "csv", "EG_filtered.csv"), encoding='utf-8') # 實驗組的輸出檔名
#output_CG.to_csv(os.path.join(base_dir, "csv", "CG_filtered.csv"), encoding='utf-8') # 對照組的輸出檔名