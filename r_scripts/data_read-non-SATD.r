data <- read.csv("./datasets/CSV/non_satd_interest.ssv", sep="#")

# (Step 1) choose one of duplicated method and version name
method_and_version_name <- paste(data$Signature, data$Intro, sep="")
data.s1 <- data[!duplicated(method_and_version_name), ]

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
