

################################# import packages #################################

x_names = ['L%d%c' % (i, c) for i in range(21) for c in ['x', 'y', 'z']] 


################################# gamma smoothing #################################

def gamma_smoothing(df, gamma=0.4):

    df = df.copy()
    
    for x in x_names:
        for row in range(1, len(df)):
            df[x].iloc[row] = df[x].iloc[row-1] * (1-gamma) + df[x].iloc[row] * gamma

    return df



################################# average smoothing ###############################

def average_smoothing(df, window_size=5):    
    
    df = df.copy()
    df_x = df[x_names].copy()

    window_size = 5

    for x in x_names:
        for i in range(1, len(df)):

            start = max(0, i - window_size + 1)
            end   = i + 1

            df[x].iloc[i] = df_x[x].iloc[start:end].mean()
    
    return df


