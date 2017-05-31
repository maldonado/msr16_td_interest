statNumOfLinking <- function(data){
  num_all <- nrow(data)
  num_v1 <- sum(data$CountInput_v1 != -1)
  num_v2 <- sum(data$CountInput_v2 != -1)
  num_v1_v2 <- sum((data$CountInput_v1 != -1 & data$CountInput_v2 != -1))
  
  cat(sprintf("Num Of Tech Debt : %d\n", num_all))
  cat(sprintf("  Per of linking to v1 : %.2f%% (=%d/%d)\n",num_v1/num_all*100, num_v1,num_all))
  cat(sprintf("  Per of linking to v2 : %.2f%% (=%d/%d)\n",num_v2/num_all*100, num_v2,num_all))
  cat(sprintf("  Per of linking to all: %.2f%% (=%d/%d)\n",num_v1_v2/num_all*100, num_v1_v2,num_all))
}

# setwd("/Users/kamei/Research/techdebt/msr16_td_interest/")
data <- read.csv("./datasets/CSV/interest.ssv", sep="#",  quote = "")
#data <- read.csv("./datasets/CSV/interest_laptop.ssv", sep="#",  quote = "")
#data <- read.csv("./datasets/CSV/temp_interest.ssv", sep="#",  quote = "")
cat(sprintf("Num Of Raw Data : %d\n", nrow(data)))

# (Step 1) choose one of duplicated method and version name
method_and_version_name <- paste(data$Method_Signature, data$v1, sep="")
data.s1 <- data[!duplicated(method_and_version_name), ]
statNumOfLinking(data.s1)

# (Step 2) only use technical debt including metrics
data.s2 <- data.s1[(data.s1[, "CountInput_v1"] != -1 & data.s1[, "CountInput_v2"] != -1), ]

# only use technical debt including non 0 for division
data.CountInput <- data.s2[(data.s2[,"CountInput_v1"] != 0), ]
data.CountInput.all <- cbind(data.CountInput, interest = ((data.CountInput$CountInput_v2 - data.CountInput$CountInput_v1) / data.CountInput$CountInput_v1 * 100))
data.CountInput.positive <- subset(data.CountInput.all, data.CountInput.all$CountInput_v2 > data.CountInput.all$CountInput_v1)
data.CountInput.negative <- subset(data.CountInput.all, data.CountInput.all$CountInput_v2 < data.CountInput.all$CountInput_v1)

data.CountLine <- data.s2[(data.s2[,"CountLine_v1"] != 0), ]
data.CountLine.all <- cbind(data.CountLine, interest = ((data.CountLine$CountLine_v2 - data.CountLine$CountLine_v1) / data.CountLine$CountLine_v1 * 100))
data.CountLine.positive <- subset(data.CountLine.all, data.CountLine.all$CountLine_v2 > data.CountLine.all$CountLine_v1)
data.CountLine.negative <- subset(data.CountLine.all, data.CountLine.all$CountLine_v2 < data.CountLine.all$CountLine_v1)
