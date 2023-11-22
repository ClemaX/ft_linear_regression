#!/usr/bin/env python

import pandas as pd

THETAS_INITIAL = {'theta_0': [0], 'theta_1': [0]}

thetas = pd.DataFrame(data=THETAS_INITIAL)

def thetas_load(filepath):
    pd.read_csv(filepath)

def thetas_save(filepath):
    thetas.to_csv(filepath)

def model(x):
    return thetas['theta_0'][0] + thetas['theta_1'][0] * x
