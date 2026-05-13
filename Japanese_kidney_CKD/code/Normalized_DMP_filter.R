# Normalized_DMP_filter.R

run_normalized_dmp_filter <- function(base_dir) {
  # 設定檔案路徑
  normalization_path <- file.path(base_dir, "csv", "all_beta_normalized.csv")
  dmp_path <- file.path(base_dir, "csv", "DMP_result_TC.csv")
  sample_sheet_path <- file.path(base_dir, "processing_data", "Sample_sheet.csv")
  
  # 讀取資料
  # row.names = 1 相當於 pandas 的 index_col=0
  Normalization <- read.csv(normalization_path, row.names = 1, stringsAsFactors = FALSE)
  DMP <- read.csv(dmp_path, row.names = 1, stringsAsFactors = FALSE)
  Sample_Sheet <- read.csv(sample_sheet_path, stringsAsFactors = FALSE)
  cat("資料讀取完成\n")
  
  # 篩選資料 (取交集)
  common_CpG <- intersect(rownames(Normalization), rownames(DMP))
  cat(sprintf("共有 %d 筆相同的 ID 資料。\n", length(common_CpG)))
  
  # subset 取出共同列，drop = FALSE 確保只有一欄時不會被轉為 Vector
  filtered_Normalization <- Normalization[common_CpG, , drop = FALSE]
  cat(sprintf("篩選完成！共保留了 %d 筆相同的 ID 資料。\n", nrow(filtered_Normalization)))
  
  # 分組 (CKD 與 Normal)
  Sample_Sheet$Sample_Name <- as.character(Sample_Sheet$Sample_Name)
  
  ckd_samples <- Sample_Sheet$Sample_Name[Sample_Sheet$Sample_Group == 'C']
  normal_samples <- Sample_Sheet$Sample_Name[Sample_Sheet$Sample_Group == 'N']
  cat(sprintf("在 Sample Sheet 中找到 %d 個 CKD 樣本，%d 個 Normal 樣本。\n", 
              length(ckd_samples), length(normal_samples)))
  
  # 確保取出的 column name 確實存在於 dataframe 中
  ckd_cols <- intersect(ckd_samples, colnames(filtered_Normalization))
  normal_cols <- intersect(normal_samples, colnames(filtered_Normalization))
  
  EG <- filtered_Normalization[, ckd_cols, drop = FALSE]
  CG <- filtered_Normalization[, normal_cols, drop = FALSE]
  
  write.csv(EG, file.path(base_dir, "csv", "EG_filtered.csv"), row.names = TRUE)
  write.csv(CG, file.path(base_dir, "csv", "CG_filtered.csv"), row.names = TRUE)
  cat("結果已儲存\n")
  
  # 回傳兩個 dataframe 以供後續腳本使用
  return(list(CG = CG, EG = EG))
}

# 模擬 Python 的 if __name__ == "__main__":
if (!interactive() && sys.nframe() == 0) {
  # R 語言沒有直接對應 __file__ 的寫法，這裡以當前工作目錄(getwd)代替 base_dir
  base_dir <- file.path(getwd(), "..")
  result <- run_normalized_dmp_filter(base_dir)
}