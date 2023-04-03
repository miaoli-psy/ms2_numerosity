# -*- coding: utf-8 -*- 
"""
Project: CrowdingNumerosityGit
Creator: Miao
Create time: 2021-03-02 15:41
IDE: PyCharm
Introduction:
"""
import pandas as pd


def drop_df_nan_rows_according2cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df = df.dropna(subset = cols)
    return df


def drop_df_rows_according2_one_col(df: pd.DataFrame, col_name: str, lowerbondary: float,
                                    upperbondary: float) -> pd.DataFrame:

    df = df[(df[col_name] < upperbondary) & (df[col_name] > lowerbondary)]
    return df


def __cal_std_of_one_col(df: pd.DataFrame, col_name: str) -> float:
    std = df[col_name].std()
    return std


def __cal_mean_of_one_col(df: pd.DataFrame, col_name: str) -> float:
    mean = df[col_name].mean()
    return mean


def get_col_boundary(df: pd.DataFrame, col_name: str, n_std = 3) -> tuple:
    mean = __cal_mean_of_one_col(df, col_name)
    std = __cal_std_of_one_col(df, col_name)
    return mean - n_std * std, mean + n_std * std