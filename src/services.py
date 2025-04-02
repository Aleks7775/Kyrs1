import datetime
import json
import os
from datetime import datetime

from functions import xlsx_file

file_ = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(file_, '..', 'data', 'operations.xlsx')

transactions = xlsx_file(file)


def increased_cashback(transaction, year, month):
    """Функция фильтрует данные за год и месяц"""
    filtered_data = [transaction for transaction in transactions
                     if datetime.strptime(transaction['Дата операции'],'%d.%m.%Y %H:%M:%S').year == year
                     and datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').month == month]
    return filtered_data


def cash_by_category(list_of_category):
    """Функция выводит данные сколько на каждой категории можно было заработать кешбэка в указанном месяце года"""
    cashback_by_category = {}
    for i in list_of_category:
        category = i["Категория"]
        cash = i["Бонусы (включая кэшбэк)"]
        if category not in cashback_by_category:
            cashback_by_category[category] = 0
        cashback_by_category[category] += cash
    return cashback_by_category


k = increased_cashback(transactions, 2020, 1)
result = cash_by_category(k)
json_data = json.dumps(result, ensure_ascii=False, indent=4)
print(json_data)
