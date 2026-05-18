import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. 讀取提取後的小矩陣
df_jp = pd.read_csv('jp_top10_beta_matrix.csv', index_col=0).transpose()

# 2. 標準化數據
scaled_data = StandardScaler().fit_transform(df_jp)

# 3. 執行 PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

# 4. 建立結果表格並標註組別 (假設前一半 Normal，後一半 CKD)
pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'], index=df_jp.index)
half = len(pca_df) // 2
pca_df['Group'] = ['Normal'] * half + ['CKD'] * (len(pca_df) - half)

# 5. 存出數據供畫圖使用
pca_df.to_csv('jp_pca_results.csv')
print("Step 3 完成：數據已存檔。")