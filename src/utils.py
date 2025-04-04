import datetime
import json
import os
from operator import itemgetter
import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()
api_key_currency = os.getenv("API_KEY_currency")
api_key_stocks = os.getenv("API_KEY_stocks")


file_ = os.path.dirname(os.path.abspath(__file__))
file_xlsx = os.path.join(file_, '..', 'data', 'operations.xlsx')
stocks_file = os.path.join(file_, '..', 'user_seting.json')


with open(stocks_file, 'r') as f:
    user_settings = json.load(f)


def currency_and_shares():
    """Выводит курс валют"""
    new_currency = []
    url = f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={api_key_currency}"
    response = requests.get(url)
    data_ = response.json()
    new_currency.append({"currency": "USD", "rate": data_["data"]["USDRUB"]})
    new_currency.append({"currency": "EUR", "rate": data_["data"]["EURRUB"]})
    return new_currency


def share_price():
    """Выводит курс акций"""
    stocks = user_settings.get('user_stocks', [])
    stocks_price = []
    for i in stocks:
        response = requests.get(f"https://www.alphavantage.co/"
                                f"query?function=GLOBAL_QUOTE&symbol={i}&apikey={api_key_stocks}")
        data_shares = response.json()
        stocks_price.append({
            "stocks": i,
            "price": data_shares['Global Quote']['05. price']
        })
    return stocks_price
