import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import pickle

def get_data(tick):
  t = yf.Ticker(tick)
  data = t.history(period='730d', interval='1h')
  data.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
  return(data)


def use_data(open, close, high, low, volume):
  df = pd.DataFrame(open, columns=['open'])
  df['close'] = close
  df['high'] = high
  df['low'] = low
  df['volume'] = volume
  return(df)


def use_scale(df, ssx, ssy):
  x = ssx.transform(df.drop('High', axis=1))
  y = ssy.transform(df['High'])
  return(x,y)


def feature_engineer(df):
  df['High_Low_Diff'] = df['High']-df['Low']
  df['Open_Close_Diff'] = df['Open']-df['Close']
  df['High_Open_Diff'] = df['High']-df['Open']
  df['Low_Open_Diff'] = df['Low']-df['Open']
  df['Open_Shift_Diff'] = df['Open'] - df.shift()['Open']
  df['Close_Shift_Diff'] = df['Close'] - df.shift()['Close']
  df['Close_Open_Diff'] = df['Close'] - df.shift()['Open']
  df['Volume_Shift_Diff'] = df['Volume']-df.shift()['Volume']
  df.fillna(0, inplace=True)
  return(df)


def scale_data(data):
  ssx = StandardScaler()
  ssy = StandardScaler()
  new_x = pd.DataFrame(ssx.fit_transform(data[data.drop('High', axis=1).columns]), columns=data.drop('High', axis=1).columns)
  new_y = pd.DataFrame(ssy.fit_transform(data[['High']]), columns=['High'])
  new_data = pd.concat([new_x, new_y], axis=1)
  return(new_data, ssx, ssy)

def train_test_xy_split(data):
  train = data.iloc[:-1000]
  test = data.iloc[-1000:]
  print(train.shape, test.shape)
  trainx = train.drop('High', axis=1)
  trainy = train[['High']]
  testx = test.drop('High', axis=1)
  testy = test[['High']]
  datax = data.drop('High', axis=1)
  datay = data[['High']]
  return(trainx, testx, trainy, testy, datax, datay)

def model_create(trainx,trainy):
  model = Sequential()
  model.add(Dense(50, input_dim=12, activation='relu'))
  model.add(Dense(50, activation='relu'))
  model.add(Dense(50, activation='relu'))
  model.add(Dense(50, activation='relu'))
  model.add(Dense(50, activation='relu'))
  model.add(Dense(50, activation='relu'))
  model.add(Dense(1, activation='linear'))
  model.compile(loss='mse', optimizer='adam')
  model.fit(trainx, trainy,  batch_size=20, epochs=250)
  return(model)

def model_predict(model, x, ssy):
  pred = model.predict(x)
  pred = ssy.inverse_transform(pred)
  return(pred)
