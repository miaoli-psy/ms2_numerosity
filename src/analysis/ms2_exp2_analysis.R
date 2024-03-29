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
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_preprocessed <- read_excel("../../data/ms2_triplets_4_data/preprocessed_triplets_4.xlsx")

# check avg age
df <- data_preprocessed %>% 
  summarise(mean_age = mean(age),
            sd = sd(age),
            range = paste(min(age), "-", max(age)))


# Visualization------------------------------------------------------

# TODO
dv <- "deviation_score"
# dv <- "percent_change_mean"

# subject
bxp <- ggboxplot(data = data_preprocessed,
                 x = "participant",
                 y = dv,
                 color = "protectzonetype") +
  facet_wrap( ~ winsize, nrow = 2, scale = "free_x")

print(bxp)

# numerosity

bxp3 <- ggboxplot(data = data_preprocessed,
                  x = "numerosity",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")

print(bxp3)



hist(my_data$deviation_score)


# LMM ----------------------------------------------------------------
  
data_by_subject <- data_preprocessed %>%
  group_by(participant,
           protectzonetype,
           winsize) %>%
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


# TODO
my_data <- data_by_subject

#my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
#hist(my_data$deviation_score2)

str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$winsize <- as.factor(my_data$winsize)

contrasts(my_data$protectzonetype) <- matrix(c(-0.5, 0.5), ncol = 1)
contrasts(my_data$winsize) <- matrix(c(-0.5, 0.5), ncol = 1)

levels(my_data$protectzonetype)
levels(my_data$winsize)

model.lmm <-
  lmer(
    deviation_score_mean ~ protectzonetype * winsize +
      (1 + protectzonetype + winsize|participant),
    data = my_data,
    control = lmerControl(optimizer = "Nelder_Mead") # use a different optimizer 
  )

summary(model.lmm)

# use this model
model.lmm2 <-
  lmer(
    deviation_score_mean ~ protectzonetype + winsize +
      (1 + protectzonetype + winsize|participant),
    data = my_data,
    control = lmerControl(optimizer = "Nelder_Mead") # use a different optimizer 
  )

summary(model.lmm2)

anova(model.lmm, model.lmm2)
emmip(model.lmm2, protectzonetype ~ winsize)



# contrast: post-hoc comparison
emms <- emmeans(
  model.lmm2,
  list(pairwise ~ protectzonetype),
  adjust = "tukey"
)

summary(emms, infer = TRUE)



r2beta(model.lmm2, method = 'kr', partial = TRUE)

tab_model(model.lmm2, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)


