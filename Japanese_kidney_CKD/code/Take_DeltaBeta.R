# Take_DeltaBeta.R

# 載入前一個腳本的函數 (請確保兩個腳本在同一目錄)
source("Normalized_DMP_filter.R")

# 建立一個通用的去除離群值函數
remove_outliers <- function(df) {
  # 轉為矩陣以加速運算
  mat <- as.matrix(df)
  
  # 計算每個 row 的 Q1 與 Q3 (MARGIN = 1 代表 row)
  # R 內建的 quantile 預設演算法(type=7)與 Pandas 的線性內插預設值相同
  quants <- apply(mat, 1, quantile, probs = c(0.25, 0.75), na.rm = TRUE)
  Q1 <- quants[1, ]
  Q3 <- quants[2, ]
  IQR_val <- Q3 - Q1
  
  lower_outlier <- Q1 - 1.5 * IQR_val
  upper_outlier <- Q3 + 1.5 * IQR_val
  
  # 建立布林遮罩 (利用 sweep 函數進行 row-wise 比較)
  mask_lower <- sweep(mat, 1, lower_outlier, ">=")
  mask_upper <- sweep(mat, 1, upper_outlier, "<=")
  mask <- mask_lower & mask_upper
  
  # 將不在範圍內 (False) 的值轉為 NA (等同於 Pandas 的 where)
  mat[!mask] <- NA
  
  return(as.data.frame(mat))
}

run_take_delta_beta <- function(base_dir) {
  # 1. 取得 CG 與 EG 資料
  cat("正在執行篩選與分組...\n")
  filtered_data <- run_normalized_dmp_filter(base_dir)
  CG <- filtered_data$CG
  EG <- filtered_data$EG
  
  # 2. 去除 CG 與 EG 的離群值
  cat("正在去除離群值...\n")
  CG_outliers_removed <- remove_outliers(CG)
  EG_outliers_removed <- remove_outliers(EG)
  
  # 3. 計算 CG 平均值 (忽略 NA)
  CG_mean_values <- rowMeans(CG_outliers_removed, na.rm = TRUE)
  
  # 4. 計算 Delta Beta (EG - CG_mean)
  # 使用 sweep 將 CG_mean_values 逐列 (row-wise) 扣除
  delta_beta_mat <- sweep(as.matrix(EG_outliers_removed), 1, CG_mean_values, "-")
  delta_beta <- as.data.frame(delta_beta_mat)
  
  # 5. 去除 Delta Beta 的離群值並計算平均
  delta_beta_outliers_removed <- remove_outliers(delta_beta)
  delta_beta_mean_values <- rowMeans(delta_beta_outliers_removed, na.rm = TRUE)
  
  # 轉回 DataFrame 格式以符合原始輸出的樣式
  output_df <- data.frame(delta_beta_mean_values)
  colnames(output_df) <- c("Delta_Beta_Mean")
  
  # 6. 輸出結果
  output_path <- file.path(base_dir, "csv", "delta_beta_mean_values.csv")
  write.csv(output_df, output_path, row.names = TRUE)
  cat("Delta Beta 平均值計算完成並已儲存。\n")
  
  return(output_df)
}

# 模擬 Python 的 if __name__ == "__main__": (已移除 if 限制，讓 RStudio 可以直接跑)
base_dir <- file.path(getwd(), "..")
delta_beta_results <- run_take_delta_beta(base_dir)
print(head(delta_beta_results)) # 印出前幾筆檢查