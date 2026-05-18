import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 讀取 PCA 運算結果
try:
    pca_df = pd.read_csv('combined_pca_results.csv', index_col=0)
    print("✅ 成功讀取合併 PCA 座標。")
except FileNotFoundError:
    print("❌ 錯誤：找不到 combined_pca_results.csv，請先執行 Step 4。")
    exit()

# 2. 繪圖設定
plt.figure(figsize=(10, 7))
sns.set_style("whitegrid") # 乾淨的網格背景

# 定義視覺規範
# 顏色 (Condition): Normal = 綠色, CKD = 藍色
# 圖示 (Country): American = X, Japanese = o
colors = {'Normal': '#2ecc71', 'CKD': '#3498db'}
markers = {'American': 'X', 'Japanese': 'o'}

# 3. 繪製樣本點
# 我們透過迴圈組合，確保每一種標籤組合都被正確繪製
for country in ['American', 'Japanese']:
    for condition in ['Normal', 'CKD']:
        subset = pca_df[(pca_df['Country'] == country) & (pca_df['Condition'] == condition)]
        
        if not subset.empty:
            plt.scatter(
                subset['PC1'], 
                subset['PC2'], 
                label=f"{country} {condition}",
                color=colors[condition],
                marker=markers[country],
                s=160,           # 點的大小
                edgecolor='w',   # 白色邊框增加辨識度
                linewidth=1,
                alpha=0.85,      # 稍微透明感
                zorder=10
            )

# 4. 修飾圖表細節
plt.axhline(0, color='grey', linestyle='-', alpha=0.1, linewidth=1)
plt.axvline(0, color='grey', linestyle='-', alpha=0.1, linewidth=1)

# 設定解釋量標籤 (根據你剛才跑出的數值)
plt.xlabel('Principal Component 1 (57.41%)', fontsize=12)
plt.ylabel('Principal Component 2 (14.07%)', fontsize=12)
plt.title('Cross-Population PCA Analysis: American vs Japanese CKD', fontsize=14, pad=20)

# 圖例設定
plt.legend(title="Populations", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)

plt.tight_layout()
plt.savefig('Combined_Final_Pure_Plot.png', dpi=300)
plt.show()

print("🎉 恭喜！跨國結合分析的最終圖表已產出：Combined_Final_Pure_Plot.png")