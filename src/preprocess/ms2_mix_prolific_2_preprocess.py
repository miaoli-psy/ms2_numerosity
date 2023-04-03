import os

import pandas as pd
import numpy as np

from src.commons.process_dataframe import keep_valid_columns, change_col_value_type, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value, get_std, get_mean
from src.commons.process_number import get_percent_change, get_deviation
from src.constants.ms2_mix_2_constants import KEEP_COLS
from src.preprocess.sub.get_data2analysis import drop_df_rows_according2_one_col

if __name__ == '__main__':
    write_to_excel = False
    PATH = "../../data/ms2_mix_prolific_2_data/raw/"
    dir_list = os.listdir(PATH)

    df_list_all = [pd.read_csv(PATH + file) for file in dir_list if file.endswith(".csv")]

    # preprocess
    df_list = list()
    for df in df_list_all:
        # keep useful cols
        df = keep_valid_columns(df = df, kept_columns_list = KEEP_COLS)

        # drop practice and ref trials
        df = df.dropna(subset = ["trials.thisN"])

        # remove spaces
        if df["responseN"].dtypes == "object":
            df["responseN"] = df["responseN"].str.strip()
            # remove non numeric responses
            df["is_num"] = df["responseN"].str.isnumeric()
            drop_index = df[df["is_num"] == False].index
            df.drop(drop_index, inplace = True)

            # change responseN to float
            change_col_value_type(df, "responseN", float)

            # remove the "is_num" col
            df = df.drop(columns = ["is_num"])
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

    # 30 subitizing trials per participants: remove participant subitizing less than 90% correct
    # 13 participants were removed
    correct_trial_list = list()
    for sub_df in subitizing_df_list:
        correct_trial_list.append((sub_df["deviation_score"] == 0).sum())

    remove_indices = [idx for idx, element in enumerate(correct_trial_list) if element < 27]
    print("%s  out of %s participants were removed, failing the subitizing check" % (len(remove_indices), len(correct_trial_list)))

    for ele in sorted(remove_indices, reverse = True):
        del df_list[ele]

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

    # see trials number before removing any trials
    df_data = pd.concat(df_list_prepro, ignore_index = True)

    n_discs = [34, 36, 38, 40, 42, 44,
              54, 56, 58, 60, 62, 64]

    df_list_by_num = [get_sub_df_according2col_value(df_data, "numerosity", n) for n in n_discs]
    prepro_df_list = list()
    for sub_df in df_list_by_num:
        lower_bondary = get_mean(sub_df, "responseN") - 3 * get_std(sub_df, "responseN")
        upper_bondary = get_mean(sub_df, "responseN") + 3 * get_std(sub_df, "responseN")
        new_sub_df = drop_df_rows_according2_one_col(sub_df, "responseN", lower_bondary, upper_bondary)
        prepro_df_list.append(new_sub_df)

    # 1.13% trials were removed
    df_data_prepro = pd.concat(prepro_df_list, ignore_index = True)

    # check participant/ average age
    df_by_participant = df_data_prepro.groupby(by = ["participant", "winsize"], dropna = False).mean()

    table1 = pd.pivot_table(df_data_prepro, values = ['age'], columns = ["winsize"], aggfunc = {"age": np.mean})
    table2 = pd.pivot_table(df_data_prepro, values = ['age'], columns = ["winsize"], index = ["participant"], aggfunc = {"age": np.mean})
    table2 = pd.pivot_table(df_data_prepro, values = ['age'], columns = ["winsize", "sex"], index = ["participant"])


    if write_to_excel:
        df_data_prepro.to_excel("ms2_mix_2_preprocessed.xlsx")