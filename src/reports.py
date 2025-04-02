import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

file_ = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(file_, '..', 'data', 'operations.xlsx')


def read_df_excel(file):
    '''Читаем Excel-файл'''
    with open(file, 'r', encoding='utf-8'):
        operations_xls = pd.read_excel(file)
    return operations_xls


transactions = read_df_excel(file)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    if date is None:
        date = pd.Timestamp.now()
    else:
        date = pd.Timestamp(date)
    start_date = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S"
    )
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]
    logging.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")
    return filtered_transactions


print(spending_by_category(transactions, "Супермаркеты", "01.01.2019"))
