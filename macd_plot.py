import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

bit_file = pd.read_csv('2022_Problem_C_DATA\BCHAIN-MKPRU.csv')
bit_df = pd.DataFrame(bit_file)

def _ema(arr):
    N = len(arr)
    α = 2/(N+1)
    data = np.zeros(len(arr))
    for i in range(len(data)):
        data[i] = arr[i] if i==0 else α*arr[i]+(1-α)*data[i-1]  #从首开始循环
    return data[-1]
    
def EMA(arr,period):
    data = np.full(arr.shape,np.nan)
    for i in range(period-1,len(arr)):
        data[i] = _ema(arr[i+1-period:i+1])
    return data

bit_df['EMA_S'] = EMA(bit_df['Price'].values, period=12)        # Short-term EMA
bit_df['EMA_L'] = EMA(bit_df['Price'].values,period=26)   # Long-term EMA

EMAS = bit_df['EMA_S'].values
EMAL = bit_df['EMA_L'].values
prices = bit_df['Price'].values
dates = bit_df['long_date'].values

bit_df['dif'] = bit_df['EMA_S'] - bit_df['EMA_L']
dif = bit_df['dif'].values
def MA(arr, N):
    data = np.zeros(len(arr))
    for i in range(len(arr)):
        data[i] = np.mean(arr[i-N:i])
    return data
DEA = MA(bit_df['dif'].values,12)
bit_df['DEA'] = DEA
bit_df['MACD'] = 2*(dif-DEA)
print(len(DEA[np.isnan(DEA)]))
print(len(EMAS[np.isnan(EMAS)]))
print(len(EMAL[np.isnan(EMAL)]))
print(len(dif[np.isnan(dif)]))

ax= bit_df.plot.bar(x="long_date",y="Price",color='green', legend='Price', alpha = 0.5)
bit_df.plot(x="long_date",y="EMA_S",color='red', alpha = 0.5,legend='EMA Short', ax=ax)
bit_df.plot(x="long_date",y="EMA_L",color='skyblue', legend = 'EMA Long',ax=ax)
bit_df.plot.bar(x="long_date",y="MACD",color='orange', legend = 'EMA Long', alpha = 0.5,ax=ax)
bit_df.plot(x="long_date",y="dif",color='blue', legend = 'EMA Long', alpha = 0.8,ax=ax)
bit_df.plot(x="long_date",y="DEA",color='yellow', legend = 'EMA Long', alpha = 0.8,ax=ax)
plt.axhline(0,color='black')
plt.xticks([])
plt.title('Bitcoin')
plt.show()