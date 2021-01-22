from datetime import datetime, timezone
from unittest import mock

import pytest


@pytest.mark.json_loader
def test_load_data_from_file(json_loader):
    with mock.patch("builtins.open", mock.mock_open(read_data='{"results": "awesome-mock"}'), create=True):
        json_loader.load_data_from_file('persons.json')
    assert json_loader.data == {'results': 'awesome-mock'}


@pytest.mark.json_loader
def test_load_data_from_api(json_loader, requests_mock):
    requests_mock.get(f'https://randomuser.me/api/?results={str(1)}', json={'results': 'awesome-mock'})
    json_loader.load_data_from_api(1)
    assert json_loader.data == {'results': 'awesome-mock'}


@pytest.mark.json_loader
def test_modify_data(json_loader_with_data):
    json_loader_with_data.modify_data()
    with pytest.raises(KeyError):
        picture_field = json_loader_with_data.data['results'][0]['picture']
    assert json_loader_with_data.data['results'][0]['phone'] == '0262351898'
    assert json_loader_with_data.data['results'][0]['cell'] == '0607808311'


@pytest.mark.json_loader
def test_fix_numbers(json_loader_with_data):
    json_loader_with_data.fix_numbers(json_loader_with_data.data['results'][0])
    assert json_loader_with_data.data['results'][0]['phone'] == '0262351898'
    assert json_loader_with_data.data['results'][0]['cell'] == '0607808311'


@pytest.mark.json_loader
def test_clean_string_to_number(json_loader):
    cleaned_number = json_loader.clean_string_to_number('00-00.00,00!00xyz')
    assert cleaned_number == '0000000000'


@pytest.mark.json_loader
def test_add_days_to_birthday(json_loader_with_data):
    json_loader_with_data.add_days_to_birthday(json_loader_with_data.data['results'][0])
    assert json_loader_with_data.data['results'][0]['dtb'] is not None


@pytest.mark.json_loader
def test_calculate_days_to_birthday(json_loader):
    date = datetime.strftime(datetime.now(timezone.utc), '%Y-%m-%dT%H:%M:%S.%f%z')
    dob = {'date': date}
    days_to_birthday = json_loader.calculate_days_to_birthday(dob)
    assert days_to_birthday == 365


@pytest.mark.json_loader
@pytest.mark.freeze_time('2020-03-02')
def test_calculate_days_to_birthday_february_29_leap_year(json_loader):
    dob = {'date': '2020-02-29T00:00:00.000Z'}
    days_to_birthday = json_loader.calculate_days_to_birthday(dob)
    assert days_to_birthday == 363


@pytest.mark.json_loader
def test_day_not_exist(json_loader):
    not_existing_day = json_loader.day_not_exist(2021, 2, 29)
    existing_day = json_loader.day_not_exist(2021, 2, 28)
    assert not_existing_day
    assert not existing_day
