import pandas as pd
import os

# 1. 設定工作目錄與原始大檔路徑 (請根據你的路徑微調)
base_path = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Jap&Ama_kidney_CKD'
path_us_big = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Amarican_kidney_CKD\csv\all_beta_normalized.csv'
path_jp_big = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Japanese_kidney_CKD\csv\all_beta_normalized.csv'

os.chdir(base_path)

# 2. 定義統一使用的 10 個核心位點 (以日本版為準，因為日本大檔位點較少)
shared_ids = [
    'cg14856563', 'cg05843596', 'cg12184937', 'cg07609206', 'cg27485152',
    'cg02988288', 'cg25104066', 'cg06878787', 'cg17032138', 'cg06930016'
]

def extract_for_combined(big_path, target_ids, output_name):
    print(f"🚀 正在從 {big_path} 提取數據...")
    chunks = pd.read_csv(big_path, chunksize=5000, index_col=0)
    extracted = []
    for chunk in chunks:
        matched = chunk[chunk.index.isin(target_ids)]
        if not matched.empty:
            extracted.append(matched)
    
    if extracted:
        final_df = pd.concat(extracted)
        final_df.to_csv(output_name)
        print(f"✅ 成功產出: {output_name} (位點數: {len(final_df)})")
    else:
        print(f"❌ 錯誤: 在該檔案中找不到指定的位點。")

# 3. 同時執行美國與日本的提取
extract_for_combined(path_us_big, shared_ids, 'us_for_combined.csv')
extract_for_combined(path_jp_big, shared_ids, 'jp_for_combined.csv')