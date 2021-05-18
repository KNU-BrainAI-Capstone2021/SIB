import pandas as pd
import numpy as np

data = pd.read_csv('C:\study\opencv\datapreprocessing\dtest.csv')

n=3 # data 수

X = data['x'].sum()/n
print(X)

Y = data['y'].sum()/n
print(Y)

Z = data['z'].sum()/n
print(Z)
