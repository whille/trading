#!/usr/bin/env python
# encoding: utf-8
from scipy.stats import rankdata
import numpy as np
import pandas as pd


# 计算alpha时会使用的函数
def stddev(df,window=10):
    return df.rolling(window).std()

def correlation(x,y,window=10):
    return x.rolling(window).corr(y)

def covariance(x,y,window=10):
    return x.rolling(window).cov(y)

def rolling_rank(na):
    return rankdata(na)[-1]

def sma(df,window=10):
    return df.rolling(window).mean()

def rolling_prod(na):
    return na.prod(na)

def product(df,window=10):
    return df.rolling(window).apply(rolling_prod)

def delta(df,period=1):
    return df.diff(period)

def delay(df,period=1):
    return df.shift(period)

def rank(df):
    return df.rank(axis=1,pct=True)

def scale(df,k=1):
    return df.mul(k).div(np.abs(df).sum())

def ts_sum(df,window=10):
    return df.rolling(window).sum()

def ts_rank(window=10):
    # time series rank in the past d days
    return pd.rolling(window).apply(rolling_rank)

def ts_min(df,window=10):
    return df.rolling(window).min()

def ts_max(df,window=10):
    return df.rolling(window).max()

def ts_argmax(df,window=10):
    return df.rolling(window).apply(np.argmax)+1

def ts_argmin(df,window=10):
    return df.rolling(window).apply(np.argmin)+1
