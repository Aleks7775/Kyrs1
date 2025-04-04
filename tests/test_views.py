from src.views import time_, date_entry, processing, top_transaction, xlsx_file
import pandas as pd
import datetime
import pytest
import os
import tempfile


def test_time_():
    current_datetime = datetime.datetime.now()
    time = int(current_datetime.strftime("%H"))
    greeting = time_(time)
    if 5 <= time <= 11:
        assert greeting == "Доброе утро"
    elif 12 <= time <= 18:
        assert greeting == "Добрый день"
    elif 19 <= time <= 23:
        assert greeting == "Добрый вечер"
    else:
        assert greeting == "Доброй ночи"


@pytest.fixture()
def transaction():
    return [{'Дата операции': '02.01.2019 17:08:12','Номер карты': '*7197','Сумма операции с округлением': 316.0,'Категория': 'Переводы','Описание': 'Линзомат ТЦ Юность'},
             {'Дата операции': '02.01.2018 17:08:12','Номер карты': '*6197','Сумма операции с округлением': 415.0,'Категория': 'Красота','Описание': 'OOO Balid'},
             {'Дата операции': '02.01.2019 17:08:12','Номер карты': '*4197','Сумма операции с округлением': 854.0,'Категория': 'Топливо','Описание': 'Pskov AZS 12 K2'},
             {'Дата операции': '02.01.2018 17:08:12','Номер карты': '*5197','Сумма операции с округлением': 2500.0,'Категория': 'Супермаркеты','Описание': 'Магнит'},
            {'Дата операции': '02.01.2020 17:08:12','Номер карты': '*5197','Сумма операции с округлением': 4000.0,'Категория': 'Топливо','Описание': 'Pskov AZS 12 K2'},
            {'Дата операции': '02.01.2020 17:08:12','Номер карты': '*5197','Сумма операции с округлением': 3500.0,'Категория': 'Супермаркеты','Описание': 'Лента'}]


def test_date_entry(transaction):
    assert date_entry(transaction, data_time="05.01.2018 10:10:10") == [
        {'Дата операции': '02.01.2018 17:08:12','Номер карты': '*6197','Сумма операции с округлением': 415.0,'Категория': 'Красота','Описание': 'OOO Balid'},
        {'Дата операции': '02.01.2018 17:08:12','Номер карты': '*5197','Сумма операции с округлением': 2500.0,'Категория': 'Супермаркеты','Описание': 'Магнит'}]

    assert date_entry(transaction, data_time="05.01.2019 10:10:10") == [
        {'Дата операции': '02.01.2019 17:08:12','Номер карты': '*7197','Сумма операции с округлением': 316.0,'Категория': 'Переводы','Описание': 'Линзомат ТЦ Юность'},
        {'Дата операции': '02.01.2019 17:08:12','Номер карты': '*4197','Сумма операции с округлением': 854.0,'Категория': 'Топливо','Описание': 'Pskov AZS 12 K2'}]



def test_processing(transaction):
    assert processing(transaction) == [{'cashback': 3.0, 'last_digits': '*7197', 'total_spent': 316.0},
 {'cashback': 4.0, 'last_digits': '*6197', 'total_spent': 415.0},
 {'cashback': 8.0, 'last_digits': '*4197', 'total_spent': 854.0},
 {'cashback': 25.0, 'last_digits': '*5197', 'total_spent': 2500.0},
 {'cashback': 40.0, 'last_digits': '*5197', 'total_spent': 4000.0},
 {'cashback': 35.0, 'last_digits': '*5197', 'total_spent': 3500.0}]

def test_top_transaction(transaction):
    """Проверяет вывод на топ 5 транзакций"""
    assert top_transaction(transaction) == [{'amount': 4000.0,
  'category': 'Топливо',
  'date': '02.01.2020 17:08:12',
  'description': 'Pskov AZS 12 K2'},
 {'amount': 3500.0,
  'category': 'Супермаркеты',
  'date': '02.01.2020 17:08:12',
  'description': 'Лента'},
 {'amount': 2500.0,
  'category': 'Супермаркеты',
  'date': '02.01.2018 17:08:12',
  'description': 'Магнит'},
 {'amount': 854.0,
  'category': 'Топливо',
  'date': '02.01.2019 17:08:12',
  'description': 'Pskov AZS 12 K2'},
 {'amount': 415.0,
  'category': 'Красота',
  'date': '02.01.2018 17:08:12',
  'description': 'OOO Balid'}]


@pytest.fixture
def temp_xlsx_file():
    # Создаем временный XLSX-файл
    df = pd.DataFrame({
        'Дата операции': ['01.01.2020', '02.01.2020'],
        'Сумма': [100, 200]
    })
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    df.to_excel(temp_file.name, index=False)
    yield temp_file.name
    os.remove(temp_file.name)  # Удаляем файл после теста


def test_xlsx_file(temp_xlsx_file):
    # Проверяем, что функция возвращает корректные данные
    result = xlsx_file(temp_xlsx_file)
    expected = [
        {'Дата операции': '01.01.2020', 'Сумма': 100},
        {'Дата операции': '02.01.2020', 'Сумма': 200}
    ]
    assert result == expected
