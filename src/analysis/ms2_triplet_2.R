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
  
# TODO
my_data <- data_preprocessed

my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
hist(my_data$deviation_score2)


str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$winsize <- as.factor(my_data$winsize)


# not converged (take about 15 - 20 min to run)
full_model <- lmer(deviation_score2 ~ protectzonetype * winsize + 
                     (1 + winsize + protectzonetype|participant), 
                   data = my_data, REML = FALSE)

summary(full_model)
rePCA(full_model)
summary(rePCA(full_model))


# converged
model.lm <- lmer(deviation_score2 ~ protectzonetype * winsize +
                   (1 +  protectzonetype|participant),
                 data = my_data, REML = FALSE)
summary(model.lm)

model.lm2 <- lmer(deviation_score2 ~ protectzonetype * winsize + 
                    (1 |participant), data = my_data, REML = FALSE)

summary(model.lm2)

anova(model.lm, model.lm2)


emmip(model.lm, protectzonetype ~ winsize)


# interaction

model.reduced <- lmer(deviation_score2 ~ protectzonetype + winsize + 
                        (1 + protectzonetype|participant), data = my_data, REML = FALSE)
summary(model.reduced)
anova(model.reduced)
anova(model.lm, model.reduced)

emmip(model.lm, protectzonetype ~ winsize)


# alignment condition/numerosity
model.null <- lmer(deviation_score2 ~ protectzonetype + (1 + protectzonetype|participant),
                   data = my_data, REML = FALSE)


anova(model.reduced, model.null)


# contrast: post-hoc comparison
emms <- emmeans(
  model.reduced,
  list(pairwise ~ protectzonetyp|winsize),
  adjust = "tukey"
)

emms$emmeans

summary(emms, infer = TRUE)


emms2 <- emmeans(
  model.reduced,
  list(pairwise ~ winsize|protectzonetype),
  adjust = "tukey"
)

summary(emms2, infer = TRUE)


r2beta(model.reduced, method = 'kr', partial = TRUE)

tab_model(model.reduced, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)


# LMM  numerosity  nested factor----------------------------------------------------------------

my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
hist(my_data$deviation_score2)


# TODO
my_data <- data_preprocessed

# each small and large numerosity ranges only occurs under small and large winszie:
# so we created a nested numerosity factor
my_data <- within(my_data, nest_numerosity <- factor(winsize:numerosity))

summary(my_data)

str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$numerosity <- as.factor(my_data$numerosity)
my_data$winsize <- as.factor(my_data$winsize)


# not converged (take about 15 - 20 min to run)
full_model <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity + 
                     (1 + nest_numerosity + protectzonetype|participant), 
                   data = my_data, REML = FALSE)

summary(full_model)
rePCA(full_model)
summary(rePCA(full_model))


# converged
model.lm <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity +
                        (1 +  protectzonetype|participant),
                      data = my_data, REML = FALSE)
summary(model.lm)

model.lm2 <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity + 
                    (1 |participant), data = my_data, REML = FALSE)

summary(model.lm2)

anova(model.lm, model.lm2)


emmip(model.lm, protectzonetype ~ nest_numerosity)

# interaction

model.reduced <- lmer(deviation_score2 ~ protectzonetype + nest_numerosity + 
                        (1 + protectzonetype|participant), data = my_data, REML = FALSE)
summary(model.reduced)
anova(model.reduced)
anova(model.lm, model.reduced)

emmip(model.lm, protectzonetype ~ numerosity)


# alignment condition/numerosity
model.null <- lmer(deviation_score2 ~ protectzonetype + (1 + protectzonetype|participant),
                   data = my_data, REML = FALSE)


anova(model.reduced, model.null)


# contrast: post-hoc comparison
emms <- emmeans(
  model.lm,
  list(pairwise ~ protectzonetype|nest_numerosity),
  adjust = "tukey"
)

summary(emms, infer = TRUE)


emms2 <- emmeans(
  model.lm,
  list(pairwise ~ nest_numerosity|protectzonetype),
  adjust = "tukey"
)

summary(emms2, infer = TRUE)



r2beta(model.reduced, method = 'kr', partial = TRUE)

tab_model(model.reduced, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)


