import datetime

from datetime import datetime


def increased_cashback(transactions, year, month):
    """Функция фильтрует данные за год и месяц"""
    filtered_data = [transaction for transaction in transactions
                     if datetime.strptime(transaction['Дата операции'],'%d.%m.%Y %H:%M:%S').year == year
                     and datetime.strptime(transaction['Дата операции'],  '%d.%m.%Y %H:%M:%S').month == month]
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
