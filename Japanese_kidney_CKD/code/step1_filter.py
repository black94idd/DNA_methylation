import pandas as pd

# 1. 日本資料路徑
file_path = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Japanese_kidney_CKD\csv\delta_beta_mean_values.csv'

try:
    # 讀取檔案
    df = pd.read_csv(file_path)
    
    # 2. 自動偵測欄位
    # 第一欄通常是 CpG_ID，最後一欄通常是數值
    id_col = df.columns[0]
    db_col = df.columns[-1] 
    
    print(f"偵測到 ID 欄位：{id_col}")
    print(f"偵測到數值欄位：{db_col}")
    
    # 3. 建立絕對值進行排序
    # 確保數值欄位是浮點數
    df[db_col] = pd.to_numeric(df[db_col], errors='coerce')
    df['abs_delta_beta'] = df[db_col].abs()
    
    # 4. 取得前 10 名
    top_10 = df.sort_values(by='abs_delta_beta', ascending=False).head(10)
    
    print("\n--- ✅ 日本資料前 10 名 DMPs ---")
    print(top_10[[id_col, db_col]])
    
    # 輸出 ID 清單供 Step 2 使用
    target_ids = top_10[id_col].tolist()
    print("\n請複製這組 ID 到 Step 2：")
    print(target_ids)

except Exception as e:
    print(f"❌ 還是出錯了：{e}")
    print("目前檔案的欄位名稱列表：", df.columns.tolist() if 'df' in locals() else "無法讀取檔案")