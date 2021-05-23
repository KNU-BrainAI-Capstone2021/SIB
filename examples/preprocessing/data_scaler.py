#1. Standard_Scaler  -평균 = 0 / 표준편차 = 1
from sklearn.preprocessing import StandardScaler

# Standardization 평균 0 / 분산 1
scaler = StandardScaler()   

scaler = scaler.fit_transform(data)

# 교차검증시
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



#2. MinMax_Scaler - 최소-최대 정규화 Min-Max Normalization(이상치에 취약)
from sklearn.preprocessing import MinMaxScaler

# Normalization 최소값 0 / 최대값 1
scaler = MinMaxScaler()

scaler = scaler.fit_transform(data)

# 교차검증시
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



#3. Robust_Scaler- 중앙값 = 0 / IQR(1분위(25%) ~ 3분위(75%)) = 1,( 이상치(outlier) 영향 최소)
from sklearn.preprocessing import RobustScaler

# median 0 / IQR 1
scaler = RobusterScaler()

scaler = scaler.fit_transform(data)

# 교차검증시
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


#4. MaxAbsScaler - 0을 기준으로 절대값이 가장 큰 수가 1또는 -1이 되도록 변환
from sklearn.preprocessing import MaxAbsScaler

# 절대값
scaler = MaxAbsScaler()

scaler = scaler.fit_transform(data)

# 교차검증시
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)