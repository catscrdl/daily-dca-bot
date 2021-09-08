from time import sleep
from alpaca_interface import buy_stock
from alpaca_interface import determine_buy_the_dip
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
        count = 0
        while res == {}:
            try:
                for ticker in get_tickers("stock_advisor", config):
                    res[ticker] = config['amount']
                if 'custom' in config:
                    for custom_amount in config['custom']:
                        ticker = list(custom_amount.keys())[0]
                        res[ticker] = custom_amount[ticker]
            except Exception as e:
                print('Failure retrieving stock advisor picks. Attempt ' + count)
                count += 1
                print(e)
        return res
    elif data_source == "motley_fool_rule_breakers":
        res = {}
        count = 0
        while res == {}:
            try:
                for ticker in get_tickers("rule_breakers", config):
                    res[ticker] = config['amount']
                if 'custom' in config:
                    for custom_amount in config['custom']:
                        ticker = list(custom_amount.keys())[0]
                        res[ticker] = custom_amount[ticker]
            except Exception as e:
                print('Failure retrieving rule breaker picks. Attempt ' + count)
                count += 1
                print(e)
        return res
    elif data_source == "google_sheet":
        res = {}
        default_amount = config['amount']
        csv_url = config['sheet_url']
        csv_obj = csv.reader(StringIO(requests.get(url=csv_url).content.decode("utf-8") ), delimiter=',')
        it = iter(csv_obj)
        next(it, None)
        for row in it:
            ticker = row[0]
            if row[1] == '':
                res[ticker] = int(default_amount)
            else:
                res[ticker] = int(row[1])
        return res
    else:
        return {}

def get_stocks_to_not_buy(config):
    res = []
    csv_url = config['sheet_url']
    csv_obj = csv.reader(StringIO(requests.get(url=csv_url).content.decode("utf-8") ), delimiter=',')
    it = iter(csv_obj)
    next(it, None)
    for row in it:
        res = res + row
    return res

def main():
    stocks_to_buy = {}
    stocks_to_not_buy = []
    enviornment = "paper"
    with open('config.yml') as file:
        config_file = yaml.load(file, Loader=yaml.FullLoader)
        environment = config_file['environment']
        sources = config_file['sources']
        for source in sources:
            if source == "do_not_buy_list":
                stocks_to_not_buy = get_stocks_to_not_buy(sources[source])
            else:
                stocks_to_buy.update(get_stocks_to_buy(source, sources[source]))
    print('Stocks to buy and amounts')
    print(stocks_to_buy)
    for key in stocks_to_buy.keys():
        print(key)
        if key not in stocks_to_not_buy:
            try:
                do_we_dip_buy = determine_buy_the_dip(key)
                print("are we buying the dip? " + (str(do_we_dip_buy)))
                print(buy_stock(key,stocks_to_buy[key],environment, do_we_dip_buy))
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()