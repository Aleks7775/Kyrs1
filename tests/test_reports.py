import pytest
from src.reports import read_df_excel
from src.reports import spending_by_category
import os


file_ = os.path.dirname(os.path.abspath(__file__))
file_xlsx = os.path.join(file_, '..', 'data', 'operations.xlsx')


@pytest.fixture(scope='module')
def transactions():
    df = read_df_excel(file_xlsx)
    df['Категория'] = df['Категория'].str.strip()
    return df


@pytest.mark.parametrize('category, expected_length', [
    ('Супермаркеты', 131),
    ('Транспорт', 5),
])
def test_spending_by_category(transactions, category, expected_length):
    result = spending_by_category(transactions, category, date="2021-12-31")
    assert len(result) == expected_length
