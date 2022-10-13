# ==libraries==
import MetaTrader5 as mt5
from Trading-AI-Temps.mt5-Trend-Chaser-MA import SMA_PERIOD
from Trading-AI-Temps.mt5-Trend-Chaser-MA import DEVIATION
from Trading-AI-Temps.mt5-Trend-Chaser-MA import VOLUME
from Trading-AI-Temps.mt5-Trend-Chaser-MA import TIMEFRAME
from Trading-AI-Temps.mt5-Trend-Chaser-MA import SYMBOL
import pandas as pd
import time

#=====Strat Config=====

SYMBOL = 'EURUSD' #==CURRENCY BEING TRADED==
TIMEFRAME = mt5.TIMEFRAME_M1 #==TIMEFRAME==
VOLUME = 1.0  #==LOT SIZE==
DEVIATION = 20 #==ORDER SLIPPAGE==
MAGIC = 10
SMA_PERIOD = 20 #==SMA PERIOD FOR BANDS==
STANDARD_DEVIATIONS = 2 #==Deviations per band==
TP_SD = 2 #==Deviations per take profit==
SL_SD = 3 #==Deviations per stop loss==


#==MARKET ORDER FUNCTIONS==
def market_order(symbol, volume, order_type, deviation, magic, stoploss, takeprofit):
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": order_dict[order_type],
        "deviation": deviation,
        "magic": magic,
        "sl": stoploss,
        "tp": takeprofit,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC 
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result

def get_signal():
    #==bar data==
    bars = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 1, SMA_PERIOD)

    #==convert to dataframe==
    df = pd.DataFrame(bars)

    #==SMA==
    sma = df['close'].mean()

    #==standard deviation==
    sd = df['close'].std()

    #==lower boll band==
    lower_band = sma - STANDARD_DEVIATIONS * sd
    #==upper boll band==
    upper_band = sma + STANDARD_DEVIATIONS * sd

    #==last close price==
    last_close_price = df.iloc[-1]['close']

    print(last_close_price, upper_band)
    #==signal==
    if last_close_price < lower_band:
        return 'buy', sd

    elif last_close_price > upper_band:
        return 'sell', sd

    else:
        return [None, None]

#==platform commit==
initialized = mt5.initialize()

if initialized:
    print('commented to MetaTrader5')
    print('Login: ', mt5.account_info().login)
    print('Server: ', mt5.account_info().server)

#==Strat Loop==
while True:

      #==Strat logic==

      #==if no position is open==
      if mt5.position_total() == 0:
        signal, standard_deviation = get_signal()
        print(signal, standard_deviation)

        tick = mt5.symbol_info_tick(SYMBOL)
        if signal == 'buy'
            market_order(SYMBOL, 1.0, 'buy', 20, 10, tick.bid - SL_SD * standard_deviation,
                         tick.bid + TP_SD * standard_deviation)

# signal check every 1 second
time.sleep(1)                         
