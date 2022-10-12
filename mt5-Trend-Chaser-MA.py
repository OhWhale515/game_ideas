# =====SMA Crossover=====

import MetaTrader5 as mt5
import pandas as pd
from datetime import datet
import time

# =====send market order function=====

def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": DEVIATION,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result


# =====close order by ticket id function=====

def close_order(ticket):
    positions = mt5.symbol_info_tick(pos.symbol)
    type_dict = {0: 1, 1: 0} # 0 = buy 1 = sell
    price_dict = {0: tick.ask 1: tick.bid}

    if pos.ticket == ticket:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": pos.ticket,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": type_dict[pos.type],
            "price": price_dict[pos.type],
            "deviation": DEVIATION,
            "magic": 100,
            "comment": "python close order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        order_result = mt5.order_send(request)
        print(order_result)

        return order_result

    return 'Ticket does not exist'


# =====symbol exposure function=====

def get_exposure(sumbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_sf = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volumes'].sum()

        return exposure   

# =====Signal function=====

def sugnal(symbol, timeframe, sma_period):
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period)
    bars_df = pd.DataFrame(bars)

    last_close = bars_df.iloc[-1].close
    sma = bars_df.close.mean()

    direction = 'flat'
    if last_close > sma:
        direction = 'buy'
    elif last_close < sma:
        direction = 'sell'

    return last_close, sma, direction

# =====strat parameters=====
if __name__ == '__main__':
    SYMBOL = "EURUSD" # ==TRADING PAIR==
    VOLUME = 1.0 # ==LOTS==
    TIMEFRAME = mt5.TIMEFRAME_M1 # ==Time Frame==
    SMA_PERIOD = 10 # SMA PERIOD==
    DEVIATION = 20 # ==Deviaion==

    mt5.initialize()

    while True :
        # ==account exposure calculations==
        exposure = get_exposure(SYMBOL)

        # ==last candle and SMA Signal Calculations==
        last_close, sma, direction = signal(SYMBOL, TIMEFRAME, SMA_PERIOD)

        # ==trade logic==
        if direction == 'buy'
            # ==if you have a BUY, close all Shorts==
            for pos in mt5.positions_get():
                if pos.type == 1:  # 1 = sell order
                    close_order(pos.ticket)

            # ==if no open positions, open new long==
            if not mt5.positions_total():
                market_order(SYMBOL, VOLUME, direction)

        elif direction == 'sell':
            # ==sell open, close all shorts==
            for pos in mt5.positions_get()
                if pos.type == 0: #== 0 = buy order==
                    close_order(pos.ticket)      

            # ==if not open positions, open new short==  
            if not mt5.positions_total():
                market_order(SYMBOL, VOLUME, direction)

        print('time: ', datetime.now())
        print('exposure: ', exposure)
        print('last_close: ', last_close)
        print('sma: ', sma)
        print('signal: ', direction)
        print('-------\n')

        # ==1second updates==

