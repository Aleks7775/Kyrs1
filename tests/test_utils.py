from unittest.mock import patch, mock_open, Mock
import pytest
import requests
import json
from src.utils import currency_and_shares, share_price


@patch('requests.get')
def test_currency_and_shares(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": {
            "USDRUB": 73.5,
            "EURRUB": 86.7
        }
    }

    expected_result = [
        {"currency": "USD", "rate": 73.5},
        {"currency": "EUR", "rate": 86.7}
    ]
    """Проверяем ожидаемый результат"""
    assert currency_and_shares() == expected_result

    """Проверяем статус-код ответа"""
    result = currency_and_shares()
    assert mock_get.return_value.status_code == 200
    assert result == expected_result


@patch('requests.get')
def test_share_price(mock_get):
    mock_get.return_value.json.return_value = {
        'Global Quote': {
            '05. price': '200.0'
        }
    }

    result_currency = [
        {"stocks": "AAPL", "price": '200.0'},
        {"stocks": "AMZN", "price": '200.0'},
        {"stocks": "GOOGL", "price": '200.0'},
        {"stocks": "MSFT", "price": '200.0'},
        {"stocks": "TSLA", "price": '200.0'}]
    """Проверяем ожидаемый результат"""
    assert share_price() == result_currency
