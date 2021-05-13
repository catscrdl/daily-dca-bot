from time import sleep
from alpaca_interface import buy_stock
from motley_fool_content import get_tickers
import yaml
import requests
import csv
import pandas as pd
import json
from io import StringIO

def get_stocks_to_buy(data_source, config):
    if data_source == "motley_fool_stock_advisor":
        res = {}
        for ticker in get_tickers("stock_advisor", config):
            res[ticker] = config['amount']
        return res
    elif data_source == "motley_fool_rule_breakers":
        res = {}
        for ticker in get_tickers("rule_breakers", config):
            res[ticker] = config['amount']
        for custom_amount in config['custom']:
            ticker = list(custom_amount.keys())[0]
            res[ticker] = custom_amount[ticker]
        return res
    elif data_source == "google_sheet":
        res = {}
        default_amount = config['amount']
        csv_url = 'https://docs.google.com/spreadsheets/d/e/{key}/pub?gid=0&single=true&output=csv'.format(key = config['sheet_id'])
        csv_obj = csv.reader(StringIO(requests.get(url=csv_url).content.decode("utf-8") ), delimiter=',')
        it = iter(csv_obj)
        next(it, None)
        for row in it:
            ticker = row[0]
            if row[1] == '':
                res[ticker] = default_amount
            else:
                res[ticker] = row[1]
        return res
    else:
        return {}

def main():
    stocks_to_buy = {}
    enviornment = "paper"
    with open('config.yml') as file:
        config_file = yaml.load(file, Loader=yaml.FullLoader)
        environment = config_file['enviornment']
        sources = config_file['sources']
        for source in sources:
            stocks_to_buy.update(get_stocks_to_buy(source, sources[source]))
    for key in stocks_to_buy.keys():
        print(key)
        try:
            print(buy_stock(key,stocks_to_buy[key],environment))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()