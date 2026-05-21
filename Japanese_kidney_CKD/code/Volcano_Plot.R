# 如果還沒安裝過這些套件，請先解除下方的註解並執行安裝
# install.packages("readr")
# install.packages("dplyr")
# install.packages("ggplot2")

library(readr)
library(dplyr)
library(ggplot2)

# 讀取資料
dmp_data <- read_csv("../csv/DMP_result_TC.csv")
delta_data <- read_csv("../csv/delta_beta_mean_values.csv")

# 將 dmp_data 的第一欄改名為 CpG_ID
colnames(dmp_data)[1] <- "CpG_ID"
colnames(delta_data)[1] <- "CpG_ID"

# 將 delta_data 的欄位 "0" 改名為 Delta_Beta
colnames(delta_data)[2] <- "Delta_Beta"

# 3. 將兩個檔案根據 CpG_ID 合併 (Inner Join)
merged_data <- inner_join(dmp_data, delta_data, by = "CpG_ID")

# head(merged_data)

# 4. 設定顯著標籤 (用合併出來的 Delta_Beta)
merged_data <- merged_data %>%
  mutate(
    Significance = case_when(
      N_to_C.adj.P.Val < 0.05 & Delta_Beta > 0.2 ~ "Hypermethylated (Up)",
      N_to_C.adj.P.Val < 0.05 & Delta_Beta < -0.2 ~ "Hypomethylated (Down)",
      #N_to_C.P.Value < 0.05 & Delta_Beta > 0.2 ~ "Hypermethylated (Up)",
      #N_to_C.P.Value < 0.05 & Delta_Beta < -0.2 ~ "Hypomethylated (Down)",
      TRUE ~ "Not Significant"
    )
  )

# 5. 畫出火山圖
ggplot(merged_data, aes(x = Delta_Beta, y = -log10(N_to_C.adj.P.Val), color = Significance)) +
  geom_point(alpha = 0.8, size = 1.5) +  
  scale_color_manual(values = c("Hypermethylated (Up)" = "red", 
                                "Hypomethylated (Down)" = "blue", 
                                "Not Significant" = "grey")) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "black") +
  geom_vline(xintercept = c(-0.2, 0.2), linetype = "dashed", color = "black") +
  theme_minimal() +
  labs(
    title = "Volcano Plot of CKD Methylation",
    x = "Delta Beta",
    y = "-log10(Adjusted P-Value)"
  ) +
  theme(legend.title = element_blank())

# 儲存成 PNG 檔
ggsave(filename = "../CKD_Volcano_Plot.png", 
       width = 8,       # 圖片寬度
       height = 6,      # 圖片高度
       dpi = 300)       # 解析度 300 dpi 是印刷和論文的標準要求

# 儲存成 PDF 檔
ggsave(filename = "../CKD_Volcano_Plot.pdf", 
       width = 8, 
       height = 6)