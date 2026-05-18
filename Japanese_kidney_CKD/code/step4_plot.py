import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 讀取 Step 3 產出的數據 (包含 PC1, PC2 座標與 Group 標籤)
try:
    pca_df = pd.read_csv('jp_pca_results.csv', index_col=0)
    print("✅ 成功讀取 PCA 結果數據。")
except FileNotFoundError:
    print("❌ 錯誤：找不到 jp_pca_results.csv，請先執行 Step 3。")
    exit()

# 2. 繪圖設定 (參考你提供的範例風格)
plt.figure(figsize=(9, 7))
# 使用 whitegrid 會有淡淡的背景網格，若要完全空白背景可改用 "white"
sns.set_style("whitegrid") 

# 定義組別的顏色與圖示
colors = {'Normal': '#2ecc71', 'CKD': '#3498db'} # 綠色 vs 藍色
markers = {'Normal': 'X', 'CKD': 'o'} # 叉叉 vs 圓圈

# 3. 畫出原始樣本散佈點 (最核心的步驟)
# 我們分開畫兩組，以便精確控制顏色和圖示
for group in pca_df['Group'].unique():
    subset = pca_df[pca_df['Group'] == group]
    
    plt.scatter(
        subset['PC1'], 
        subset['PC2'], 
        label=group,               # 圖例名稱
        color=colors[group],       # 點的顏色
        marker=markers[group],     # 點的形狀 (X 或 o)
        s=150,                     # 點的大小 (適中)
        edgecolor='w',             # 點的白色邊框 (讓點更清晰)
        alpha=0.9,                 # 點的透明度 (略微透明)
        zorder=10                  # 確保點在網格線之上
    )

# 4. 修飾座標軸與圖表細節
# 加上通過原點 (0,0) 的淡淡參考線 (這是 PCA 圖的慣例，非點對點連線)
plt.axhline(0, color='grey', linestyle='-', alpha=0.1, linewidth=1)
plt.axvline(0, color='grey', linestyle='-', alpha=0.1, linewidth=1)

# 設定標題與座標軸標籤
plt.title('Unsupervised Dimensionality Reduction (PCA) - Japanese Dataset', fontsize=14, pad=15)
plt.xlabel('Principal Component 1 (PC1)', fontsize=12)
plt.ylabel('Principal Component 2 (PC2)', fontsize=12)

# 設定圖例
plt.legend(title="Group", title_fontsize=11, fontsize=10, loc='best', frameon=True)

# 優化排版並存檔
plt.tight_layout()
plt.savefig('Japanese_PCA_Pure_Scatter.png', dpi=300)
plt.show()

print("🎉 Step 4 完成：已產出純淨的 PCA 散佈圖（無框線、無連線）。")