from binance import Client
import matplotlib.pyplot as plt
import talib
import numpy as np
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import urllib
from urllib import request
from datetime import datetime
from PIL import ImageTk, Image
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context

now = datetime.now()
current_time = now.strftime("%I:%M:%S %p")
global previous
previous = False

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
T3 = Frame(Tab)

# TAB Style
b_image = PhotoImage(file='Bokeh-BackgroundPhoto.png')
b1_pic = Label(T1, image=b_image)
b2_pic = Label(T2, image=b_image)
b1_pic.place(x=0, y=-50)
b2_pic.place(x=0, y=-50)

Tab.pack(fill=BOTH, expand=1)

Tab.add(T1, text='Market', compound='left')
Tab.add(T2, text='Bot', compound='left')
Tab.add(T3, text="BTC changed", compound='left')
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
# L3 = ttk.Label(F3)

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

################################### Current Bitcoin change TAB ##################################
F3 = ttk.Labelframe(T3, text='Changed Bitcoin Price')
F3.place(x=50, y=20)
lprice_label = Label(F3, text='Current BTC price', font=('Consolas', 36), bg='white')
lprice_label.pack()
def Update():
    global previous

    page = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json' , verify = False)
    data = page.json()
    price_large2 = data["bpi"]["USD"]["rate"]

    bit_label.config(text=f'${price_large2}')


    F3.after(30000, Update)

    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")

    current = price_large2
    status_bar.config(text=f'Last Updated: {current_time}   ')


    current = current.replace(',','')

    if previous:
        if float(previous) > float(current):
            lprice_label.config(text=f'-{round(float(previous) - float(current), 2)}', fg='red')

        elif float(previous) == float(current):
            lprice_label.config(text='+0.00', fg='grey')

        else:
            lprice_label.config(text=f'+{round(float(current) - float(previous), 2)}', fg='green')

    else:
        previous = current
        lprice_label.config(text='+0.00', fg='grey')
        
head = Label(F3, text='Bitcoin Price', font=('Verdana', 20), bg='white')
bit_label = Label(F3, text='TEST', font=('Consolas', 15), bg='white')
status_bar = Label(F3, text=f'Last Updated {current_time}   ',
	bd=0,
	anchor=E,
	fg="grey")
status_bar.pack(fill=X, side=TOP, ipady=2)
head.pack()
bit_label.pack()

Update()


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
