

################################# import packages #################################

import pandas as pd
from visualizer import plot_2d, plot_3d


#################################### load data ####################################

file_path = 'example_log.csv'

x_names = ['L%d%c' % (i, c) for i in range(21) for c in ['x', 'y', 'z']] 
y_names = ['a', 's', 'd', 'f']

col_names = x_names + y_names

df = pd.read_csv(file_path, names=col_names)

df = df.iloc[df.index[340:420]]


################################# average smoothing ###############################

x_df = df[x_names]

window_size = 20

for i in range(1, len(x_df)):

    start = max(0, i - window_size + 1)
    end   = i + 1

    df[x_names].iloc[i] = x_df.iloc[start:end].mean()


#################################### plot data ####################################

file_path = 'results/hand_average'

plot_2d(df, file_path + '.png')
plot_3d(df, file_path + '.gif')
