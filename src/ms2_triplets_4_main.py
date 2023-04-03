import pandas as pd

from src.commons.process_dataframe import rename_df_col, insert_new_col_from_two_cols
from src.commons.process_number import cal_SEM

if __name__ == '__main__':
    to_excel = False

    # read data
    PATH = "../data/ms2_triplets_4_data/"
    DATA = "preprocessed_triplets_4.xlsx"
    data = pd.read_excel(PATH + DATA)

    dv = "deviation_score"
    dv2 = "percent_change"

    indv = "numerosity"
    indv2 = "protectzonetype"
    indv3 = "winsize"
    indv4 = "participant"

    # averaged data: averaged deviation and percent change for each condition per participant
    data_1 = data.groupby([indv, indv2, indv3, indv4])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3, indv4])

    # transfer column name
    data_1.columns = [''.join(x) for x in data_1.columns]

    data_1["samplesize"] = [5] * data_1.shape[0]  # each participant repeat each condition 5 times (5 displays)
    insert_new_col_from_two_cols(data_1, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_1, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # averaged across participant
    data_2 = data.groupby([indv, indv2, indv3])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3])

    # transfer column name
    data_2.columns = [''.join(x) for x in data_2.columns]

    data_2["samplesize"] = [16*5] * data_2.shape[0]  # 5 displays * 16 participants
    insert_new_col_from_two_cols(data_2, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_2, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    if to_excel:
        data_1.to_excel("ms2_triplets_4_data_each_pp.xlsx", index = False)
        data_2.to_excel("ms2_triplets_4_data.xlsx", index = False)
