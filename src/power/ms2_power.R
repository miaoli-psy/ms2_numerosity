library(tidyverse)
library(lme4)
library(mixedpower)

# set working path
setwd("D:/OneDrive/projects/ms2_numerosity/data/")

# Exp1-------------------------------------------------------------------------

data_e1 <- readxl::read_excel(path = file.choose())

data_e1_ws04 <- subset(data_e1, winsize == 0.4)
data_e1_ws06 <- subset(data_e1, winsize == 0.6)

# TODO

my_data <- data_e1_ws04
# my_data <- data_e1_ws06

str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$numerosity<- as.integer(my_data$numerosity)


model.e1 <- lmer(deviation_score ~ protectzonetype + 
                   (1|participant) +
                   (1|numerosity),
                 data = my_data, REML = FALSE)

summary(model.e1)


power <- mixedpower(model = model.e1, data = my_data,
                    fixed_effects = c("protectzonetype", "numerosity"),
                    simvar = "participant", steps = c(10, 15, 20, 25, 30),
                    critical_value = 2)


# Exp2-------------------------------------------------------------------------

data_e2 <- readxl::read_excel(path = file.choose())

str(data_e2)

data_e2$protectzonetype <- as.factor(data_e2$protectzonetype)
data_e2$winsize <- as.factor(data_e2$winsize)
data_e2$numerosity <- as.integer(data_e2$numerosity)


# the other fixed factor could be either winsize or numerosity
model.e2 <- lmer(deviation_score ~ protectzonetype + 
                   numerosity +
                   (1|participant),
                 data = data_e2, REML = FALSE)

power <- mixedpower(model = model.e2, data = data_e2,
                    fixed_effects = c("protectzonetype", "numerosity"),
                    simvar = "participant", steps = c(10, 15, 20, 25, 30),
                    critical_value = 2)

# Exp3-------------------------------------------------------------------------

data_e3 <- readxl::read_excel(path = file.choose())

data_e3_ws04 <- subset(data_e3, winsize == 0.4)
data_e3_ws06 <- subset(data_e3, winsize == 0.6)

my_data3 <- data_e3_ws04
# my_data3 <- data_e3_ws06

str(my_data3)

my_data3$protectzonetype <- as.factor(my_data3$protectzonetype)
my_data3$numerosity<- as.integer(my_data3$numerosity)


model.e3 <- lmer(deviation_score ~ protectzonetype + 
                   (1|participant) +
                   (1|numerosity),
                 data = my_data3, REML = FALSE)

power <- mixedpower(model = model.e3, data = my_data3,
                    fixed_effects = c("protectzonetype", "numerosity"),
                    simvar = "participant", steps = c(10, 15, 20, 25, 30),
                    critical_value = 2)


# Exp4--------------------------------------------------------------------------

data_e4 <- readxl::read_excel(path = file.choose())


str(data_e4)

data_e4$protectzonetype <- as.factor(data_e4$protectzonetype)
data_e4$winsize <- as.factor(data_e4$winsize)
data_e4$contrast <- as.factor(data_e4$contrast)


model.e4 <- lmer(deviation_score ~ protectzonetype + 
                   winsize +
                   contrast +
                   (1|participant) +
                   (1|numerosity),
                 data = data_e4, REML = FALSE)


power <- mixedpower(model = model.e4, data = data_e4,
                    fixed_effects = c("protectzonetype", "contrast", "winsize"),
                    simvar = "participant", steps = c(10, 15, 20, 25, 30),
                    critical_value = 2)
