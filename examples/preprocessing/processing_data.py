
################################# preprocessing ##################################

def preprocess(df,x_names, gamma): # df to df
    
    df = df.copy()

    cut_df = cut_outlier(df, x_names)
    gamma_df = gamma_smoothing(cut_df, gamma, x_names)
    minmax_df = MinMaxScaler(gamma_df, x_names)

    pre_df = minmax_df

    return pre_df

################################# cut_outlier ##################################
from matplotlib.pyplot import axis
import pandas as pd
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

################################# gamma_smoothihng ##################################

def gamma_smoothing(df, gamma, x_names):
    
    df = df.copy()

    for x in x_names:
        for row in range(1, len(df)):
            df[x].iloc[row] = df[x].iloc[row-1] * (1-gamma) + df[x].iloc[row] * gamma

    return df

################################# minmax_scaler ##################################


def MinMaxScaler(df, x_names):
    
    # for column in x_names:
    #     df_column = df[column]
    #     df_column = df_column.values.reshape(-1, 1)

    #     df_column = MinMaxScaler(df_column)

    #     for row in range(len(df)):
    #         df[column].iloc[row] = df_column[row]

    df = df.copy()

    x_df = df[x_names]

    x_min = x_df.min(axis=0)
    x_max = x_df.max(axis=0)

    df[x_names] = (df[x_names] - x_min) / (x_max - x_min)

    return df