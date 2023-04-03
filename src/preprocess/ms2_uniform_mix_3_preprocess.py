import os

import pandas as pd

from src.commons.process_dataframe import keep_valid_columns, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value, get_mean, get_std, insert_new_col
from src.commons.process_number import get_deviation, get_percent_change
from src.constants.ms2_mix_uniform_3_constants import KEEP_COLs
from src.preprocess.sub.get_data2analysis import drop_df_rows_according2_one_col


def convert_blockOrdertocontrast1(blockOrder: str):
    if blockOrder == "c4_mix.xlsx" or blockOrder == "c6_mix.xlsx":
        return "mix"
    else:
        return "uniform"


def convert_blockOrdertocontrast2(blockOrder: str):
    if blockOrder == "c4_mix.xlsx" or blockOrder == "c6_mix.xlsx":
        return "mix"
    elif blockOrder == "c4_white.xlsx" or blockOrder == "c6_white.xlsx":
        return "white"
    else:
        return "black"


if __name__ == '__main__':
    write_to_excel = False
    # read data
    PATH = "../../data/ms2_uniform_mix_3_data/rawdata/"
    dir_list = os.listdir(PATH)
    df_list_all = [pd.read_csv(PATH + file) for file in dir_list if file.endswith(".csv")]

    # preprocess
    df_list = list()
    for df in df_list_all:
        # keep useful cols
        df = keep_valid_columns(df = df, kept_columns_list = KEEP_COLs)
        # drop practice and ref trials
        df = df.dropna(subset = ["trials.thisN"])
        df_list.append(df)

    # add deviation score and percent change
    for df in df_list:
        insert_new_col_from_two_cols(df, "responseN", "numerosity", "deviation_score", get_deviation)
        insert_new_col_from_two_cols(df, "deviation_score", "numerosity", "percent_change", get_percent_change)

    # check subitizing results
    subitizing_df_list = list()
    for df in df_list:
        sub_df = df.loc[df["numerosity"] <= 4]
        subitizing_df_list.append(sub_df)

    # 72 subitiing trials per participants: all are above 95% correct, the worst, 69 out of 72 correct
    correct_trial_list = list()
    for sub_df in subitizing_df_list:
        correct_trial_list.append((sub_df["deviation_score"] == 0).sum())

    # remove subitizing trials
    df_list_t1 = list()
    for df in df_list:
        df_list_t1.append(df.loc[df["numerosity"] > 4])

    # drop obvious wrong response:
    min_res = 10
    max_res = 128
    df_list_prepro = list()
    for df in df_list_t1:
        df_list_prepro.append(drop_df_rows_according2_one_col(df, "responseN", min_res, max_res))

    # concat all participant
    df_data = pd.concat(df_list_prepro)

    # keep data within 3 sd
    n_discs = [34, 36, 38, 40, 42, 44,
               54, 56, 58, 60, 62, 64]

    df_list_by_num = [get_sub_df_according2col_value(df_data, "numerosity", n) for n in n_discs]
    prepro_df_list = list()
    for sub_df in df_list_by_num:
        lower_bondary = get_mean(sub_df, "responseN") - 3 * get_std(sub_df, "responseN")
        upper_bondary = get_mean(sub_df, "responseN") + 3 * get_std(sub_df, "responseN")
        new_sub_df = drop_df_rows_according2_one_col(sub_df, "responseN", lower_bondary, upper_bondary)
        prepro_df_list.append(new_sub_df)

    # 1.20% trials were removed
    df_data_prepro = pd.concat(prepro_df_list, ignore_index = True)

    insert_new_col(df_data_prepro, "blockOrder", "contrast", convert_blockOrdertocontrast1)
    insert_new_col(df_data_prepro, "blockOrder", "contrast_full", convert_blockOrdertocontrast2)

    if write_to_excel:
        df_data_prepro.to_excel("preprocessed_uniform_mix_3.xlsx", index = False)