from datetime import datetime

import pytest

import models
from data_getter import DataFromFile
from data_loader import DataLoader


@pytest.fixture()
def loader():
    file = DataFromFile('./script/persons.json')
    data = file.get_persons_data()
    loader = DataLoader(':memory:', data)
    return loader


def test_add_days_to_birthday_to_data(loader):
    new_data_list = loader.add_days_to_birthday_to_data()
    for data in new_data_list:
        assert 'days_to_birthday' in data['dob']


def test_calculate_days_to_birthday(loader):
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
        days_to_birthday = loader.calculate_days_to_birthday(date)
        assert days_to_birthday == correctly_day


def test_day_not_exist(loader):
    assert loader.day_not_exist(1996, 2, 29) is None
    assert loader.day_not_exist(2021, 2, 29) == True


def test_add_cleaned_phone_number_to_data(loader):
    new_data_list = loader.add_cleaned_phone_number_to_data()
    assert new_data_list[0]['phone'] == '0262351898'
    assert new_data_list[-2]['cell'] == '0753022945'


def test_clean_string_to_number(loader):
    assert loader.clean_string_to_number('-23-54-6x') == '23546'
    assert loader.clean_string_to_number('00[;75') == '0075'


def test_insert_to_database(loader):
    database_models = loader.models
    for model in database_models:
        loader.drop_table(model)
    loader.initialize()
    loader.add_database_field(models.Dob, 'dob', 'days_to_birthday', models.IntegerField(null=True))
    loader.add_days_to_birthday_to_data()
    loader.add_cleaned_phone_number_to_data()
    loader.drop_table(models.Picture)
    loader.insert_to_database()
    query = models.Person.select()
    assert query.count() != 0
