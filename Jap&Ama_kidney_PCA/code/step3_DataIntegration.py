import pandas as pd

# 1. 讀取 Step 2 產出的對齊檔案
# 這些檔案應該位於 C:\Users\hyuju\Downloads\DNA_methylation (1)\DNA_methylation\Jap&Ama_kidney_CKD
try:
    df_us = pd.read_csv('us_for_combined.csv', index_col=0).transpose()
    df_jp = pd.read_csv('jp_for_combined.csv', index_col=0).transpose()
    print("✅ 成功讀取美國與日本的對齊數據。")

    # 2. 為美國資料標註國家與疾病狀態
    # 假設美國資料：前一半樣本為 Normal，後一半為 CKD
    df_us['Country'] = 'American'
    num_us = len(df_us)
    df_us['Condition'] = ['Normal'] * (num_us // 2) + ['CKD'] * (num_us - (num_us // 2))

    # 3. 為日本資料標註國家與疾病狀態
    # 假設日本資料：前一半樣本為 Normal，後一半為 CKD
    df_jp['Country'] = 'Japanese'
    num_jp = len(df_jp)
    df_jp['Condition'] = ['Normal'] * (num_jp // 2) + ['CKD'] * (num_jp - (num_jp // 2))

    # 4. 垂直合併 (將兩張表接起來)
    # 因為 Step 2 已經統一了 ID，所以這裡會完美對齊
    combined_df = pd.concat([df_us, df_jp], axis=0)

    # 5. 儲存最終合併大表 (包含標籤)
    combined_df.to_csv('combined_metadata_matrix.csv')

    print(f"\n--- ✅ Step 3 完成 ---")
    print(f"合併後的總樣本數：{len(combined_df)} (美國: {num_us}, 日本: {num_jp})")
    print(f"使用的特徵位點數：{len(df_us.columns) - 2}") # 扣除 Country 和 Condition
    print(f"最終檔案已存為: combined_metadata_matrix.csv")

except FileNotFoundError:
    print("❌ 錯誤：找不到 us_for_combined.csv 或 jp_for_combined.csv。請確認 Step 2 執行成功。")
except Exception as e:
    print(f"❌ 發生錯誤：{e}")