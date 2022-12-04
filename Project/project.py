from binance import Client
import matplotlib.pyplot as plt
import talib
import numpy as np

api_key = "Hgl2ZQwY8mYVQ7Z9xVOd5p30PfgsKo0kiY7CxNmGoA98lotG7JBrdetgY1bDQRze"
api_secret = "6dRPwHLJcYOXYDzLag72eXDU6ayMAT5S1bKPtELv4Eu2dQZw4s5jLAKueYwkuxAy"

client = Client(api_key, api_secret)

#symbols = "BTCUSDT"
def signal_by_symbols(symbols):
    klines = client.get_historical_klines(symbols, Client.KLINE_INTERVAL_1MINUTE, "100 minutes ago UTC")

    closes = [float(i[4]) for i in klines]
    closes = np.array(closes)

    ema12 = talib.EMA(closes, timeperiod=12)
    ema26 = talib.EMA(closes, timeperiod=26)

    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_xlabel("1 MIN TIME FRAME")
    axes.set_ylabel("PRICE {}".format(symbols))

    plt.plot(closes, "--", color="grey", label="Price")
    plt.plot(ema12, "-", color="green", label="ema12")
    plt.plot(ema26, "-", color="red", label="ema26")

    #cross over / cross under
    crossover = [] #buy
    crossunder = [] #sell

    for index, val in enumerate(zip(ema12, ema26)):
        i = val[0]
        j = val[1]
        print(i, ':', j)
        if (ema12[index-1] < ema26[index-1]) and (i>j):
            print("BULLISH HERE")
            crossover.append(i)
        elif (ema12[index-1] > ema26[index-1]) and (i<j):
            print("BEARISH HERE")
            crossunder.append(i)
        else:
            crossover.append(None)
            crossunder.append(None)

    crossover = np.array(crossover)
    crossunder = np.array(crossunder)
    print(crossover, crossunder)

    plt.plot(crossover, "x", color="green", label="BULLISH")
    plt.plot(crossunder, "x", color="red", label="BEARISH")

    plt.legend(loc="upper left")
    plt.show()

signal_by_symbols("ETHUSDT")
