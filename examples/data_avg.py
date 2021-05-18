import pandas as pd
import numpy as np

data = []
f = open('C:\study\opencv\datapreprocessing\log_example.csv', 'r',encoding='utf-8')

for i in range(1,10):   #1부터 10까지 읽어오기
    D=f.readline()      #line마다 읽어오기
    data.append(float(D[:-1])) #/n 제거
f.close()

# print(data)
sum=0
num=0
for ii in data:
    sum = sum + ii
    num = num+1

avg_data=sum/num

print(avg_data)