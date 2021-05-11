from time import sleep
from alpaca_interface import buy_stock
from motley_fool_content import get_tickers
import yaml

def get_stocks_to_buy(data_source, credentials):
    if data_source == "motley_fool_stock_advisor":
        return get_tickers("stock_advisor", credentials)
    elif data_source == "motley_fool_rule_breakers":
        return get_tickers("rule_breakers", credentials)
    else:
        exit(1)

def main():
    stocks_to_buy = []
    enviornment = "paper"
    notional = 0
    with open('config.yml') as file:
        config_file = yaml.load(file, Loader=yaml.FullLoader)
        environment = config_file['enviornment']
        notional =  config_file['notional']
        sources = config_file['sources']
        for source in sources:
            stocks_to_buy.extend(get_stocks_to_buy(source, sources[source]))
    stocks_to_buy = set(stocks_to_buy)
    for stock in stocks_to_buy:
        print(stock)
        try:
            print(buy_stock(stock,notional,environment))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()