import os

import pandas as pd

file_ = os.path.dirname(os.path.abspath(__file__))
file_xlsx = os.path.join(file_, '..', 'data', 'operations.xlsx')


def xlsx_file(file):
    """Cчитывает финансовые операции из XLSX-файлов"""
    try:
        pd_xlsx = pd.read_excel(file)
        tr = pd_xlsx.to_dict('records')
        return tr
    except FileNotFoundError:
        return "отсутствует файл"
