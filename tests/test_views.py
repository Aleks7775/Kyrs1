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
