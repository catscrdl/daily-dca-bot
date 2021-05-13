import yaml
import os
import requests
import alpaca_trade_api as tradeapi
from math import ceil
from datetime import date

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

def buy_stock(symbol, amount, environment):
    with open('config.yml') as file:
        creds = yaml.load(file, Loader=yaml.FullLoader)['alpaca']
        os.environ["APCA_API_KEY_ID"] = creds[environment]['api_key_id']
        os.environ["APCA_API_SECRET_KEY"] = creds[environment]['secret_key']
        os.environ["APCA_API_BASE_URL"] = creds[environment]['endpoint']

    api = tradeapi.REST()

    try:
        trade_result = api.submit_order(symbol = symbol, notional= amount , side='buy', type='market', time_in_force='day')
    except Exception as e:
        barset = api.get_barset(symbol, 'day', limit=5)
        stock_bars = barset[symbol]
        count = 0
        val = 0
        for stock_bar in stock_bars:
            val += stock_bar.o
            val += stock_bar.c
            count += 2
        if val/count < 200 and date.today().isoweekday() == 3 and date.today().day >= 15 and date.today().day < 22:
            trade_result = api.submit_order(symbol = symbol, qty= 1 , side='buy', type='market', time_in_force='day')
        else:
            return "no trade - not right day or stock costs too much"

    return trade_result