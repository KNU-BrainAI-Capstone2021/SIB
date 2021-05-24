

################################# import packages #################################

import pandas as pd
import matplotlib.pyplot as plt

from celluloid import Camera

#################################### load data ####################################

file_path = 'example_log.csv'

x_names = ['L%d%c' % (i, c) for i in range(21) for c in ['x', 'y', 'z']] 
y_names = ['a', 's', 'd', 'f']

col_names = x_names + y_names

df = pd.read_csv(file_path, names=col_names)

df = df.iloc[df.index[340:420]]

columns = ['L%d%c' % (i, c) for i in range(21) for c in ['x', 'y', 'z']]
gamma = 0.2  # 감마 가중치

for column in columns:
    for row in range(1, len(df)):
        df[column].iloc[row] = df[column].iloc[row-1] * (1-gamma) + df[column].iloc[row] * gamma

x_df = df[x_names]


################################ plot hand landmark ###############################

fingers = [[0, 1, 2, 3, 4],
           [0, 5, 6, 7, 8],
           [9, 10, 11, 12],
           [13, 14, 15, 16],
           [0, 17, 18, 19, 20],
           [5, 9, 13, 17]]

finger_colors = ['r','g','b','c','m','y']


xs = df[['L%dx' % i for i in range(21)]]
ys = df[['L%dy' % i for i in range(21)]]
zs = df[['L%dz' % i for i in range(21)]]

a = xs.iloc[0]
b = xs.iloc[1]


fig = plt.figure(figsize=(10, 10))
ax = fig.gca(projection='3d')

camera = Camera(fig)

for n in range(len(xs)):
    x, y, z = xs.iloc[n], ys.iloc[n], zs.iloc[n]

    for finger, finger_color in zip(fingers, finger_colors):
        ax.plot(x[finger], y[finger], z[finger], finger_color)
        for i in finger:
            ax.text(x[i], y[i], z[i], '%d' % i)

    plt.xlabel('x')
    plt.ylabel('y')
    # plt.show()
    camera.snap()

animation = camera.animate(interval=50, blit=True)

animation.save(
    'hand_average.gif',
    dpi=100,
    savefig_kwargs={
        'frameon': False,
        'pad_inches': 'tight'
    }
)
