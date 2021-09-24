import pdb
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs
import yaml
import json
import re

def get_tickers(service, credentials):
    email = credentials['email']
    password = credentials['password']

    #with open('config.yml') as file:
    #    creds = yaml.load(file, Loader=yaml.FullLoader)
    #    email = creds[service]['email']
    #    password = creds[service]['password']

    # Set global session user agent once
    s = requests.Session()
    s.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"}

    r = s.head('https://www.fool.com/premium/auth/authenticate', allow_redirects=True)
    site = s.get(r.url)
    csrf_token = site.cookies['_csrf']
    parsed_url = urlparse(r.url)
    parsed_query = parse_qs(parsed_url.query)
    client_id = parsed_query['client'][0]
    nonce = parsed_query['nonce'][0]
    state = parsed_query['state'][0]
    data = {
        "client_id":client_id,
        "redirect_uri":"https://www.fool.com/premium/auth/callback/",
        "tenant":"fool",
        "response_type":"code",
        "scope":"openid email profile",
        "_csrf":csrf_token,
        "state":state,
        "_intstate":"deprecated",
        "nonce":nonce,
        "password":password,
        "connection":"TMF-Reg-API",
        "username":email
    }
    login_response = s.post("https://auth.fool.com/usernamepassword/login",data=data)
    bs_content = bs(login_response.text, "html.parser")
    wresult_token = bs_content.find("input",{"name":"wresult"})["value"]
    wctx_token = bs_content.find("input",{"name":"wctx"})["value"]
    headers = {
        "Origin": "https://auth.fool.com",
        "Referer":r.url
    }
    data = {
        "wa":"wsignin1.0",
        "wresult":wresult_token,
        "wctx":wctx_token
    }
    login_response = s.post("https://auth.fool.com/login/callback",data=data, headers=headers, allow_redirects = True)
    bs_content = bs(login_response.text, "html.parser")
    recommendations = bs_content.find_all("div",{"class":"watch-state-button"})
    tickers = []
    for recommendation in recommendations:
        tickers.append(json.dumps(recommendation.text).split()[1])
    tickers = set(tickers)

    new_rec_tickers = []
    try:
        new_recs = bs_content.find_all("th",{"class":"primary"})
        for new_rec in new_recs:
            if "New Stock" in new_rec.text:
                z = re.search("(?=\/).*(?<=.png)", str(new_rec))
                if z is not None:
                    new_rec_tickers.append(z.group(0).split('/')[-1].split('.')[0])
    except Exception as e:
        print("Failed to get new recommendations")
        print(e)
    print("new recommendations")
    print(new_rec_tickers)
    return list(tickers), new_rec_tickers