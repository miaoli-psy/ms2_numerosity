# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-09 00:02
IDE: PyCharm
Introduction:
"""


def get_sub_dict(input_dict: dict, wanted_key_list: list) -> dict:
    return dict((k, input_dict[k]) for k in wanted_key_list)