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
data_preprocessed <- read_excel("../../data/ms2_uniform_mix_3_data/preprocessed_uniform_mix_3.xlsx")

# check average age

check_age <- data_preprocessed %>% 
  group_by(participant) %>% 
  summarise_at(vars(age),list(age = mean))

check_age <- check_age %>% 
  summarise_at(vars(age), list(age = mean))


# Visualization------------------------------------------------------

# TODO
dv <- "deviation_score"

# subject
bxp <- ggboxplot(data = data_preprocessed,
                 x = "participant",
                 y = dv,
                 color = "protectzonetype") +
  facet_wrap( ~ winsize * contrast_full, nrow = 2, scale = "free_x")

print(bxp)

# clustering level
bxp2 <- ggboxplot(data = data_preprocessed,
                  x = "perceptpairs",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize * contrast_full, nrow = 2, scale = "free_x")

print(bxp2)

# numerosity

bxp3 <- ggboxplot(data = data_preprocessed,
                  x = "numerosity",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize * contrast_full, nrow = 2, scale = "free_x")

print(bxp3)


# TODO
my_data <- data_preprocessed

hist(my_data$deviation_score)

# LMM winsize as a fixed factor-------------------------------------------

my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
hist(my_data$deviation_score2)


str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$winsize <- as.factor(my_data$winsize)
my_data$contrast <- as.factor(my_data$contrast)


# not converged (~80min)
full_model <- lmer(deviation_score2 ~ protectzonetype * winsize * contrast + 
                     (1 + contrast + winsize + protectzonetype|participant), 
                   data = my_data, REML = FALSE)

summary(full_model)
rePCA(full_model)
summary(rePCA(full_model))


# converged
model.lm <- lmer(deviation_score2 ~ protectzonetype * winsize * contrast +
                   (1 +  protectzonetype|participant),
                 data = my_data, REML = FALSE)
summary(model.lm)

model.lm2 <- lmer(deviation_score2 ~ protectzonetype * winsize * contrast + 
                    (1 |participant), data = my_data, REML = FALSE)

summary(model.lm2)

anova(model.lm, model.lm2)


emmip(model.lm, protectzonetype ~ winsize | contrast)


# 3-way interaction

model.reduced <- lmer(deviation_score2 ~ protectzonetype * winsize + 
                        winsize * contrast+ 
                        contrast * protectzonetype+
                        (1 + protectzonetype|participant), data = my_data, REML = FALSE)

summary(model.reduced)
anova(model.reduced)
anova(model.lm, model.reduced)

emmip(model.lm, contrast ~ winsize)


# 2-way interaction

model.reduced2 <- lmer(deviation_score2 ~ winsize * contrast+ 
                         winsize * protectzonetype+
                         (1 + protectzonetype|participant), data = my_data, REML = FALSE)

anova(model.reduced, model.reduced2)


# alignment condition/numerosity/contrast polarity
model.reducedlm <- lmer(deviation_score2 ~ nest_numerosity + contrast + protectzonetype +
                          (1 + protectzonetype|participant), data = my_data, REML = FALSE)

summary(model.reducedlm)

model.null <- lmer(deviation_score2 ~ protectzonetype + contrast + (1 + protectzonetype|participant),
                   data = my_data, REML = FALSE)


anova(model.reducedlm, model.null)



# contrast: post-hoc comparison
emms <- emmeans(
  model.lm,
  list(pairwise ~  contrast|winsize),
  adjust = "tukey"
)

emms$emmeans
summary(emms, infer = TRUE)


emms2 <- emmeans(
  model.lm,
  list(pairwise ~ protectzonetype|winsize),
  adjust = "tukey"
)

summary(emms2, infer = TRUE)


# check main effect with likely radiohood test

model.tem <- lmer(deviation_score2 ~ protectzonetype + winsize + contrast +
                    (1 + protectzonetype|participant), data = my_data, REML = FALSE)


model.tem2 <- lmer(deviation_score2 ~ winsize + contrast +
                    (1 + protectzonetype|participant), data = my_data, REML = FALSE)

anova(model.tem, model.tem2)

emms3 <- emmeans(
  model.lm,
  list(pairwise ~ protectzonetype),
  adjust = "tukey"
)

summary(emms3, infer = TRUE)

# LMM nested numerosity as a fixed factor-------------------------------------------

my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
hist(my_data$deviation_score2)


str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$winsize <- as.factor(my_data$winsize)
my_data$numerosity <- as.factor(my_data$numerosity)
my_data$contrast <- as.factor(my_data$contrast)

# each small and large numerosity ranges only occurs under small and large winszie:
# so we created a nested numerosity factor
my_data <- within(my_data, nest_numerosity <- factor(winsize:numerosity))


# not converged (~80min)
full_model <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity * contrast + 
                     (1 + contrast + nest_numerosity + protectzonetype|participant), 
                   data = my_data, REML = FALSE)

summary(full_model)
rePCA(full_model)
summary(rePCA(full_model))


# converged
model.lm <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity * contrast +
                   (1 +  protectzonetype|participant),
                 data = my_data, REML = FALSE)
summary(model.lm)

model.lm2 <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity * contrast + 
                    (1 |participant), data = my_data, REML = FALSE)

summary(model.lm2)

anova(model.lm, model.lm2)


emmip(model.lm, protectzonetype ~ nest_numerosity | contrast)


# 3-way interaction

model.reduced <- lmer(deviation_score2 ~ protectzonetype * nest_numerosity + 
                        nest_numerosity * contrast+ 
                        contrast * protectzonetype+
                        (1 + protectzonetype|participant), data = my_data, REML = FALSE)

summary(model.reduced)
anova(model.reduced)
anova(model.lm, model.reduced)

emmip(model.lm, protectzonetype ~ numerosity)


# 2-way interaction

model.reduced2 <- lmer(deviation_score2 ~ nest_numerosity * contrast+ 
                        nest_numerosity * protectzonetype+
                        (1 + protectzonetype|participant), data = my_data, REML = FALSE)

anova(model.reduced, model.reduced2)


# alignment condition/numerosity/contrast polarity
model.reducedlm <- lmer(deviation_score2 ~ nest_numerosity + contrast + protectzonetype +
                          (1 + protectzonetype|participant), data = my_data, REML = FALSE)

summary(model.reducedlm)

model.null <- lmer(deviation_score2 ~ protectzonetype + contrast + (1 + protectzonetype|participant),
                   data = my_data, REML = FALSE)


anova(model.reducedlm, model.null)


# contrast: post-hoc comparison
emms <- emmeans(
  model.lm,
  list(pairwise ~ protectzonetype * contrast|nest_numerosity),
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


