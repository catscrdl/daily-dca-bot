from time import sleep
from alpaca_interface import buy_stock
from motley_fool_content import get_tickers

def get_stocks_to_buy(data_source):
    if data_source == "motley_fool_premium":
        return get_motley_fool_premium_stocks()
    elif data_source == "gsheet":
        return get_gsheet_stocks()
    else:
        exit(1)

def main():
    #stocks_to_buy = []
    #for data_source in collect_data_sources()
    #    stocks_to_buy = get_stocks_to_buy(data_source)
    #buy_stocks(stocks_to_buy)
    sa_tickers = get_tickers("stock_advisor")
    rb_tickers = get_tickers("rule_breakers")

    #results = '{"stock_advisor":'+sa_tickers+', "rule_breakers":'+rb_tickers+'}'
    #result_json_object = json.dumps(list(results))
    #print(result_json_object)

    print(f"Stock Advisor Picks: {sa_tickers}")
    print(f"Rule Breakers Picks: {rb_tickers}")

    buy_stock("AAPL",150,"paper")

if __name__ == "__main__":
    main()