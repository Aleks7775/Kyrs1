import pandas as pd


def xlsx_file(file):
    """Cчитывает финансовые операции из XLSX-файлов"""
    try:
        pd_xlsx = pd.read_excel(file)
        tr = pd_xlsx.to_dict('records')
        return tr
    except FileNotFoundError:
        return "отсутствует файл"
