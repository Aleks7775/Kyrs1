import datetime
import os
from operator import itemgetter
import pandas as pd


file_ = os.path.dirname(os.path.abspath(__file__))
file_xlsx = os.path.join(file_, '..', 'data', 'operations.xlsx')


current_datetime = datetime.datetime.now()
formatted_datetime = int(current_datetime.strftime("%H"))


def xlsx_file(file):
    """Cчитывает финансовые операции из XLSX-файлов"""
    try:
        pd_xlsx = pd.read_excel(file)
        tr = pd_xlsx.to_dict('records')
        return tr
    except FileNotFoundError:
        return "отсутствует файл"


def time_(time):
    """Приветствие в зависимости от текущего времени"""
    if 5 <= time <= 11:
        return "Доброе утро"
    elif 12 <= time <= 18:
        return "Добрый день"
    elif 19 <= time <= 23:
        return "Добрый вечер"
    return "Доброй ночи"


def date_entry(transaction, data_time):
    """Фильтрует данные по дате и времени"""
    end_date = datetime.datetime.strptime(data_time, '%d.%m.%Y %H:%M:%S')
    start_date = end_date.replace(day=1)
    operation = [item for item in transaction if
                 (datetime.datetime.strptime(item["Дата операции"], "%d.%m.%Y %H:%M:%S") >= start_date) and
                 (datetime.datetime.strptime(item["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date)]
    return operation


def processing(data_cards):
    """Выводит данные по каждой карте {последние 4 цифры карты, общая сумма расходов,
     кешбэк (1 рубль на каждые 100 рублей)}"""
    operation_cards = []
    for i in data_cards:
        operation_cards.append({
            "last_digits": i["Номер карты"],
            "total_spent": i["Сумма операции с округлением"],
            "cashback": i['Сумма операции с округлением']//100,
        })
    return operation_cards


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
