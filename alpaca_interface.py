import yaml
import os
import requests

def buy_stock(symbol, amount, environment):
    with open('config.yml') as file:
        creds = yaml.load(file, Loader=yaml.FullLoader)
        os.environ["APCA_API_KEY_ID"] = creds[environment]['api_key_id']
        os.environ["APCA_API_SECRET_KEY"] = creds[environment]['secret_key']
        os.environ["APCA_API_BASE_URL"] = creds[environment]['endpoint']

    api = REST()

    api.submit_order(symbol = symbol, notional= amount , side='buy', type='market', time_in_force='day')