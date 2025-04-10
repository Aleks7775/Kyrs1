from src.views import xlsx_file, time_, date_entry, processing, top_transaction
from src.utils import currency_and_shares, share_price
from src.services import increased_cashback, cash_by_category
from src.reports import read_df_excel, spending_by_category
import datetime
import json
import os


file_ = os.path.dirname(os.path.abspath(__file__))
file_xlsx = os.path.join(file_, '..', 'data', 'operations.xlsx')
transactions = xlsx_file(file_xlsx)
transaction = read_df_excel(file_xlsx)

current_datetime = datetime.datetime.now()
formatted_datetime = int(current_datetime.strftime("%H"))


def main(date_input="05.01.2018 10:10:10"):
    """Принимает на вход строку с датой и временем и возвращает JSON-ответ"""
    greetings = time_(formatted_datetime)
    data = date_entry(transactions, date_input)
    cards_dict = processing(data)
    top_transactions = top_transaction(data)
    currency = currency_and_shares()
    stocks_prices = share_price()
    json_ = {"greetings": greetings, "cards": cards_dict, "top_transactions": top_transactions,
             "currency_rates": currency, "stocks_price": stocks_prices}
    json_answer = json.dumps(json_, ensure_ascii=False, indent=4)
    return json_answer


def services(year=2020, month=10):
    """Функция фильтрует данные за год и месяц и возвращает JSON-ответ"""
    filtration = increased_cashback(transactions, year, month)
    result = cash_by_category(filtration)
    json_data = json.dumps(result, ensure_ascii=False, indent=4)
    return json_data


def reports_by_category(category="Супермаркеты", date="01.01.2019"):
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)
     и возвращает JSON-ответ а также записывает отчет в файл"""
    reports = spending_by_category(transaction, category, date)
    json_reports = json.dumps(reports, ensure_ascii=False, indent=4)
    return json_reports


if __name__ == "__main__":
    main()
    services_data = services(year=2020, month=10)
    print(services_data)
    reports_data = reports_by_category(category="Супермаркеты", date="01.01.2019")
    print(reports_data)
