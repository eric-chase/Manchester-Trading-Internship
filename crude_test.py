from pandas import DataFrame
import pandas as pd
import numpy as np
import data3
import datetime
from reversal_test import get_df
from reversal_test import get_price_high
from reversal_test import get_price_low

if(__name__ == "__main__"):
    sp = data3.load_market(market = "crude", type_of_data = "rolled")["2016-01-19":]
    df = pd.DataFrame(sp)

    df_new = get_df("2016-01-19")
    s_arr = []
    success = 0
    count = 0
    for i in df_new.index.values:
        if(count != len(df_new.index.values) - 1):
            order_y = ''
            order_t = ''
            min_time = int((df_new.idxmin(axis = 1)[i])[0:2])
            max_time = int((df_new.idxmax(axis = 1)[i])[0:2])

            min_price = get_price_low(df_new, df_new.index.values[count + 1])
            max_price = get_price_high(df_new, df_new.index.values[count + 1])
            if(min_price < max_price):
                success += 1
            count += 1
        else:
            count += 1

    print ""
    print "Number of successes:", success
    print "Observation count:", count
    print "Probability:", float(success) / count
