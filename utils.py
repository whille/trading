#!/usr/bin/env python
# encoding: utf-8

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Return CSV file path given a stock ticker symbol."""
def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    for i, symbol in enumerate(symbols):
        df_tmp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'],na_values=['nan'])
        # rename to prevent clash
        df_tmp = df_tmp.rename(columns={'Adj Close': symbol})
        df = df.join(df_tmp)
        if i <1:
            df=df.dropna()#, how=how)
    return df

def normalize(df):
    return df/df.ix[0]

def plot_selected(df, columns, start, end):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.ix[start:end, columns])

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper = rm + rstd * 2   # !notice
    lower = rm - rstd * 2
    return upper, lower

def daily_returns(df):
    res = df.copy()
    #res[1:] = (df[1:] / df[:-1].values) -1
    res = (df[1:] / df.shift(1)) -1
    res.ix[0] = 0 # set row 0 to 0
    return res

def cumulative_returns(df):
    res = df.copy()
    res = (df[1:] / df.ix[0,0]) -1
    res.ix[0, :] = 0
    return res

def plot_beta(df, x, symbol):
    df.plot(kind='scatter', x=x, y=symbol)
    beta, alpha = np.polyfit(df[x], df[symbol], 1)
    print beta, alpha
    plt.plot(df[x], beta * df[x] + alpha , '-', color='r')

def plot_rolling(df, symbol):
    # Plot raw values, rolling mean and Bollinger Bands
    roll = df[symbol].rolling(window=20,center=False)
    mean, std = roll.mean(), roll.std()
    upper_band, lower_band = get_bollinger_bands(mean, std)
    ax = df[symbol].plot(title="Bollinger Bands", label=symbol)
    mean.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='best') #'upper left')
    plt.show()
