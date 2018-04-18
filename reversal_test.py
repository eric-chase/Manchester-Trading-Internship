# Program for returning the price at time of high or low for the previous day
# Author: Eric Chase

from pandas import DataFrame
import pandas as pd
import numpy as np
import data3
import data3_new
import datetime

# The easiest way to do this is to create a DataFrame with the time stamp
# (date part) as the indices and the market hours as the columns
def get_df(date = 0):
    # Unless specified otherwise, we will only use the last two months of data
    if(date == 0):
        start_date = datetime.date.today() - datetime.timedelta(2 * (365 / 12))
        sp = data3_new.load_market(market = "crude", type_of_data = "rolled")[start_date:]
        df = pd.DataFrame(sp)
    else:
        start_date = date
        sp = data3_new.load_market(market = "crude", type_of_data = "rolled")[start_date:]
        df = pd.DataFrame(sp)
    
    rng = []
    data = {}
    x = 0
    length = 0
    for i in df.index:
        time = (str(i))[11:]
        date = (str(i))[:10]
        if date not in rng:
            rng.append(date)
            length += 1
        if ((time[3:] == '00:00') and (time not in data)):
            # Fill in missing hours
            for i in range(0, int(time[0:2])):
                hour = str(i) + ':00:00'
                if(len(hour) != 8):
                    hour = '0' + hour
                if(hour not in data):
                    data[hour] = []
            data[time] = []
        if(time in data):
            while(len(data[time]) + 1 < length):
                data[time].append(np.nan)
            data[time].append(df['price'][x])
        x += 1
    for i in data:
        while(len(data[i]) != length):
            data[i].append(np.NaN)

    print df.describe()
    df_updated = pd.DataFrame(data, index = rng)
    print df_updated.describe()
    return df_updated

# Prints the price for the requested day at the time of the previous day's high
def get_price_high(df, date):
    try:
        prev_date = ''
        count = 0
        for i in df.index.values:
            if(i == date):
                prev_date = df.index.values[count - 1]
            count += 1
        max_prev_time = df.idxmax(axis = 1)[prev_date]
        print "Time at maximum of previous day:", max_prev_time
        current_price = df[max_prev_time][date]
        print "Price at time of maximum:", current_price
        return float(current_price)
    except(KeyError):
        get_price_high(get_df(), date)

# Prints the price for the requested day at the time of the previous day's low
def get_price_low(df, date):
    try:
        prev_date = ''
        count = 0
        for i in df.index.values:
            if(i == date):
                prev_date = df.index.values[count - 1]
            count += 1
        min_prev_time = df.idxmin(axis = 1)[prev_date]
        print "Time at minimum of previous day:", min_prev_time
        current_price = df[min_prev_time][date]
        print "Price at time of minimum:", current_price
        return float(current_price)
    except(KeyError):
        get_price_low(get_df(), date)

# Calculation of the prices
if(__name__ == "__main__"):
    df_new = get_df()
    get_price_high(df_new, '2018-01-17')
    get_price_low(df_new, '2018-01-17')
