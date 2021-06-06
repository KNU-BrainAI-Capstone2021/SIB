


################################# import packages #################################

import matplotlib.pyplot as plt

from celluloid import Camera


x_names = ['L%d%c' % (i, c) for i in range(21) for c in ['x', 'y', 'z']] 
y_names = ['a', 's', 'd', 'f']

landmark = ['WRIST', 
            'THUMB_CMC',         'THUMB_MCP',         'THUMB_IP',          'THUMB_TIP', 
            'INDEX_FINGER_MCP',  'INDEX_FINGER_PIP',  'INDEX_FINGER_DIP',  'INDEX_FINGER_TIP',
            'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_TIP',
            'RING_FINGER_MCP',   'RING_FINGER_PIP',   'RING_FINGER_DIP',   'RING_FINGER_TIP',
            'PINKY_MCP',         'PINKY_PIP',         'PINKY_DIP',         'PINKY_TIP']


########################### plot z-values of finger tips ##########################

def plot_2d(df, title, file_name='hand.png'):                

    plt.figure(figsize=(12, 8))

    ax0 = plt.subplot2grid((3, 1), (0, 0), rowspan=1)
    ax1 = plt.subplot2grid((3, 1), (1, 0), rowspan=2)

    for y in y_names:
        ax0.plot(df[y], label=y)
    ax0.set_title('keyboard input')
    ax0.legend(loc='upper left')

    for i in [4, 8, 12, 16, 20]:
        ax1.plot(df['L%dz' %i], label=landmark[i])
    ax1.set_title('z values')
    ax1.legend(loc='upper left')

    plt.suptitle(title)
    plt.tight_layout()
    # plt.show()
    plt.savefig(file_name)


################################ plot hand landmark ###############################

def plot_3d(df, title, filename='hand.gif'):
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


    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')
    ax.set_title(title)

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
        filename=filename,
        dpi=100,
        savefig_kwargs={
            'frameon': False,
            'pad_inches': 'tight'
        }
    )
