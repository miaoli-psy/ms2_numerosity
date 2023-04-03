import pandas as pd

from src.commons.process_dataframe import rename_df_col, insert_new_col, insert_new_col_from_two_cols
from src.commons.process_number import cal_SEM
from src.ms2_uniform_prolific_1_main import get_percent_triplets


def get_samplesize(winsize):
    if winsize == 0.4:
        return 29
    else:
        return 27


if __name__ == '__main__':
    to_excel = False
    # read data
    PATH = "../data/ms2_mix_prolific_2_data/"
    DATA = "ms2_mix_2_preprocessed.xlsx"
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
    indv5 = "participant"

    # average data: average deviation and percent change for each condition per participant
    data_1 = data.groupby([indv, indv2, indv3, indv4, indv5])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3, indv4, indv5])

    # transfer column name
    data_1.columns = [''.join(x) for x in data_1.columns]

    data_1["samplesize"] = [5] * data_1.shape[0]  # each participant repeat each condition 5 times (5 displays)
    insert_new_col_from_two_cols(data_1, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_1, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # averaged across participant
    data_2 = data.groupby([indv, indv2, indv3, indv4])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3, indv4])

    # transfer column name
    data_2.columns = [''.join(x) for x in data_2.columns]

    insert_new_col(data_2, indv3, "samplesize", get_samplesize)  # 50 participants, 29 for winsize0.4, 21 for winsize0.6
    insert_new_col_from_two_cols(data_2, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_2, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # averaged data: averaged deviation for different winsize per participant
    data_3 = data.groupby([indv2, indv3, indv4, indv5])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv2, indv3, indv4, indv5])

    # transfer column name
    data_3.columns = [''.join(x) for x in data_3.columns]

    data_3["samplesize"] = [5 * 6] * data_3.shape[0]  #  5 displays * 6 numerosities
    insert_new_col_from_two_cols(data_3, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_3, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # averaged data: averaged deviation for different winsize across participant
    data_4 = data.groupby([indv2, indv3, indv4])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv2, indv3, indv4])

    # transfer column name
    data_4.columns = [''.join(x) for x in data_4.columns]

    insert_new_col(data_4, indv3, "samplesize", get_samplesize)  # 56 participants, 29 for winsize0.4, 27 for winsize0.6

    insert_new_col_from_two_cols(data_4, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_4, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    if to_excel:
        data_1.to_excel("ms2_mix_2_each_pp.xlsx")
        data_2.to_excel("ms2_mix_2.xlsx")
        data_3.to_excel("ms2_mix_2_combine_num_each_pp.xlsx")
        data_4.to_excel("ms2_mix_2_combine_num.xlsx")
