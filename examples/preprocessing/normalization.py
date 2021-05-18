import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

data = pd.read_csv('/home/hwang/SIB/log_example.csv')

#### normalization ####
MIN_BOUND = 0.01
MAX_BOUND = 0.02

def normalize(data):
    data = (data - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    data[data>1] = 1.
    data[data<0] = 0.
    return data

print(normalize(data))

#### zero centering ####
# a = np.array(data)
# AVG = np.mean(a)

# def zero_centering(data):
#     data = data - AVG
#     return data