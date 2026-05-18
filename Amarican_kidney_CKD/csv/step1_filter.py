import pandas as pd

file_path = r'C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Amarican_kidney_CKD\csv\delta_beta_mean_values.csv'

try:
    # 讀取學長指定的檔案
    df = pd.read_csv(file_path)
    
    # 1. 欄位設定
    id_col = 'CpG_ID'
    db_col = '0'  # 學長的檔案中 delta beta 的欄位名稱
    
    # 2. 建立絕對值欄位進行排序
    # 因為這份檔案看起來是「計算結果」，我們直接取絕對值最大的前 10
    df['abs_delta_beta'] = df[db_col].abs()
    top_10 = df.sort_values(by='abs_delta_beta', ascending=False).head(10)
    
    print("\n--- 恭喜！根據實驗室數據選出的前 10 名 DMPs ---")
    print(top_10[[id_col, db_col]])
    
    # 這是我們要的「正確版本」關鍵清單
    target_ids = top_10[id_col].tolist()
    print("\n請把這 10 個 ID 複製給我，我們重新跑 PCA：")
    print(target_ids)

except Exception as e:
    print(f"執行出錯：{e}")
    print("請確認檔案內容是否如截圖所示？")