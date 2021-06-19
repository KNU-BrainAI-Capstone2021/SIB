
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

