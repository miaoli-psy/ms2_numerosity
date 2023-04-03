import pandas as pd

from src.commons.process_dataframe import rename_df_col, insert_new_col, insert_new_col_from_two_cols
from src.commons.process_number import cal_SEM


def get_percent_triplets(percentpairs):
    if percentpairs == 1:
        return 0
    elif percentpairs == 0.75:
        return 0.25
    elif percentpairs == 0.5:
        return 0.5
    elif percentpairs == 0.25:
        return 0.75
    elif percentpairs == 0:
        return 1
    else:
        raise Exception(f"percentpair {percentpairs} is unexpected")


def get_samplesize(winsize):
    if winsize == 0.4:
        return 34
    else:
        return 32


if __name__ == '__main__':
    write_to_excel = False
    # read data
    PATH = "../data/ms2_uniform_prolific_1_data/"
    DATA = "preprocessed_prolific.xlsx"
    data = pd.read_excel(PATH + DATA)
    # process the cols
    rename_df_col(data, "Unnamed: 0", "n")
    # convert percentpairs to percent_triplets
    insert_new_col(data, "perceptpairs", "percent_triplets", get_percent_triplets)

    dv = "deviation_score"
    dv2 = "percent_change"

    indv = "numerosity"
    indv2 = "protectzonetype"
    indv3 = "winsize"
    indv4 = "percent_triplets"
    indv5 = "perceptpairs"
    indv6 = "participant"

    # averaged data: averaged deviation for each condition per participant
    # data_1 = data.groupby(["percent_triplets", "numerosity", "protectzonetype", "participant", "winsize"])[
    #     "deviation_score"] \
    #     .agg(['mean', 'std']) \
    #     .reset_index(level = ["percent_triplets", "numerosity", "protectzonetype", "participant", "winsize"])
    # rename_df_col(df = data_1, old_col_name = "mean", new_col_name = "mean_deviation_score")

    data_1 = data.groupby([indv, indv2, indv3, indv4, indv5, indv6])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3, indv4, indv5, indv6])

    # transfer column name
    data_1.columns = [''.join(x) for x in data_1.columns]

    data_1["samplesize"] = [5] * data_1.shape[0]  # each participant repeat each condition 5 times (5 displays)
    insert_new_col_from_two_cols(data_1, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_1, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # averaged data: averaged across participant
    data_2 = data.groupby(["percent_triplets", "numerosity", "protectzonetype", "winsize"])["deviation_score"] \
        .agg(["mean", "std"]).reset_index(level = ["percent_triplets", "numerosity", "protectzonetype", "winsize"])

    rename_df_col(df = data_2, old_col_name = "mean", new_col_name = "mean_deviation_score")
    insert_new_col(data_2, "winsize", "samplesize",
                   get_samplesize)  # 66 participants, 34 for winsize0.4, 32 for winsize0.6
    insert_new_col_from_two_cols(data_2, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: averaged deviation for different winsize per participant
    data_3 = data.groupby(["percent_triplets", "protectzonetype", "participant", "winsize"])["deviation_score"] \
        .agg(['mean', 'std']).reset_index(level = ["percent_triplets", "protectzonetype", "participant", "winsize"])
    rename_df_col(df = data_3, old_col_name = "mean", new_col_name = "mean_deviation_score")
    data_3["samplesize"] = [30] * data_3.shape[0]  # each participant repeat 6 numerosity * 5 displays = 30 times
    insert_new_col_from_two_cols(data_3, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: averaged deviation for different winsize, across participant
    data_4 = data.groupby(["percent_triplets", "protectzonetype", "winsize"])["deviation_score"] \
        .agg(['mean', 'std']).reset_index(level = ["percent_triplets", "protectzonetype", "winsize"])
    rename_df_col(df = data_4, old_col_name = "mean", new_col_name = "mean_deviation_score")
    insert_new_col(data_4, "winsize", "samplesize",
                   get_samplesize)  # 66 participants, 34 for winsize0.4, 32 for winsize0.6
    insert_new_col_from_two_cols(data_4, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: combined clustering level per participant
    data_5 = data.groupby(["numerosity", "protectzonetype", "participant", "winsize"])[
        "deviation_score"] \
        .agg(['mean', 'std']) \
        .reset_index(level = ["numerosity", "protectzonetype", "participant", "winsize"])

    rename_df_col(df = data_5, old_col_name = "mean", new_col_name = "mean_deviation_score")
    data_5["samplesize"] = [30] * data_5.shape[0]  # each participant repeat 6 numerosity * 5 displays = 30 times
    insert_new_col_from_two_cols(data_5, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: combined clustering level, across participant
    data_6 = data.groupby(["numerosity", "protectzonetype","winsize"])["deviation_score"].agg(['mean', 'std']) \
        .reset_index(level = ["numerosity", "protectzonetype", "winsize"])

    rename_df_col(df = data_6, old_col_name = "mean", new_col_name = "mean_deviation_score")
    insert_new_col(data_6, "winsize", "samplesize",
                   get_samplesize)  # 66 participants, 34 for winsize0.4, 32 for winsize0.6
    insert_new_col_from_two_cols(data_6, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    if write_to_excel:
        data_1.to_excel("prolifc_data.xlsx", index = False)