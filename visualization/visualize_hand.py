

################################# import packages #################################

import pandas as pd

from smoother import gamma_smoothing, average_smoothing
from visualizer import plot_2d, plot_3d


#################################### load data ####################################

file_path = 'example_log.csv'

x_names = ['L%d%c' % (i, c) for i in range(21) for c in ['x', 'y', 'z']] 
y_names = ['a', 's', 'd', 'f']

col_names = x_names + y_names

df = pd.read_csv(file_path, names=col_names)

df = df.iloc[df.index[340:420]]


################################## data smoothing #################################

df_original = df
df_gamma    = gamma_smoothing(df, 0.4)
df_average  = average_smoothing(df, 5)

del df


#################################### plot data ####################################

dfs = [
    (df_original, 'Original Data (Unsmoothed)', 'results/hand_original'),
    (df_gamma,    'Gamma Decay Smoothing',      'results/hand_gamma'),
    (df_average,  'Local Average Smoothing',    'results/hand_average')
]

for df, title, file_path in dfs:
    plot_2d(df, title, file_path + '.png')
    plot_3d(df, title, file_path + '.gif')

