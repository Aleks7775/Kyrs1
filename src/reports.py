import logging
import os
from typing import Optional, Any
import pandas as pd
import functools
import json


def read_df_excel(file):
    '''Читаем Excel-файл'''
    with open(file, 'r', encoding='utf-8'):
        operations_xls = pd.read_excel(file)
    return operations_xls


file_ = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(file_, '..', 'data', 'operations.xlsx')
file_ = read_df_excel(file)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> (
        list)[dict[Any, Any]]:
    """
    Возвращает траты по заданной категории за последние три месяца.
    """
    if date is None:
        date = pd.Timestamp.now()
    else:
        date = pd.Timestamp(date)

    start_date = date - pd.DateOffset(months=3)
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S")
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)]
    df_dict = filtered_transactions.to_dict(orient='records')
    result = []
    for i in df_dict:
        result.append({i["Категория"]: i["Сумма операции с округлением"]})
    logging.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")
    return result


def save_to_file(file_name="default_report.json"):
    """Декоратор для записи результата функции в файл."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, 'w') as f:
                json.dump(result, f, ensure_ascii=False)
            return result
        return wrapper
    return decorator


@save_to_file()
def spending_by_category_report(transactions, category, date):
    """Обертка для функции spending_by_category"""
    return spending_by_category(transactions, category, date)
