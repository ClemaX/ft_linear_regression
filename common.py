#!/usr/bin/env python

import pandas as pd


PARAMS_FILEPATH = "params.csv"


def params_load(filepath=PARAMS_FILEPATH):
    return pd.read_csv(filepath)


def params_save(params, filepath=PARAMS_FILEPATH):
    params['theta'].to_csv(filepath, index=False)


def model(params, x):
    return params['theta'][0] + params['theta'][1] * x
