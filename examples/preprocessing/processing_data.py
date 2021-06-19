################################# preprocessing ##################################

def Preprocess_data(df, x_names, gamma=0.4,  ):

    cut_df = cut_outlier(df,x_names)
    smooth_df = gamma_smoothing(cut_df, x_names, gamma)
    minmax_df = MinMaxScaler(smooth_df, x_names)

    processed_df = minmax_df

    return processed_df



################################# 보조 함수들... ##################################
################################# cut_outlier ##################################

def cut_outlier(df, x_names):
    
    df = df.copy()

    df_median = df[x_names]-df[x_names].median()
    df_median = pd.DataFrame(abs(df_median)).to_numpy()

    new_df = df.copy()
    for c in x_names:     #Left hands's x,y,z
        if c == 'L0x' or c=='L0y' or c=='L0z' : # 이 좌표값은 필요 없을것으로 판단..
            continue
        std_ = df[c].std()
        # change = 0
        cc = 0
        for i in range(df.shape[0]):   

            # replace pre row data
            if (df_median[i,cc] > 3*(std_)):
                new_df.iloc[i,:] = new_df.iloc[i-1,:]
                # change = change+1
        # print('changes number %s:'%c ,change)
        cc = cc+1

    return new_df

################################# gamma smoothing ##################################

def gamma_smoothing(df,x_names, gamma):
    
    df = df.copy()

    for x in x_names:
        for row in range(1, len(df)):
            df[x].iloc[row] = df[x].iloc[row-1] * (1-gamma) + df[x].iloc[row] * gamma

    return df

################################# MinMaxScaler ##################################

def MinMaxScaler(df,x_names):
    df = df.copy()

    df_min = df.min()
    df_max = df.max()

    for cc in range(len(x_names)):
        for i in range(len(df)):
            df.iloc[i,cc] = (df.iloc[i,cc] - df_min) / (df_max - df_min)

    return df


