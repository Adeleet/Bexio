import keras
import numpy as np
import pandas as pd
from keras.backend import dot
from keras.layers import RNN, Activation, Dense, Input
from keras.models import Sequential


def in_quantile_range(series, lower, upper):
    upper = series.quantile(upper)
    lower = series.quantile(lower)
    return series.between(lower, upper)


def calculate_vwap(df):
    return df["foreignNotional"] / df["homeNotional"]


data = pd.read_csv("data/bucketed/trades.csv.gz", parse_dates=["timestamp"])

data["hlc"] = data[["high", "low", "close"]].mean(axis=1)
data["year"] = data["timestamp"].apply(lambda dt: dt.year)
data["vwap_calc"] = calculate_vwap(data)

data = data.fillna(method='ffill')

data["vwap_increase"] = data["vwap_calc"].shift(-1) > data["vwap_calc"]


model = Sequential()
model.add(Dense(128, input_shape=(6,)))
model.add(Activation('relu'))

model.add(Dense(1))
model.add(Activation('relu'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(x, y, batch_size=256)
