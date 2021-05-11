import yaml
import os
import requests

ENVIRONMENT = "paper"

with open('creds.yml') as file:
    creds = yaml.load(file, Loader=yaml.FullLoader)
    os.environ["APCA_API_KEY_ID"] = creds[ENVIRONMENT]['api_key_id']
    os.environ["APCA_API_SECRET_KEY"] = creds[ENVIRONMENT]['secret_key']
    os.environ["APCA_API_BASE_URL"] = creds[ENVIRONMENT]['endpoint']

api = REST()

api.submit_order(symbol = 'AAPL', notional=150, side='buy', type='market', time_in_force='day')