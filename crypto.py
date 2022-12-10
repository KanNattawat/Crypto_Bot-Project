from tkinter import *
from tkinter import ttk
from binance.client import Client

#################################### Binance ####################################

API_KEY = 'vTLCvhZ44XPLaaKfDzk0bclZNSSCZDdeZTdn4ciychjcYHoEwjGe2GBKHMnouzTp'
SECRET_KEY = 'GMdE32SEbwCGMzbBRAuefQGDDGFlYfapYiPF6BS7NZoca4ODLuaaRDA6AL8DZhmK'
client = Client(API_KEY, SECRET_KEY)

################################### GUI #########################################

GUI = Tk()
GUI.geometry('700x500')
GUI.title('CryptoBot')
FONT1 = ("Times", 30)

# TAB
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)
T4 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

Tab.add(T1, text='Market', compound='left')
Tab.add(T2, text='Sell', compound='left')
Tab.add(T3, text='Buy', compound='left')
Tab.add(T4, text='Balance', compound='left')

################################### MARKET TAB ##################################
F1 = ttk.Labelframe(T1, text='Market Price')
F1.place(x=50, y=50)

# LABEL
L1 = ttk.Label(F1,text='Coin', font=FONT1)
L1.grid(row=0, column=0,padx=20)

# ENTRY COIN
v_coin = StringVar()
v_coin.set('BTCUSDT')
E1 = ttk.Entry(F1, textvariable=v_coin, font=FONT1, width=15)
E1.grid(row=0, column=1, padx=20)

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

# BUTTON 
B1 = Button(F1,text='Check Price', command=CheckPrice, bg="green")
B1.grid(row=1, column=1, padx=20, pady=10, ipady=8, ipadx=115)

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

################################### SELL TAB ##################################

v_sell_coin = StringVar()
v_sell_coin.set('BTCUSDT')
ET21 = ttk.Entry(T2, textvariable=v_sell_coin, font=FONT1, width=15)
ET21.pack(pady=10)

v_sell_amount = StringVar()
v_sell_amount.set('1')
ET22 = ttk.Entry(T2, textvariable=v_sell_amount, font=FONT1, width=15)
ET22.pack(pady=10)

v_sell_price = StringVar()
v_sell_price.set('54321')
ET23 = ttk.Entry(T2, textvariable=v_sell_price, font=FONT1, width=15)
ET23.pack(pady=10)

BSell = ttk.Button(T2, text='Sell')
BSell.pack(pady=50, ipadx=20, ipady=10)

GUI.mainloop()
