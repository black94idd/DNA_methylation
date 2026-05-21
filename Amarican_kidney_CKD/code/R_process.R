#install.packages("BiocManager")
#BiocManager::install("ChAMP")

library("ChAMP")

library(stringr)

path <- file.path(getwd(), "..")

my_pd <- read.csv(str_c(path, "/processing_data/Sample_sheet.csv"))

# Basename不動，用 stringr 套件拆解，並新增兩個欄位
# 用底線 "_" 切割成3等份 (樣本_ID_位置)
#split_basename <- str_split_fixed(my_pd$Basename, "_", 3)

# 將切割出的第2部分存成 Sentrix_ID，第3部分存成 Sentrix_Position
#my_pd$Sentrix_ID <- split_basename[, 2]
#my_pd$Sentrix_Position <- split_basename[, 3]

# 3. 覆蓋原本的 Sample_sheet.csv (記得 quote = FALSE, row.names = FALSE)
#write.csv(my_pd, file = str_c(path, "/processing_data/Sample_sheet.csv"), quote = FALSE, row.names = FALSE)

# QC
myLoad <- champ.load(
  directory = str_c(path, "/processing_data"),
  arraytype = "EPIC",
  method = "minfi",         # 底層使用 minfi 讀取與計算 P-value
  
  # 探針失效QC處理
  filterDetP = TRUE,        # 開啟偵測 P 值過濾
  detPcut = 0.01,           # 判定探針失效 (P > 0.01 即視為訊號不可信/撞針故障)
  ProbeCutoff = 0.05,       # 【探針過濾】if某個 CpG 點位在超過 5% 的樣本中都失效，剔除該點位
  SampleCutoff = 0.05,      # 【樣本過濾】if某個病患/樣本有超過 5% 的點位失效，就整個人剔除
  
  # 其他標準化生資QC處理
  filterBeads = TRUE,       # 剔除 Bead count < 3 的探針 (物理性偵測不良)
  filterNoCG = TRUE,        # 剔除探針名稱非 cg 開頭的點位 (非 CpG 點位)
  filterSNPs = TRUE,        # 剔除序列中包含 SNP 的探針 (避免基因多態性干擾甲基化判讀)
  filterMultiHit = TRUE,    # 剔除會發生非特異性結合 (Cross-reactive) 的探針
  filterXY = TRUE,          # 剔除 X, Y 染色體上的探針 (避免性別差異造成的偏差)
  
  force = TRUE              #因為有些idat檔案大小差2KB，minifi安全性報錯，需強制執行
)

myNorm <- champ.norm(beta = myLoad$beta, plotBMIQ = FALSE, cores = 10 , arraytype = "EPIC")

write.csv(myNorm, file = str_c(path, "/csv/", "all_beta_normalized.csv"), quote = F, row.names = T)

# 我們用變異數過濾(Variance Filtering)，刪除明顯不顯著的CpG，藉此降低懲罰係數
# =====================================================================

# 1. 計算 myNorm 中每個探針在「所有樣本」中的變異數
probe_variances <- apply(myNorm, 1, var, na.rm = TRUE)

# 2. 設定門檻：砍掉變異數最低的 50% 探針 (可依後續特徵數量需求改為 0.3 或 0.7)
variance_threshold <- quantile(probe_variances, 0.5, na.rm = TRUE)

# 3. 只保留變異數大於門檻的探針，建立新的過濾矩陣 beta_filtered
keep_probes <- names(probe_variances[probe_variances > variance_threshold])
beta_filtered <- myNorm[keep_probes, ]

# 印出過濾結果檢查
print(paste("過濾前探針數:", nrow(myNorm)))
print(paste("變異數過濾後探針數:", nrow(beta_filtered)))

# =====================================================================

myDMP <- champ.DMP(beta = beta_filtered, pheno = myLoad$pd$Sample_Group, arraytype = "EPIC")

write.csv(myDMP[1], file = str_c(path, "/csv/DMP_result_TC.csv"), quote = F)