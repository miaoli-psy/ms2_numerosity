import os
import pandas as pd

from src.commons.process_dataframe import keep_valid_columns, change_col_value_type, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value, get_mean, get_std
from src.commons.process_number import get_deviation, get_percent_change
from src.constants.ms2_uniform_prolific_1_constants import KEEP_COLS
from src.preprocess.sub.get_data2analysis import drop_df_rows_according2_one_col

if __name__ == '__main__':
    write_to_excel = False
    # read data
    PATH_DATA = "../../data/ms2_uniform_prolific_1_data/raw/"
    dir_list = os.listdir(PATH_DATA)
    df_list_all = [pd.read_csv(PATH_DATA + file) for file in dir_list]

    # preprocess
    df_list = list()
    for df in df_list_all:
        # keep useful clos
        df = keep_valid_columns(df = df, kept_columns_list = KEEP_COLS)

        # drop practice trials
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

        df_list.append(df)

    # drop participants more than 5% of invalid trials
    # remove pp 12 data: only 311 valid trials out of 330 trials
    df_list.pop(2)

    # add deviation score col
    for df in df_list:
        insert_new_col_from_two_cols(df, "responseN", "numerosity", "deviation_score", get_deviation)
        insert_new_col_from_two_cols(df, "deviation_score", "numerosity", "percent_change", get_percent_change)

    # check subitizing results
    # take subitizing trials out
    subitizing_df_list = list()
    for df in df_list:
        sub_df = df.loc[df["numerosity"] <= 4]
        subitizing_df_list.append(sub_df)

    # 30 subitizing trials (only keep participant has 28, 29 and 30 correct)
    correct_trial_list = list()
    for sub_df in subitizing_df_list:
        correct_trial_list.append((sub_df["deviation_score"] == 0).sum())

    # removed index
    index_list = list()
    for i, n_correct in enumerate(correct_trial_list):
        if n_correct < 28:
            index_list.append(i)

    # removed participant performance not more than 90%
    df_list = [df for i, df in enumerate(df_list) if i not in index_list]

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

    # remove redundant col
    df_data = df_data.drop(["is_num"], axis = 1)

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

    df_data_prepro = pd.concat(prepro_df_list, ignore_index = True)

    if write_to_excel:
        df_data_prepro.to_excel("preprocessed_prolific.xlsx")





