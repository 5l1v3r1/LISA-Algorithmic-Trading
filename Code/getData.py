# imports
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import datetime as dt
import pandas_datareader.data as wb
import pickle

df = pd.read_csv('S&P500.csv')

def save_tickers():
    tickers = []
    for i in df['Symbol']:
        tickers.append(i)
    with open('sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

def getData():
    save_tickers()
    with open('sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)
    if not os.path.exists('stocks'):
        os.makedirs('stocks')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tqdm(tickers):
        if not os.path.exists('stocks/{}.csv'.format(ticker)):
            try:
                df = wb.DataReader(ticker, 'google', start, end) # get data from google finance.
                df.to_csv('stocks/{}.csv'.format(ticker))
            except:
                pass
        else: print "The stock {} exists.".format(ticker)

def compileData():
    with open('sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    file_df = pd.DataFrame()

    for ticker in tickers:
        try: df = pd.read_csv('stocks/{}.csv'.format(ticker))
        except: pass
        df.set_index(df['Date'], inplace=True)
        df.rename(columns={'Close':ticker}, inplace=True)
        try: df.drop(['Open','High','Low','Volume'], axis=1, inplace=True)
        except: pass
        if file_df.empty: file_df = df
        else: file_df = file_df.merge(df, on='Date', how='outer')
    file_df.to_csv('sp500data.csv')

if __name__ == '__main__':
    compileData()
