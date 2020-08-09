from utils import *


def test_day_not_exist():
    assert day_not_exist(1996, 2, 29) is None
    assert day_not_exist(2021, 2, 29) is True


def test_calculate_days_to_birthday():
    today = datetime(datetime.today().year, datetime.today().month, datetime.today().day).date()
    yesterday = datetime(datetime.today().year, datetime.today().month, datetime.today().day - 1).date()
    tomorrow = datetime(datetime.today().year, datetime.today().month, datetime.today().day + 1).date()
    dates = [
        today, yesterday, tomorrow
    ]
    correctly_days = [
        365, 364, 1
    ]
    for date, correctly_day in zip(dates, correctly_days):
        days_to_birthday = calculate_days_to_birthday(date)
        assert days_to_birthday == correctly_day
