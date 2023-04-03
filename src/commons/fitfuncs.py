# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-08 22:31
IDE: PyCharm
Introduction:
"""
from scipy.optimize import curve_fit
from scipy.stats import poisson
import numpy as np


def fit_poisson_cdf(input_np_array) -> float :
    """
    :param input_np_array: 2 columns, first col: x; second col: y
    :return: lambda (float) of cdf poisson fit
    """
    x_val = input_np_array[:, 0]
    y_val = input_np_array[:, 1]
    popt, _ = curve_fit(poisson.cdf, x_val, y_val, p0 = 1)
    return round(popt[0], 4)

