from binance import Client
import matplotlib.pyplot as plt
import talib
import numpy as np
from tkinter import *
from tkinter import ttk

api_key = "Hgl2ZQwY8mYVQ7Z9xVOd5p30PfgsKo0kiY7CxNmGoA98lotG7JBrdetgY1bDQRze" # API KEY
api_secret = "6dRPwHLJcYOXYDzLag72eXDU6ayMAT5S1bKPtELv4Eu2dQZw4s5jLAKueYwkuxAy"
API_KEY = 'vTLCvhZ44XPLaaKfDzk0bclZNSSCZDdeZTdn4ciychjcYHoEwjGe2GBKHMnouzTp'
SECRET_KEY = 'GMdE32SEbwCGMzbBRAuefQGDDGFlYfapYiPF6BS7NZoca4ODLuaaRDA6AL8DZhmK'

# Crypto Price Checking Client
client = Client(api_key, api_secret)

################################### Bot Tab Function ##################################
def main(event=None):

    # Crypto Bot Client
    client = Client(API_KEY, SECRET_KEY)

    # INPUT
    USER_INP = e_coin.get().upper()

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
        plt.title(USER_INP.upper())
        plt.legend(loc="upper left")
        plt.show()

    signal_by_symbols(USER_INP.upper())

# GUI
GUI = Tk()
GUI.geometry('700x500')
GUI.title('CryptoBot')
t_image = PhotoImage(file='iconimage.png')
GUI.iconphoto(False, t_image)
FONT1 = ("Times", 30)

# TAB
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)

# TAB Style
b_image = PhotoImage(file='Bokeh-BackgroundPhoto.png')
b1_pic = Label(T1, image=b_image)
b2_pic = Label(T2, image=b_image)
b1_pic.place(x=0, y=-50)
b2_pic.place(x=0, y=-50)

Tab.pack(fill=BOTH, expand=1)

Tab.add(T1, text='Market', compound='left')
Tab.add(T2, text='Bot', compound='left')
ttk.Label(T2, text='Hello')

# Theme Style
F1_sty = ttk.Style()
F1_sty.theme_use('xpnative')

################################### MARKET TAB ##################################
F1 = ttk.Labelframe(T1, text='Market Price')
F1.place(x=50, y=50)

################################### Bot TAB ##################################
F2 = ttk.Labelframe(T2, text='Crypto BOT Processing')
F2.place(x=50, y=50)
# LABEL
L1 = ttk.Label(F1,text='Coin', font=FONT1)
L1.grid(row=0, column=0,padx=20)
L2 = ttk.Label(F2, text='Coin', font=FONT1)
L2.grid(row=0, column=0,padx=20)

# ENTRY COIN
v_coin = StringVar()
v_coin.set('BTCUSDT')
e_coin = StringVar()
e_coin.set('BTCUSDT')

E1 = ttk.Entry(F1, textvariable=v_coin, font=FONT1, width=15)
E1.grid(row=0, column=1, padx=20)
E2 = ttk.Entry(F2, textvariable=e_coin, font=FONT1, width=15)
E2.grid(row=0, column=1, padx=20)

# CHECK PRICE FUNCTION
def CheckPrice(event=None):
    global autostate
    symbol = v_coin.get()
    try:
        tickers = client.get_ticker(symbol=symbol)
        lastprice = float(tickers['lastPrice'])
        if lastprice > 5000:
            text = '{} : {:,.2f} ($)'.format(symbol, lastprice)
        elif lastprice > 200:
            text = '{} : {:,.3f} ($)'.format(symbol, lastprice)
        elif lastprice > 10:
            text = '{} : {:,.5f} ($)'.format(symbol, lastprice)
        else:
            text = '{} : {:,.8f} ($)'.format(symbol, lastprice)
        v_result.set(text)
    except:
        v_result.set('Error')
        ChangeState(state=False)
    if autostate == True:
        Result.after(500, CheckPrice)
    print(lastprice)

# BUTTON 
B1 = ttk.Button(F1, text='Check Price', command=CheckPrice)
B1.grid(row=1, column=1, padx=20, pady=10, ipady=10, ipadx=120)
B2 = ttk.Button(F2, text='Enter', command=main)
B2.grid(row=1, column=1, padx=20, pady=10, ipady=10, ipadx=120)

# ENTER
E1.bind('<Return>', CheckPrice)

# FRAME 2 
F2 = Frame(T1)
F2.place(x=50, y=200)

# PRICE RESULT
v_result = StringVar()
Result = ttk.Label(F2, textvariable = v_result, font=FONT1)
Result.pack()

# MODE
autostate = False 
def ChangeState(event=None, state=None):
    global autostate
    autostate = not autostate
    if state is not None:
        autostate = state
    if autostate == True:
        v_status.set('Status: (Auto) [F1] Change to Manual')
        CheckPrice()
    else:
        v_status.set('Status: (Manual) [F1] Change to Auto')
GUI.bind('<F1>', ChangeState)

v_status = StringVar()
v_status.set('Status: (Manual) [F1] Change to Auto')

Status = ttk.Label(T1, textvariable=v_status)
Status.place(x=20, y=450)


GUI.mainloop()
