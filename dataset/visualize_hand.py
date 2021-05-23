

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

df = df.iloc[df.index[100:-100]]

x_df = df[x_names]


################################# import packages #################################

fingers = [[0, 1, 2, 3, 4],
           [0, 5, 6, 7, 8],
           [9, 10, 11, 12],
           [13, 14, 15, 16],
           [0, 17, 18, 19, 20],
           [5, 9, 13, 17]]

finger_colors = ['r','g','b','c','m','y']


# x_means = x_df.mean()

# xs = x_means[['L%dx' % i for i in range(21)]]
# ys = x_means[['L%dy' % i for i in range(21)]]
# zs = x_means[['L%dz' % i for i in range(21)]]

xs = df[['L%dx' % i for i in range(21)]]
ys = df[['L%dy' % i for i in range(21)]]
zs = df[['L%dz' % i for i in range(21)]]


fig = plt.figure(figsize=(10, 10))
camera = Camera(fig)

for n in range(10):

    ax = fig.gca(projection='3d')

    x, y, z = xs.iloc[n], ys.iloc[n], zs.iloc[n]    
    j = 0

    for finger, finger_color in zip(fingers, finger_colors):
        ax.plot(x[finger], y[finger], z[finger], finger_color)
        j = (j+1) % 6
        for i in finger:
            ax.text(x[i], y[i], z[i], '%d' % i)


    plt.xlabel('x')
    plt.ylabel('y')
    # plt.show()
    camera.snap()

animation = camera.animate(interval=50, blit=True)

animation.save(
    'hand.gif',
    dpi=100,
    savefig_kwargs={
        'frameon': False,
        'pad_inches': 'tight'
    }
)
