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
    with open('sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)
        print tickers
    if not os.path.exists('stocks'):
        os.makedirs('stocks')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tqdm(tickers):
        if not os.path.exists('stocks/{}.csv'.format(ticker)):
            df = wb.DataReader(ticker, 'google', start, end) # get data from google finance.
            df.to_csv('stocks/{}.csv'.format(ticker))
        else: print "The stock {} exists.".format(ticker)


if __name__ == '__main__':
    getData()
