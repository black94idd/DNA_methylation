import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. 讀取 Step 3 產出的合併大表
try:
    combined_df = pd.read_csv('combined_metadata_matrix.csv', index_col=0)
    print("✅ 成功讀取合併矩陣。")

    # 2. 準備特徵數據：排除非數值的標籤欄位 (Country 和 Condition)
    # 這樣 PCA 才會只計算基因位點的差異
    features = combined_df.drop(columns=['Country', 'Condition'])

    # 3. Z-score 標準化 (跨研究合併時這步極度重要，因為兩國實驗室數值基準可能不同)
    scaled_data = StandardScaler().fit_transform(features)

    # 4. 執行 PCA 運算 (取前兩個主成分)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)

    # 5. 建立座標結果表
    pca_res_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'], index=combined_df.index)
    
    # 把剛才拿掉的國家和疾病標籤接回來
    pca_res_df['Country'] = combined_df['Country']
    pca_res_df['Condition'] = combined_df['Condition']

    # 6. 儲存 PCA 座標結果
    pca_res_df.to_csv('combined_pca_results.csv')
    
    # 印出解釋變異量
    var_exp = pca.explained_variance_ratio_
    print(f"\n--- ✅ Step 4 運算完成 ---")
    print(f"PC1 解釋量: {var_exp[0]:.2%}")
    print(f"PC2 解釋量: {var_exp[1]:.2%}")
    print(f"PCA 座標已存為: combined_pca_results.csv")

except Exception as e:
    print(f"❌ 發生錯誤：{e}")