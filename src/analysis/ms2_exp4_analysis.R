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

# prepare -----------------------------------------------------------------

# set working path
setwd("D:/OneDrive/projects/ms2_numerosity/src/analysis/")

# read data
data_preprocessed <- read_excel("../../data/ms2_uniform_mix_3_data/preprocessed_uniform_mix_3.xlsx")

# check average age

check_age <- data_preprocessed %>% 
  group_by(participant) %>% 
  summarise_at(vars(age),list(age = mean))

check_age <- check_age %>% 
  summarise_at(vars(age), list(age = mean))

# arrange data

data_by_subject <- data_preprocessed %>%
  group_by(participant,
           protectzonetype,
           winsize,
           contrast) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
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

#write.csv(data_by_subject, "data.csv")

# TODO
my_data <- data_by_subject

hist(my_data$deviation_score_mean)

# LMM winsize as a fixed factor-------------------------------------------

#my_data$deviation_score_mean <- scale(my_data$deviation_score_mean, center = TRUE, scale = TRUE)
#hist(my_data$deviation_score2)


str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$winsize <- as.factor(my_data$winsize)
my_data$contrast <- as.factor(my_data$contrast)

contrasts(my_data$protectzonetype) <- matrix(c(-0.5, 0.5), ncol = 1)
contrasts(my_data$winsize) <- matrix(c(-0.5, 0.5), ncol = 1)
contrasts(my_data$contrast) <- matrix(c(-0.5, 0.5), ncol = 1)

levels(my_data$protectzonetype)
levels(my_data$contrast)
levels(my_data$winsize)

model.lmm <-
  lmer(
    deviation_score_mean ~  protectzonetype * contrast + winsize +
      (1 + contrast + winsize + protectzonetype |
         participant),
    data = my_data,
    REML = FALSE
  )

summary(model.lmm)

# interaction-style plots
emmip(model.lmm, protectzonetype ~ winsize | contrast)
emmip(model.lmm, protectzonetype ~ contrast | winsize)


# contrast: post-hoc comparison
emms <- emmeans(
  model.lmm,
  list(pairwise ~  protectzonetype),
  adjust = "tukey"
)

emms2 <- emmeans(
  model.lmm,
  list(pairwise ~  contrast),
  adjust = "tukey"
)
summary(emms, infer = TRUE)
summary(emms2, infer = TRUE)

emm <- emmeans(model.lmm, specs = pairwise ~ protectzonetype | contrast * winsize)
pairs(emm)


r2beta(model.lmm, method = 'kr', partial = TRUE)

tab_model(model.lmm, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)


