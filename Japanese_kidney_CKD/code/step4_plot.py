import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 讀取 Step 3 產出的美國 PCA 結果
try:
    pca_df = pd.read_csv('us_pca_results.csv', index_col=0)
    print("✅ 成功讀取 us_pca_results.csv")
except FileNotFoundError:
    print("❌ 錯誤：找不到 us_pca_results.csv，請先執行 Step 3。")
    exit()

# 2. 繪圖設定 (純淨散佈圖風格)
plt.figure(figsize=(9, 7))
sns.set_style("whitegrid") # 保持乾淨的白色網格背景

# 定義顏色與圖示 (Normal: 綠色X, CKD: 藍色O)
colors = {'Normal': '#2ecc71', 'CKD': '#3498db'}
markers = {'Normal': 'X', 'CKD': 'o'}

# 3. 畫出原始樣本點 (不加任何邊框或連線)
for group in ['Normal', 'CKD']:
    subset = pca_df[pca_df['Group'] == group]
    plt.scatter(
        subset['PC1'], 
        subset['PC2'], 
        label=group,
        color=colors[group],
        marker=markers[group],
        s=150,           # 點的大小
        edgecolor='w',   # 白色邊框增加辨識度
        linewidth=1,
        alpha=0.9,
        zorder=10
    )

# 4. 修飾細節
plt.title('Unsupervised Dimensionality Reduction (PCA) - American Dataset', fontsize=14, pad=15)
plt.xlabel('Principal Component 1 (PC1)', fontsize=12)
plt.ylabel('Principal Component 2 (PC2)', fontsize=12)

# 加上淡淡的中心參考線 (通過 0,0)
plt.axhline(0, color='grey', linestyle='-', alpha=0.1, linewidth=1)
plt.axvline(0, color='grey', linestyle='-', alpha=0.1, linewidth=1)

# 設定圖例
plt.legend(title="Group", loc='best', frameon=True)

# 優化排版並存檔
plt.tight_layout()
plt.savefig('American_PCA_Pure_Final.png', dpi=300)
plt.show()

print("🎉 恭喜！美國資料的純淨版 PCA 圖已完成：American_PCA_Pure_Final.png")