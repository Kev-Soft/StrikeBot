import ccxt
import pandas as pd
from datetime import datetime
import talib as ta

money = 5000
active = False
tp_val = 0.5
stop_val = 0.5
side = "none"


# Connect binance
binance = ccxt.binance()
ohlcv = binance.fetch_ohlcv('BTC/USDT','15m',limit=1000)




df = pd.DataFrame(ohlcv, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
df['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
df.set_index('Time', inplace=True)
df['index'] = df.index
df['MA'] = ta.SMA(df['Close'],20)

df['3LineStrk'] = ta.CDL3LINESTRIKE(df['Open'],df['High'],df['Low'],df['Close'])




for i in df.index: 

    if active == False:
        if df["3LineStrk"][i] == 100:
            entry_price = df["Close"][i]
            
            size = money / df["Close"][i]
            active = True
            side = "short"
            stop = df["Close"][i] / 100 * (100 + stop_val)
            #print(stop)
            tp = df["Close"][i] / 100 * (100 - tp_val)
            #print(size*df["Close"][i])

        if df["3LineStrk"][i] == -100:
            entry_price = df["Close"][i]
            
            size = money / df["Close"][i]
            active = True
            side = "long"
            stop = df["Close"][i] / 100 * (100 - stop_val)
            #print(stop)
            tp = df["Close"][i] / 100 * (100 + tp_val)
            #print(size*df["Close"][i])    

    if active == True and side == "short":
        if df["Close"][i] >= stop:
            pnl = (entry_price * size) - (df["Close"][i] * size)
            money += pnl
            active = False
            print("Time: {} | Money: {} | Side: {} | Buy @: {} | Sell @: {} | PnL: {} ".format(df["index"][i], money, side, entry_price, df["Close"][i], pnl))
        if df["Close"][i] <= tp:
            pnl = (entry_price * size) - (df["Close"][i] * size)
            money += pnl
            active = False
            print("Time: {} | Money: {} | Side: {} | Buy @: {} | Sell @: {} | PnL: {} ".format(df["index"][i], money, side, entry_price, df["Close"][i], pnl))

    if active == True and side == "long":
        if df["Close"][i] <= stop:
            pnl = (df["Close"][i] * size) - (entry_price * size)
            money += pnl
            active = False
            print("Time: {} | Money: {} | Side: {} | Buy @: {} | Sell @: {} | PnL: {} ".format(df["index"][i], money, side, entry_price, df["Close"][i], pnl))
        if df["Close"][i] >= tp:
            pnl = (df["Close"][i] * size) - (entry_price*size)
            money += pnl
            active = False
            print("Time: {} | Money: {} | Side: {} | Buy @: {} | Sell @: {} | PnL: {} ".format(df["index"][i], money, side, entry_price, df["Close"][i], pnl))




