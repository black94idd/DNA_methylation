import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. 讀取 Step 2 產出的美國小矩陣
try:
    # 讀取並轉置 (使樣本變成橫列，基因變成直欄)
    df_us = pd.read_csv('us_top10_beta_matrix.csv', index_col=0).transpose()
    print("✅ 成功讀取 us_top10_beta_matrix.csv")

    # 2. 數據標準化 (Z-score Scaling)
    # PCA 對數值縮放很敏感，這一步是必須的
    scaled_data = StandardScaler().fit_transform(df_us)

    # 3. 執行 PCA 運算 (取前兩個主成分)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)

    # 4. 建立結果表格並標註組別
    # 依照美國資料集的樣本分佈，假設前一半是 Normal，後一半是 CKD
    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'], index=df_us.index)
    
    total_samples = len(pca_df)
    half = total_samples // 2
    pca_df['Group'] = ['Normal'] * half + ['CKD'] * (total_samples - half)

    # 5. 儲存計算結果座標
    pca_df.to_csv('us_pca_results.csv')
    
    # 印出解釋變異量 (Explained Variance) 供參考
    var_exp = pca.explained_variance_ratio_
    print(f"\n--- ✅ Step 3 計算完成 ---")
    print(f"PC1 解釋量: {var_exp[0]:.2%}")
    print(f"PC2 解釋量: {var_exp[1]:.2%}")
    print(f"結果已存為: us_pca_results.csv")

except FileNotFoundError:
    print("❌ 錯誤：找不到 us_top10_beta_matrix.csv。請確認 Step 2 是否執行成功。")
except Exception as e:
    print(f"❌ 發生錯誤：{e}")