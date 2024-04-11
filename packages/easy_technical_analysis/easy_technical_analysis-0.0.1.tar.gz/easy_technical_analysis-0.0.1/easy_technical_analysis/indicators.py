import ta
import ta.wrapper
import urllib3
import requests
import kiteconnect
import time as tt
import pandas as pd
from requests import ReadTimeout
from datetime import datetime, timedelta

from easy_technical_analysis.kite_login import kite


national_holiday = {'1': [22, 26], '3': [8, 25, 29], '4': [11, 17], '5': [1], '6': [17], '7': [17], '8': [15], '9': [], '10': [2],
                    '11': [1, 15], '12': [25]}
"""
time - time frame data, it should be in form of 1minute ,1hr,
interval - it can be [hour , minute ]
intervalValue - it is the numerical value like 1,2...
"""


def get_historical_data(instrument, interval, interval_value):
    try:
        if "min" in interval:
            interval = str(interval_value) + "minute"
        if ("hr" in interval) or ("hour" in interval):
            interval = str(interval_value) + "hour"
        date = datetime.now()
        return kite.historical_data(instrument, date - timedelta(days=3), date, interval, False)
    except (
            kiteconnect.exceptions.DataException, KeyError, ReadTimeout,
            requests.exceptions.ConnectionError, ConnectionResetError, ConnectionAbortedError,
            ConnectionRefusedError, urllib3.exceptions.ConnectTimeoutError, requests.exceptions.ConnectionError):
        tt.sleep(5)
        time = datetime.now()
        return kite.historical_data(instrument, time - timedelta(days=1), time, interval, False)


"""
time - time frame data, it should be in form of 1minute ,1hr,
interval - it can be [hour , minute ]
intervalValue - it is the numerical value like 1,2...
window - rsi window 
"""


def get_rsi_value(instrument_token, window, interval, interval_value):
    dataBN = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    dataBN['RSI'] = ta.momentum.RSIIndicator(
        dataBN['close'], window=window, fillna=False).rsi()
    dataLast = dataBN.tail(2)
    return dataLast.iloc[1]['RSI']


# True strength index (TSI)
# close(pandas.Series) – dataset ‘Close’ column.
# window_slow(int) – high period.
# window_fast(int) – low period.

def tsi(instrument_token, slow, fast, interval, interval_value):
    dataBN = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    dataBN['TSI'] = ta.wrapper.TSIIndicator(
        dataBN["close"], slow, fast, fillna=False).tsi()
    dataLast = dataBN.tail(2)
    return dataLast.iloc[1]['TSI']

# ROC Indicator

# close (pandas.Series) – dataset ‘Close’ column.
# window (int) – n period.
# fillna (bool) – if True, fill nan values.


def roc(instrument_token, window, interval, interval_value):
    dataBN = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    dataBN['ROC'] = ta.wrapper.ROCIndicator(dataBN["close"], window).roc()
    dataLast = dataBN.tail(2)
    return dataLast.iloc[1]['ROC']

# Average True Range

# high (pandas.Series) – dataset ‘High’ column.
# low (pandas.Series) – dataset ‘Low’ column.
# close (pandas.Series) – dataset ‘Close’ column.
# window (int) – n period.
# fillna (bool) – if True, fill nan values.


def atr_indicator(instrument_token, window, interval, interval_value):
    dataBN = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    dataBN['ATR'] = ta.wrapper.AverageTrueRange(
        dataBN["high"], dataBN["low"], dataBN["close"], window).average_true_range()
    dataLast = dataBN.tail(2)
    return dataLast.iloc[1]['ATR']

# Detrended Price Oscillator (DPO)

# close (pandas.Series) – dataset ‘Close’ column.
# window (int) – n period.
# fillna (bool) – if True, fill nan values


def dpo_indicator(instrument_token, interval, interval_value, window):
    dataBN = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    dataBN['DPO'] = ta.wrapper.DPOIndicator(
        dataBN["close"], window, False).dpo()
    dataLast = dataBN.tail(2)
    return dataLast.iloc[1]['DPO']

# ADX Indicator

# high (pandas.Series) – dataset ‘High’ column.
# low (pandas.Series) – dataset ‘Low’ column.
# close (pandas.Series) – dataset ‘Close’ column.
# window (int) – n period.
# fillna (bool) – if True, fill nan values.


def adx_indicator(instrument_token, interval, interval_value, window):
    data = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    data['ADX'] = ta.wrapper.ADXIndicator(
        data["high"], data["low"], data["close"], window).adx()
    dataLast = data.tail(2)
    return dataLast.iloc[1]['ADX']


# MACD

# close (pandas.Series) – dataset ‘Close’ column.
# window_fast (int) – n period short-term.
# window_slow (int) – n period long-term.
# window_sign (int) – n period to signal.
# fillna (bool) – if True, fill nan values.

def macd(instrument_token, interval, interval_value, window_fast, window_slow, window_sign):
    data = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    data['MACD'] = ta.wrapper.MACD(
        data["close"], window_slow, window_fast, window_sign).macd()
    dataLast = data.tail(2)
    return dataLast.iloc[1]['MACD']


# SMA Indicator
# close (pandas.Series) – dataset ‘Close’ column.
# window (int) – n period.
# fillna (bool) – if True, fill nan values.

def sma_Indicator(instrument_token, interval, interval_value, window):
    data = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    data['SMA'] = ta.wrapper.SMAIndicator(
        data["close"], window, False).sma_indicator()
    dataLast = data.tail(2)
    return dataLast.iloc[1]['SMA']


# EMA Indicator

# close (pandas.Series) – dataset ‘Close’ column.
# window (int) – n period.
# fillna (bool) – if True, fill nan values.

def ema_Indicator(instrument_token, interval, interval_value, window):
    data = pd.DataFrame(get_historical_data(
        instrument_token, interval, interval_value))
    data['EMA'] = ta.wrapper.EMAIndicator(
        data["close"], window, False).ema_indicator()
    dataLast = data.tail(2)
    return dataLast.iloc[1]['EMA']
