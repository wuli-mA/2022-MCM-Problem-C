import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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

def MA(arr, N):
    data = np.zeros(len(arr))
    for i in range(len(arr)):
        data[i] = np.mean(arr[i-N:i])
    return data

class MACD_method:
    def __init__(self, df):
        self. df = df
        self. S = 12
        self.L = 26
        self.position = 0
    
    def derivative(self, array):
        data = np.zeros(len(array))
        for i in range(len(array)):
            data[i] = array[i] if i==0 else array[i]-array[i-1]
        return data

    def processing(self):
        self.df['EMA_S'] = EMA(self.df['Price'].values, period=12)
        self.df['EMA_L'] = EMA(self.df['Price'].values, period=26)
        self.df['dif'] = self.df['EMA_S'] - self.df['EMA_L']

        DEA = MA(self.df['dif'].values,12)
        MACD = 2*(self.df['dif'].values - DEA)
        self.df['DEA'] = DEA
        self.df['MACD'] = MACD
        self.df['Signal'] = EMA(MACD, 9)
        # self.df['dK'] = self.derivative(self.df['Price'].values)
        # self.df['dDEA'] = self.derivative(MACD)

    def get_strategy(self):
        self.df['Choice'] = 0
        choice = 'Hold'
        for i in range(3, self.df.shape[0]):
            if self.df['MACD'][i-3] <0 and self.df['MACD'][i-1] > 0:
                choice = 'Buy'
            if self.df['MACD'][i-3] >0 and self.df['MACD'][i-1] < 0:
                choice = 'Sell'
            self.df['Choice'][i] = choice

# bit_file = pd.read_csv('2022_Problem_C_DATA\BCHAIN-MKPRU.csv')
# bit_df = pd.DataFrame(bit_file)

# macd = MACD_method(bit_df)
# macd.processing()
# macd.get_strategy()