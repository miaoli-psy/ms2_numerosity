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
library(mixedpower)
# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
# exp1
data_preprocessed <- read_excel("../../data/ms2_uniform_prolific_1_data/preprocessed_prolific.xlsx")
# exp3
data_preprocessed <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_preprocessed.xlsx")

# separate groups
data_ws04 <- subset(data_preprocessed, winsize == 0.4)
data_ws06 <- subset(data_preprocessed, winsize == 0.6)

# TODO
my_data <- data_ws04
my_data <- data_ws06


# LMM ----------------------------------------------------------------

data_by_subject <- my_data %>%
  group_by(participant,
           protectzonetype,
           winsize,
           numerosity) %>%
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




# my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
# hist(my_data$deviation_score2)

# ID as factor
str(data_by_subject)

# my_data$perceptpairs <- as.factor(my_data$perceptpairs)
data_by_subject$protectzonetype <- as.factor(data_by_subject$protectzonetype)
#my_data$numerosity <- as.factor(my_data$numerosity)


contrasts(data_by_subject$protectzonetype) <- matrix(c(-0.5, 0.5), ncol = 1)
levels(data_by_subject$protectzonetype)

# model exp1
model.lmm <-
  lmer(
    deviation_score_mean ~ protectzonetype +
      (1 + protectzonetype + numerosity|participant),
    data = data_by_subject,
    control = lmerControl(optimizer = "Nelder_Mead") # use a different optimizer 
  )


# model exp3
model.lmm <-
  lmer(
    deviation_score_mean ~ protectzonetype +
      (1 + protectzonetype|participant),
    data = data_by_subject,
    REML = FALSE) 


summary(model.lmm)


#  post-hoc comparison
emms <- emmeans(
  model.lmm,
  list(pairwise ~ protectzonetype),
  adjust = "tukey"
)

summary(emms, infer = TRUE)


# simulation

# winsize 0.4, protectzonetype power reach  for ;
# winsize 0.6, protectzonetype power
power <- mixedpower(model = model.lmm, data = data_by_subject,
                    fixed_effects = c("protectzonetype", "numerosity"),
                    simvar = "participant", steps = c(10, 20, 30),
                    critical_value = 2)
# fix effect r2

# r.squaredGLMM(model.lm)
# https://www.rdocumentation.org/packages/r2glmm/versions/0.1.2/topics/r2beta
# https://stats.stackexchange.com/questions/453758/differences-in-proportion-of-variance-explained-by-mumin-and-r2glmm-packages-usi
# r2beta may have error

# model R2
# r2beta(model.lm, method = 'kr', partial = TRUE)

# an APA style table: https://cran.r-project.org/web/packages/sjPlot/vignettes/tab_mixed.html
tab_model(model.lmm, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)

# # posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
# emmeans_res <- emmeans(
#   alignment_con.model_random_slope,
#   list(pairwise ~ protectzonetype * numerosity),
#   adjust = "tukey"
# )
# 
# print(emmeans_res)


# summary(glht(alignment_con.model_random_slope3, linfct=mcp(numerosity ="Tukey")))

