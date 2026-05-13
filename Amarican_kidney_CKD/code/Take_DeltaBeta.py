import pandas as pd
import os
import numpy as np
from Normalized_DMP_filter import NormalizedDMPFilter

class take_delta_beta:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.filter = NormalizedDMPFilter(self.base_dir)
        self.CG, self.EG = self.filter.run()

        self.delta_beta = None

        self.CG_outliers_removed = None
        self.EG_outliers_removed = None
        self.delta_beta_outliers_removed = None

        self.CG_mean_values = None
        self.delta_beta_mean_values = None

        

    def remove_outliers(self, group):
        if group == 'CG':
            df = self.CG
        elif group == 'EG':
            df = self.EG
        elif group == 'delta_beta':
            df = self.delta_beta
        else:
            print("Error: 參數請填入CG or EG or delta_beta")
            return
        
        Q1 = df.quantile(0.25, axis=1)
        Q3 = df.quantile(0.75, axis=1)
        IQR = Q3 - Q1

        upper_outlier = Q3 + 1.5 * IQR
        lower_outlier = Q1 - 1.5 * IQR

        #布林遮罩(Mask)，將不在範圍內的值標記為False，其他為True
        #用.ge() (greater than or equal)和.le() (less than or equal)，並指定 axis=0 讓它對齊「列」
        mask = df.ge(lower_outlier, axis=0) & df.le(upper_outlier, axis=0)

        if group == 'CG':
            self.CG_outliers_removed = df.where(mask)
        elif group == 'EG':
            self.EG_outliers_removed = df.where(mask)
        elif group == 'delta_beta':
            self.delta_beta_outliers_removed = df.where(mask)

    def CG_mean(self):
        if self.CG_outliers_removed is not None:
            self.CG_mean_values = self.CG_outliers_removed.mean(axis=1)
        else:
            print("Error: 請先執行 remove_outliers('CG') 以移除 CG 的離群值。")
    
    def calculate_delta_beta(self):
        if self.CG_mean_values is not None and self.EG_outliers_removed is not None:
            self.delta_beta = self.EG_outliers_removed.subtract(self.CG_mean_values, axis=0)
        else:
            print("Error: 請先執行 CG_mean() 和 remove_outliers('EG') 以計算 delta beta。")
        
    def run(self):
        self.remove_outliers('CG')
        self.remove_outliers('EG')
        self.CG_mean()
        self.calculate_delta_beta()
        self.remove_outliers('delta_beta')
        self.delta_beta_mean_values = self.delta_beta_outliers_removed.mean(axis=1)
        self.delta_beta_mean_values.to_csv(os.path.join(self.base_dir, "csv", "delta_beta_mean_values.csv"), encoding='utf-8') # delta beta 平均值的輸出檔
        return self.delta_beta_mean_values

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/..'
    outliers_remover = take_delta_beta(base_dir)
    delta_beta_mean_values = outliers_remover.run()
    print(delta_beta_mean_values)