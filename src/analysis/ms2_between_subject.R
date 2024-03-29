# libraries
library(readxl)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(emmeans)
library(sjstats)
library(lme4)
library(lmerTest)
library(MuMIn)
library(multcomp)
library(nlme)
library(r2glmm)
library(ggplot2)
library(ggthemes)
library(svglite)
library(sjPlot)
library(dplyr)

# prepare -----------------------------------------------------------------

# set working path
setwd("D:/OneDrive/projects/numerosity_exps/src/stat_tests/")

# read data
data1 <- read_excel("../../data/ms2_uniform_prolific_1_data/preprocessed_prolific.xlsx")
data2 <- read_excel("../../data/ms2_triplets_4_data/preprocessed_triplets_4.xlsx")
data3 <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_preprocessed.xlsx")
data4 <- read_excel("../../data/ms2_uniform_mix_3_data/preprocessed_uniform_mix_3.xlsx")

# check col names
colnames(data1)
colnames(data2)
colnames(data3)
colnames(data4)

col_to_keep_data <- c("winsize", "participant", "deviation_score", "protectzonetype",
                       "numerosity", "percent_change")

col_to_keep_data4 <- c("winsize", "participant", "deviation_score", "protectzonetype",
                       "numerosity", "percent_change", "contrast")

# some clean
data1 <- subset(data1, select = col_to_keep_data)
data2 <- subset(data2, select = col_to_keep_data)
data3 <- subset(data3, select = col_to_keep_data)
# col contrast should be kept
data4 <- subset(data4, select = col_to_keep_data4)


# assign exp number
data1$expN <- 'exp1'
data2$expN <- 'exp2'
data3$expN <- 'exp3'
data4$expN <- 'exp4'

data1$contrast <- 'uniform'
data2$contrast <- 'uniform'
data3$contrast <- 'mix'

data4$winsize <- as.character(data4$winsize)


data <-bind_rows(data1, data2, data3, data4)

# if there is overlap with participantsN

data <- data %>% 
  mutate(participant2 = paste0(expN, participant))

# --compare exp1 and 2 (all black dics, check the impact of numerosity range---
# --------------------------------------------------------------------------
data1_2 = subset(data, expN %in% c("exp1", "exp2"))

# arrange data for the LMM
# here group_by should not include winsize, as winsize is a with-subject factor
# for exp2
data_by_participant <- data1_2 %>%
  group_by(participant2, expN, protectzonetype) %>%
  summarise(
    deviation_score = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )

# write.csv(data_by_participant, "data.csv")

# visualization


# subject

bxp <- ggboxplot(data = data1_2,
                 x = "expN",
                 y = "deviation_score",
                 color = "protectzonetype") 

print(bxp)



# as factor

data1_2$expN <- as.factor(data1_2$expN)
data1_2$protectzonetype <- as.factor(data1_2$protectzonetype)

# dummy coding only to take the intercept:-4.6000 
lmm.model <- lmer(
  deviation_score ~ protectzonetype + expN +
    (1 + protectzonetype | participant2),
  data = data1_2,
  REML = FALSE
)
summary(lmm.model)

emm <- emmeans(lmm.model, ~  expN)


# ------compare exp1 and 3 (1 extra disc in the protection zone)-----
# -------------------------------------------------------------------
data1_3 = subset(data, expN %in% c("exp1", "exp3"))

# new col for between experiment index
# i.e., 4 conditions for 4 experiments
data1_3 <- data1_3 %>% 
  mutate(expN2 = paste0(expN, winsize))

# arrange data for the LMM
data_by_participant <- data1_3 %>%
  group_by(participant2,  expN2, protectzonetype) %>%
  summarise(
    deviation_score = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )

# visualization

# TODO
dv <- "deviation_score"


# subject

bxp <- ggboxplot(data = data1_3,
                 x = "winsize",
                 y = dv,
                 color = "protectzonetype") +
  facet_wrap(~expN2, ncol = 4, scale = "free_x")

print(bxp)


# as factor
data1_3$winsize <- as.factor(data1_3$winsize)
data1_3$expN <- as.factor(data1_3$expN)
data1_3$expN2 <- as.factor(data1_3$expN2)
data1_3$protectzonetype <- as.factor(data1_3$protectzonetype)

# sum coding
# intercept --> grand mean
contrasts(data1_3$expN2) = contr.sum(4)


# converged model
lmm.model <- lmer(
  deviation_score ~ protectzonetype + expN2 +
    (1 + protectzonetype| participant),
  data = data1_3,
  REML = FALSE
)
summary(lmm.model)



# ------compare exp3 and 4
# -------------------------------------------------------------------
data3_4 = subset(data, expN %in% c("exp4", "exp3"))


# arrange data for the LMM
data_by_participant <- data3_4 %>%
  group_by(participant2, expN, protectzonetype) %>%
  summarise(
    deviation_score = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )


# as factor
data3_4$expN <- as.factor(data3_4$expN)
data3_4$protectzonetype <- as.factor(data3_4$protectzonetype)


# converged model
lmm.model <- lmer(
  deviation_score ~ protectzonetype + expN +
    (1 + protectzonetype| participant),
  data = data3_4,
  REML = FALSE
)
summary(lmm.model)

emm <- emmeans(lmm.model, ~  expN)
