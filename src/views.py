import datetime
import json
import os
from operator import itemgetter

import requests
from dotenv import load_dotenv

from utils import xlsx_file

load_dotenv()
api_key_currency = os.getenv("API_KEY_currency")
api_key_stocks = os.getenv("API_KEY_stocks")

file_ = os.path.dirname(os.path.abspath(__file__))
file_xlsx = os.path.join(file_, '..', 'data', 'operations.xlsx')
stocks_file = os.path.join(file_, '..', 'user_seting.json')

with open(stocks_file, 'r') as f:
    user_settings = json.load(f)

current_datetime = datetime.datetime.now()
formatted_datetime = int(current_datetime.strftime("%H"))
transactions = xlsx_file(file_xlsx)


def time_(time):
    """Приветствие в зависимости от текущего времени"""
    if 5 <= time <= 11:
        return "Доброе утро"
    elif 12 <= time <= 18:
        return "Добрый день"
    elif 19 <= time <= 23:
        return "Добрый вечер"
    return "Доброй ночи"


greetings = time_(formatted_datetime)


def date_entry(transaction):
    """Фильтрует данные по дате и времени"""
    data_time = "03.01.2020 10:10:10"
#    data_time = input("Введите дату и время в формате 'DD.MM.YYYY HH:MM:SS' ")
    end_date = datetime.datetime.strptime(data_time, '%d.%m.%Y %H:%M:%S')
    start_date = end_date.replace(day=1)
    operation = [item for item in transaction if
                 (datetime.datetime.strptime(item["Дата операции"], "%d.%m.%Y %H:%M:%S") >= start_date) and
                 (datetime.datetime.strptime(item["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date)]
    return operation


data = date_entry(transactions)


def processing(data):
    """Выводит данные по каждой карте {последние 4 цифры карты, общая сумма расходов,
     кешбэк (1 рубль на каждые 100 рублей)}"""
    operation_cards = []
    for i in data:
        operation_cards.append({
            "last_digits": i["Номер карты"],
            "total_spent": i["Сумма операции с округлением"],
            "cashback": i['Сумма операции с округлением']//100,
        })
    return operation_cards


cards_dict = processing(data)
json_cards = json.dumps(cards_dict)


def top_transaction(transaction):
    """Выводит топ-5 транзакций по сумме платежа"""
    sorted_transactions = sorted(transaction, key=itemgetter('Сумма операции с округлением'), reverse=True)
    top_five = sorted_transactions[:5]
    result = []
    for i in top_five:
        result.append({
            "date": i['Дата операции'],
            "amount": i['Сумма операции с округлением'],
            "category": i['Категория'],
            "description": i['Описание']
        })
    return result


top_transactions = top_transaction(data)
top_json_str = json.dumps(top_transactions, ensure_ascii=False, indent=4)


def currency_and_shares():
    """Выводит курс валют"""
    new_currency = []
    response = requests.get(f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={api_key_currency}")
    data_ = response.json()
    new_currency.append({"currency": "USD", "rate": data_["data"]["USDRUB"]})
    new_currency.append({"currency": "EUR", "rate": data_["data"]["EURRUB"]})
    return new_currency


currency = currency_and_shares()


def share_price():
    """Выводит курс акций"""
    stocks = user_settings.get('user_stocks', [])
    stocks_price = []
    for i in stocks:
        response = requests.get(f"https://www.alphavantage.co/"
                                f"query?function=GLOBAL_QUOTE&symbol={i}&apikey={api_key_stocks}")
        data = response.json()
        stocks_price.append({
            "stocks": i,
            "price": data['Global Quote']['05. price']
        })
    return stocks_price


stocks_prices = share_price()


js = {"greetings": greetings, "cards": cards_dict, "top_transactions": top_transactions,
      "currency_rates": currency, "stocks_price": stocks_prices}
js_ = json.dumps(js, ensure_ascii=False, indent=4)
print(js_)
