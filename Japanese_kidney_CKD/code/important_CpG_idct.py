import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
imp_path = os.path.join(current_dir, '..', 'csv/jp_important_CpGs.csv')
dmp_path = os.path.join(current_dir, '..', 'csv/DMP_result_TC.csv')

df_imp = pd.read_csv(imp_path)
df_dmp = pd.read_csv(dmp_path)

# 因為 DMP_result_TC.csv 第一欄通常是沒有名稱的(或是 'Unnamed: 0')，
# 我們要把它改名為 'CpG_Site'，才能跟 df_imp 的欄位對接起來。
first_col_name = df_dmp.columns[0]
df_dmp.rename(columns={first_col_name: 'CpG_Site'}, inplace=True)

# how='left' 代表 left join，以 df_imp 為主體，找不到的會顯示 NaN
merged_df = pd.merge(
    df_imp, 
    # 這裡我們只挑選 DMP 表格中有用的欄位，避免合併後表格變得太肥大
    df_dmp[['CpG_Site', 'N_to_C.gene', 'N_to_C.deltaBeta', 'N_to_C.adj.P.Val']], 
    on='CpG_Site', 
    how='left'
)

print(merged_df.head(10))
merged_df.to_csv(os.path.join(current_dir, '..', 'csv/jp_important_CpGs_with_genes.csv'), index=False)
print("成功將基因註釋合併，並存成 jp_important_CpGs_with_genes.csv！")