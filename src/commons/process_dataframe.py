import pandas as pd
from typing import List
import copy


# func_name: func_name is process each element in each column, instead of the whole column
def process_col(input_df: pd.DataFrame, col_name: str, func_name):
    if col_name in input_df.columns:
        input_df[col_name] = input_df[col_name].map(func_name)
    else:
        raise Exception(f"Warning: missing {col_name}")


# input_cols: col_name string in list
def process_cols(input_df: pd.DataFrame, input_cols: List[str], func_name):
    for col in input_cols:
        if col in input_df.columns:
            input_df[col] = input_df[col].map(func_name)
        else:
            raise Exception(f"Warning: Missing {col}")


# input_cols: col_name string in list
def get_processed_cols_df(input_df: pd.DataFrame, input_cols: List[str], func_name) -> pd.DataFrame:
    output_df = copy.deepcopy(input_df)
    for col in input_cols:
        if col in input_df.columns:
            output_df[col] = output_df[col].map(func_name)
        else:
            raise Exception(f"Warning: Missing {col}")
    return output_df


# old_col: old_col name string already in input_df
# new_col: new_col name string which is to insert in input_df
def insert_new_col(input_df: pd.DataFrame, old_col: str, new_col: str, func_name):
    if old_col in input_df.columns:
        col_index = input_df.columns.get_loc(old_col)
        input_df.insert(col_index, new_col, input_df[old_col].map(func_name))
    else:
        raise Exception(f"Warning: missing {old_col}")


def insert_new_col_from_two_cols(input_df: pd.DataFrame, old_col1: str, old_col2: str, new_col: str, func_name):
    cols = input_df.columns
    if (old_col1 in cols) and (old_col2 in cols):
        input_df[new_col] = input_df.apply(lambda x: func_name(x[old_col1], x[old_col2]), axis = 1)
    else:
        raise Exception(f"Warning: missing {old_col1} or {old_col2}")


def insert_new_col_from_three_cols(input_df: pd.DataFrame, old_col1: str, old_col2: str, old_col3: str, new_col: str,
                                   func_name):
    cols = input_df.columns
    if (old_col1 in cols) and (old_col2 in cols):
        input_df[new_col] = input_df.apply(lambda x: func_name(x[old_col1], x[old_col2], x[old_col3]), axis = 1)
    else:
        raise Exception(f"Warning: missing {old_col1} or {old_col2}")


def get_sub_df_according2col_value(input_df: pd.DataFrame, col_name: str, col_value) -> pd.DataFrame:
    return input_df.loc[input_df[col_name] == col_value]


def change_col_value_type(input_df: pd.DataFrame, col_name: str, new_type):
    """
    :param input_df:
    :param col_name:
    :param new_type: could be int, float, str.
    """
    input_df[col_name] = input_df[col_name].astype(new_type)


def keep_valid_columns(df: pd.DataFrame, kept_columns_list: list) -> pd.DataFrame:
    all_col_name_list = list(df.columns)
    all_col_name_copy_list = copy.deepcopy(all_col_name_list)
    drop_name_list = list()
    for name in all_col_name_copy_list:
        if name not in kept_columns_list:
            drop_name_list.append(name)
    df = df.drop(drop_name_list, axis = 1)
    return df


def get_col_names(simuli_df):
    # check df coloum names
    c_names = simuli_df.columns.to_list()
    return c_names


def rename_df_col(df: pd.DataFrame, old_col_name: str, new_col_name: str):
    df.rename(columns = {old_col_name: new_col_name}, inplace = True)


def get_pivot_table(input_df: pd.DataFrame, index, columns, values) -> pd.DataFrame:
    """
    :param input_df:
    :param index, cp;imns and values: list of strs - df col names
    :return: pivot table
    """
    pivot_table = pd.pivot_table(input_df,
                                 index = index,
                                 columns = columns,
                                 values = values)
    return pivot_table


def get_std(df: pd.DataFrame, col_name: str):
    return df[col_name].std()


def get_mean(df: pd.DataFrame, col_name: str):
    return df[col_name].mean()


def get_deviation(resp: int, numerosity: int) -> int:
    return resp - numerosity