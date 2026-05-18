import pandas as pd

# 1. 日本大檔案路徑
big_file_jp = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Japanese_kidney_CKD\csv\all_beta_normalized.csv'

# 2. 這是你剛才 Step 1 成功跑出的 10 個日本 ID
target_ids_jp = [
    'cg14856563', 'cg05843596', 'cg12184937', 'cg07609206', 'cg27485152',
    'cg02988288', 'cg25104066', 'cg06878787', 'cg17032138', 'cg06930016'
]

print("🚀 正在從日本大矩陣提取這 10 個核心位點...")

# 使用 chunksize 避免記憶體溢出
chunks = pd.read_csv(big_file_jp, chunksize=5000, index_col=0)
extracted_data = []

for chunk in chunks:
    # 這裡的 index 就是 CpG ID
    matched = chunk[chunk.index.isin(target_ids_jp)]
    if not matched.empty:
        extracted_data.append(matched)

if extracted_data:
    final_df_jp = pd.concat(extracted_data)
    final_df_jp.to_csv('jp_top10_beta_matrix.csv')
    print("\n✅ Step 2 完成！數據已存為: jp_top10_beta_matrix.csv")
else:
    print("\n❌ 錯誤：在大表中找不到這 10 個 ID。請確認 big_file_jp 指向的是 Japanese 資料夾。")