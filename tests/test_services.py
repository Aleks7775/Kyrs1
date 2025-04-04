import pytest
from src.services import cash_by_category, increased_cashback


@pytest.fixture
def transact():
    """Фикстура с тестовыми данными"""
    return [
        {'Дата операции': '01.10.2020 12:00:00', 'Категория': 'Еда', 'Бонусы (включая кэшбэк)': 10},
        {'Дата операции': '15.10.2020 15:00:00', 'Категория': 'Транспорт', 'Бонусы (включая кэшбэк)': 5},
        {'Дата операции': '01.11.2020 12:00:00', 'Категория': 'Еда', 'Бонусы (включая кэшбэк)': 8}
    ]


def test_increased_cashback(transact):
    """Тестовая функция для increased_cashback"""
    result = increased_cashback(transact, 2020, 10)
    expected = [
        {'Дата операции': '01.10.2020 12:00:00', 'Категория': 'Еда', 'Бонусы (включая кэшбэк)': 10},
        {'Дата операции': '15.10.2020 15:00:00', 'Категория': 'Транспорт', 'Бонусы (включая кэшбэк)': 5}
    ]
    assert result == expected


def test_cash_by_category():
    """Тестовая функция для cash_by_category"""
    list_of_category = [
        {'Категория': 'Еда', 'Бонусы (включая кэшбэк)': 10},
        {'Категория': 'Транспорт', 'Бонусы (включая кэшбэк)': 5},
        {'Категория': 'Еда', 'Бонусы (включая кэшбэк)': 8}
    ]
    result = cash_by_category(list_of_category)
    expected = {
        'Еда': 18,
        'Транспорт': 5
    }
    assert result == expected


def test_integration(transact):
    """Тестовая функция для взаимодействия increased_cashback и cash_by_category"""
    filtered_data = increased_cashback(transact, 2020, 10)
    result = cash_by_category(filtered_data)
    expected = {
        'Еда': 10,
        'Транспорт': 5
    }
    assert result == expected
