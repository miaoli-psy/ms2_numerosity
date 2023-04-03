import os
import pandas as pd

from src.commons.process_dataframe import keep_valid_columns, change_col_value_type, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value, get_mean, get_std
from src.commons.process_number import get_deviation, get_percent_change
from src.constants.ms2_triplets_4_constants import KEEP_COLs
from src.preprocess.sub.get_data2analysis import drop_df_rows_according2_one_col


def pre_process_indi_data(df):
    # drop reference and practice trials
    df = df.drop([i for i in range(0, 8)])
    # drop nan in responseN
    df = df.dropna(subset=['responseN'])
    return df


if __name__ == '__main__':
    to_excel = False
    # read data
    PATH = "../../data/ms2_triplets_4_data/rawdata/"
    # list raw data files
    files = os.listdir(PATH)
    df_list_all = [pd.read_csv(PATH + file) for file in files if file.endswith("csv")]

    # preprocess
    df_list = list()
    for df in df_list_all:
        # keep useful cols
        df = keep_valid_columns(df, KEEP_COLs)
        df = pre_process_indi_data(df)
        df_list.append(df)

    # add deviation score and percent change
    for df in df_list:
        insert_new_col_from_two_cols(df, "responseN", "numerosity", "deviation_score", get_deviation)
        insert_new_col_from_two_cols(df, "deviation_score", "numerosity", "percent_change", get_percent_change)

    # check subitizing results
    subitizing_df_list = list()
    for df in df_list:
        sub_df = df.loc[df["numerosity"] <=4]
        subitizing_df_list.append(sub_df)

    # 36 subitizing trials per participant: all participants are above 90%, the worst 34 out of 36 are correct
    correct_trial_list = list()
    for sub_df in subitizing_df_list:
        correct_trial_list.append((sub_df["deviation_score"] == 0).sum())

    # remove subitizing trials
    df_list_t1 = list()
    for df in df_list:
        df_list_t1.append(df.loc[df["numerosity"] > 4])

    min_res = 10
    max_res = 150
    df_list_prepro = list()
    for df in df_list_t1:
        df_list_prepro.append(drop_df_rows_according2_one_col(df, "responseN", min_res, max_res))

    # concat all participant
    df_data = pd.concat(df_list_prepro)

    # keep data within 3 sd
    n_discs = [51, 54, 57, 60, 63, 66, 69, 72,
               78, 81, 84, 87, 90, 93, 96, 99]

    df_list_by_num = [get_sub_df_according2col_value(df_data, "numerosity", n) for n in n_discs]
    prepro_df_list = list()
    for sub_df in df_list_by_num:
        lower_bondary = get_mean(sub_df, "responseN") - 3 * get_std(sub_df, "responseN")
        upper_bondary = get_mean(sub_df, "responseN") + 3 * get_std(sub_df, "responseN")
        new_sub_df = drop_df_rows_according2_one_col(sub_df, "responseN", lower_bondary, upper_bondary)
        prepro_df_list.append(new_sub_df)

    df_data_prepro = pd.concat(prepro_df_list, ignore_index = True)
    # 3.71% of trials were removed
    df_full = pd.concat(df_list_t1, ignore_index = True)

    if to_excel:
        df_data_prepro.to_excel("preprocessed_triplets_4.xlsx", index = False)

