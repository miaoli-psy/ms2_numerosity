# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-19 21:32
IDE: PyCharm
Introduction:
"""
import os
import pandas as pd


def __get_dataframe_file(data_path: str, filetype: str, filename: str) -> pd.DataFrame:
    if filetype == ".csv":
        df = pd.read_csv(data_path + filename)
    elif filetype == ".xlsx":
        df = pd.read_excel(data_path + filename)
    return df


def merge_all_file2dataframe(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    # list data files
    files = os.listdir(data_path)
    # collect all raw data files
    filenames_list = [file for file in files if file.startswith(filename_prefix) & file.endswith(filetype)]
    # read data
    all_data = pd.DataFrame()
    for filename in filenames_list:
        curr_df = __get_dataframe_file(data_path, filetype, filename)
        all_data = all_data.append(curr_df, sort=True)
    return all_data


if __name__ == "__main__":
    data_path = "../../../data/exp3_data/exp3_pilot_data/rawdata/"
    filename_prefix = "P"
    filetype = ".csv"
    all_df = merge_all_file2dataframe(data_path, filetype, filename_prefix)
