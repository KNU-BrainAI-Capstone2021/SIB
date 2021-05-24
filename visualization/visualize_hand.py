

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


#################################### plot data ####################################

file_path = 'results/hand_original'

plot_2d(df, file_path + '.png')
plot_3d(df, file_path + '.gif')

