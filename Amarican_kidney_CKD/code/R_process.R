#install.packages("BiocManager")
#BiocManager::install("ChAMP")

library("ChAMP")

library(stringr)

path <- file.path(getwd(), "..")

my_pd <- read.csv(str_c(path, "/processing_data/Sample_sheet.csv"))

# Basename不動，用 stringr 套件拆解，並新增兩個欄位
# 用底線 "_" 切割成3等份 (樣本_ID_位置)
split_basename <- str_split_fixed(my_pd$Basename, "_", 3)

# 將切割出的第2部分存成 Sentrix_ID，第3部分存成 Sentrix_Position
my_pd$Sentrix_ID <- split_basename[, 2]
my_pd$Sentrix_Position <- split_basename[, 3]

# 3. 覆蓋原本的 Sample_sheet.csv (記得 quote = FALSE, row.names = FALSE)
write.csv(my_pd, file = str_c(path, "/processing_data/Sample_sheet.csv"), quote = FALSE, row.names = FALSE)

myLoad <- champ.load(str_c(path,"/processing_data"), arraytype = "EPIC", SampleCutoff = 0.2)

myNorm <- champ.norm(beta = myLoad$beta, plotBMIQ = FALSE, cores = 10 , arraytype = "EPIC")

write.csv(myNorm, file = str_c(path, "/csv/", "all_beta_normalized.csv"), quote = F, row.names = T)

myDMP <- champ.DMP(beta = myNorm, pheno = myLoad$pd$Sample_Group, arraytype = "EPIC")

write.csv(myDMP[1], file = str_c(path, "/csv/DMP_result_TC.csv"), quote = F)