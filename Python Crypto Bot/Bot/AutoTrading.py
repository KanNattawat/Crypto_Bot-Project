from binance import Client
import matplotlib.pyplot as plt
import talib
import numpy as np
from binance.enums import *
import math
from tkinter import *
from tkinter import ttk
from pprint import pprint

api_key = "Hgl2ZQwY8mYVQ7Z9xVOd5p30PfgsKo0kiY7CxNmGoA98lotG7JBrdetgY1bDQRze"
api_secret = "6dRPwHLJcYOXYDzLag72eXDU6ayMAT5S1bKPtELv4Eu2dQZw4s5jLAKueYwkuxAy"

client = Client(api_key, api_secret)

def place_buy(amount, symbol):
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)
    close = candles[0][4]
    minimum = float(close)*float(amount)
    print(minimum)
    if  minimum < 10:
        return print("NOT ENOUGHT MINIMUM PLACE ORDER")
    client.order_market_buy(
        symbol=symbol,
        quantity=str(amount))
    print("BUY COMPLETE")

def place_sell(symbol):
    n=3
    trades = client.get_my_trades(symbol=symbol)
    
    while True:
        try:
            qty = float(trades[0]["qty"]) - float(trades[0]["commission"])
            qty = str(qty)[:n]
            client.order_market_sell(
            symbol=symbol,
            quantity=str(qty))
            print("SELL COMPLETE")
            return  

        except:
            n = n-1
            pass

autostate = False
def signal_by_symbols():

    symbols = coin_name.get().upper()
    klines = client.get_historical_klines(symbols, Client.KLINE_INTERVAL_1MINUTE, "200 minutes ago UTC")

    closes = [float(i[4]) for i in klines]
    closes = np.array(closes)
    ema12 = talib.EMA(closes, timeperiod=12)
    ema26 = talib.EMA(closes, timeperiod=26)

    bullish = (ema12[-2] < ema26[-2]) and (ema12[-1] > ema26[-1]) #bullish cross
    bearish = (ema12[-2] > ema26[-2]) and (ema12[-1] < ema26[-1]) #bearish cross

    price = closes[-1]
    usd = int(input_coin.get())
    print(usd)

    amount = float(usd/price)
    # print(amount)

    if autostate == True:
        Result.after(1000, signal_by_symbols)

    if bullish:
        text = 'BUY'
        place_buy(amount=amount, symbol=symbols)

    elif bearish:
        text = 'SELL'
        place_sell(symbol=symbols)

    else:
        text = 'Waiting for Signal'
    print(amount, text)
    v_result.set(text)
    check_text(text)

none_count = 0
buy_count = 0
sell_count = 0
def check_text(text):
    balance = client.get_asset_balance(asset='USDT')
    global none_count, buy_count, sell_count
    if text == 'Waiting for Signal':
        none_count += 1
    elif text == 'BUY':
        buy_count += 1
    elif text == 'SELL':
        sell_count += 1
    total_nonecnt.set(str(none_count))
    total_buycnt.set(str(buy_count))
    total_sellcnt.set(str(sell_count))
    info.set(balance['free'])
    print(sell_count, buy_count, none_count)

# if __name__ == '__main__':
#     r = signal_by_symbols('BTCUSDT')
#     print(r)

GUI = Tk()
GUI.geometry('700x550')
GUI.title('CryptoBot')
t_image = PhotoImage(file='iconimage.png')
GUI.iconphoto(False, t_image)
FONT1 = ("Times", 30)

F1 = ttk.Labelframe(text='Buy & Sell\nDescription :\nThis tab will allow you to automatically buy & sell bitcoin')
F1.place(x=50, y=50)
F2 = ttk.Labelframe(text='Result')
F2.place(x=50, y=320)
F3_buy = ttk.Labelframe(text='BUY TOTAL')
F3_buy.place(x=50, y=410)
F3_sell = ttk.Labelframe(text='SELL TOTAL')
F3_sell.place(x=150, y=410)
F3_none = ttk.Labelframe(text='Wait for Signal')
F3_none.place(x=250, y=410)
F4_input = ttk.Labelframe(text='Input USDT (More than 10 USDT)')
F4_input.place(x=50, y=235)
F5_pocket = ttk.Labelframe(text='Your USDT balance')
F5_pocket.place(x=290, y=235)

display = ttk.Label(F1, text='Coin', font=FONT1)
display.grid(row=0, column=0,padx=20)

coin_name = StringVar()
coin_name.set('BTCUSDT')
v_result = StringVar()
input_coin = StringVar()
input_coin.set('10')
Result = ttk.Label(F2, textvariable = v_result, font=FONT1)
Result.pack()

total_buycnt = StringVar()
total_sellcnt = StringVar()
total_nonecnt = StringVar()
info = StringVar()
total_buy = ttk.Label(F3_buy, textvariable=total_buycnt, font=FONT1)
total_buy.grid(row=0, column=0, padx=20)
total_sell = ttk.Label(F3_sell, textvariable=total_sellcnt, font=FONT1)
total_sell.grid(row=1, column=0, padx=20)
total_none = ttk.Label(F3_none, textvariable=total_nonecnt, font=FONT1)
total_none.grid(row=2, column=0, padx=20)
pocket_display = ttk.Label(F5_pocket, textvariable=info, font=FONT1)
pocket_display.grid(row=4, column=0, padx=20)

input_box = ttk.Entry(F4_input, textvariable=input_coin, width=15)
input_box.grid(row=0, column=2, padx=20)


Ent = Entry(F1, textvariable=coin_name, font=FONT1, width=15)
Ent.grid(row=0, column=1, padx=20)

but = Button(F1, text='Enter', command=signal_by_symbols)
but.grid(row=1, column=1, padx=20, pady=10, ipady=10, ipadx=120)

sty = ttk.Style()
sty.theme_use('xpnative')

def ChangeState(event=None, state=None):
    global autostate
    autostate = not autostate
    if state is not None:
        autostate = state
    if autostate == True:
        v_status.set('Status: (Auto) [F1] Change to Manual')
        signal_by_symbols()
    else:
        v_status.set('Status: (Manual) [F1] Change to Auto')

GUI.bind('<F1>', ChangeState)

v_status = StringVar()
v_status.set('Status: (Manual) [F1] Change to Auto')

Status = ttk.Label(textvariable=v_status)
Status.place(x=20, y=525)

#พักก่อนจร้า
GUI.mainloop()
