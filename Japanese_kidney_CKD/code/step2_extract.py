import pandas as pd

# 1. 設定路徑 (請確認路徑名稱 Amarican 是否正確)
big_file_us = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Amarican_kidney_CKD\csv\all_beta_normalized.csv'
delta_file_us = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Amarican_kidney_CKD\csv\delta_beta_mean_values.csv'

print("🔄 正在讀取美國資料大表索引...")

try:
    # 2. 獲取大表現有的所有 ID (只讀取第一欄以節省時間)
    all_ids_df = pd.read_csv(big_file_us, usecols=[0])
    big_table_ids = set(all_ids_df.iloc[:, 0].astype(str).str.strip().tolist())
    print(f"大表讀取完成，共有 {len(big_table_ids)} 個可用位點。")

    # 3. 讀取美國差異分析表
    delta_df = pd.read_csv(delta_file_us)
    
    # 統一 ID 格式並進行比對
    # 假設第一欄是 ID，最後一欄或 '0' 欄是 Delta Beta 數值
    delta_df['tmp_id'] = delta_df.iloc[:, 0].astype(str).str.strip()
    
    # 只留下在大表裡存在的位點
    filtered_delta = delta_df[delta_df['tmp_id'].isin(big_table_ids)].copy()
    
    # 選出絕對值最大的前 10 名
    # 依照你截圖的結構，數值通常在第二欄或名為 '0' 的欄位
    val_col_idx = 1 # 如果報錯，請確認數值欄位位置
    filtered_delta['abs_db'] = filtered_delta.iloc[:, val_col_idx].abs()
    top_10_rescue = filtered_delta.sort_values(by='abs_db', ascending=False).head(10)
    
    rescue_ids = top_10_rescue['tmp_id'].tolist()
    print(f"\n✅ 已重新選出 10 個在大表中存在的美國位點：\n{rescue_ids}")

    # 4. 正式提取數據
    print("\n🚀 開始從大表中提取這 10 個位點的數值...")
    chunks = pd.read_csv(big_file_us, chunksize=5000, index_col=0)
    extracted_data = []
    
    for chunk in chunks:
        matched = chunk[chunk.index.isin(rescue_ids)]
        if not matched.empty:
            extracted_data.append(matched)

    if extracted_data:
        final_df_us = pd.concat(extracted_data)
        final_df_us.to_csv('us_top10_beta_matrix.csv')
        print(f"\n--- ✅ Step 2 成功完成 ---")
        print(f"檔案已存為: us_top10_beta_matrix.csv")
    else:
        print("\n❌ 提取失敗，請檢查大表格式。")

except Exception as e:
    print(f"❌ 發生錯誤：{e}")