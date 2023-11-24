#!/usr/bin/env python

import pandas as pd
import seaborn as sns


PARAMS_FILEPATH = "params.csv"


def params_load(filepath=PARAMS_FILEPATH):
    return pd.read_csv(filepath)


def params_save(params, filepath=PARAMS_FILEPATH):
    params.to_csv(filepath, index=False)


#def standardize(df):
#    return (df - df.mean()) / df.std()


def model(params, x):
    return params['theta'][0] + params['theta'][1] * x


def sns_set_theme():
    # Apply theme
    sns.set_theme(
        style="dark",
        rc={
            'figure.facecolor': "#1e1f28",
            'axes.facecolor': "#282a36",
            'axes.edgecolor': "#bd93f9",
            'axes.titlecolor': "#50fa7b",
            'axes.labelcolor': "#ff79c6",
            'xtick.color': "#f8f8f2",
            'ytick.color': "#f8f8f2",
            'text.color': "#f8f8f2",
        }
    )

sns_set_theme()