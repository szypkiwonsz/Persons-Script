import sys

import pytest
from peewee import SqliteDatabase

sys.path.append('./persons')

from data_loader import JsonLoader
from database import Person, DatabaseHandler
from password_rater import Password, PasswordRater
from query_handler import QueryHandler, CommonElementsHandler, CommonCitiesHandler, CommonPasswordsHandler, \
    GenderHandler, DateHandler, PasswordHandler


@pytest.fixture()
def json_loader():
    temp_json_loader = JsonLoader()
    return temp_json_loader


@pytest.fixture()
def persons_data():
    persons_data = [{
        "gender": "female",
        "name": {
            "title": "Miss",
            "first": "Louane",
            "last": "Vidal"
        },
        "location": {
            "street": {
                "number": 2479,
                "name": "Place du 8 Février 1962"
            },
            "city": "Avignon",
            "state": "Vendée",
            "country": "France",
            "postcode": 78276,
            "coordinates": {
                "latitude": "2.0565",
                "longitude": "95.2422"
            },
            "timezone": {
                "offset": "+1:00",
                "description": "Brussels, Copenhagen, Madrid, Paris"
            }
        },
        "email": "louane.vidal@example.com",
        "login": {
            "uuid": "9f07341f-c7e6-45b7-bab0-af6de5a4582d",
            "username": "angryostrich988",
            "password": "r2d2",
            "salt": "B5ywSDUM",
            "md5": "afce5fbe8f32bcec1a918f75617ab654",
            "sha1": "1a5b1afa1d9913cf491af64ce78946d18fea6b04",
            "sha256": "0124895aa1e6e5fb0596fad4c413602e0922e8a8c2dc758bbdb3fa070ad25a07"
        },
        "dob": {
            "date": "1966-06-26T11:50:25.558Z",
            "age": 54
        },
        "registered": {
            "date": "2016-08-11T06:51:52.086Z",
            "age": 4
        },
        "phone": "02-62-35-18-98",
        "cell": "06-07-80-83-11",
        "id": {
            "name": "INSEE",
            "value": "2NNaN01776236 16"
        },
        "picture": {
            "large": "https://randomuser.me/api/portraits/women/88.jpg",
            "medium": "https://randomuser.me/api/portraits/med/women/88.jpg",
            "thumbnail": "https://randomuser.me/api/portraits/thumb/women/88.jpg"
        },
        "nat": "FR"
    }]
    return persons_data


@pytest.fixture()
def json_loader_with_data(persons_data):
    temp_json_loader = JsonLoader()
    temp_json_loader.data['results'] = persons_data
    return temp_json_loader


@pytest.fixture()
def database():
    test_db = SqliteDatabase(':memory:')
    test_db.bind([Person], bind_refs=False, bind_backrefs=False)
    return test_db


@pytest.fixture()
def database_handler(database):
    temp_database_handler = DatabaseHandler()
    temp_database_handler.db = database
    return temp_database_handler


@pytest.fixture()
def database_with_data(database_handler, json_loader_with_modified_data):
    database_handler.insert_data_into_person(json_loader_with_modified_data.data['results'])
    return database_handler


@pytest.fixture()
def json_loader_with_modified_data(json_loader_with_data):
    json_loader_with_data.modify_data()
    return json_loader_with_data


@pytest.fixture()
def password():
    password = Password('Qwertyu1?')
    return password


@pytest.fixture()
def password_rater():
    temp_password_rater = PasswordRater('Qwertyu1?')
    return temp_password_rater


@pytest.fixture()
def query_handler():
    temp_query_handler = QueryHandler()
    return temp_query_handler


@pytest.fixture()
def common_elements_handler():
    temp_common_elements_handler = CommonElementsHandler('location', 'country')
    return temp_common_elements_handler


@pytest.fixture()
def common_cities_handler():
    temp_common_cities_handler = CommonCitiesHandler()
    return temp_common_cities_handler


@pytest.fixture()
def common_passwords_handler():
    temp_common_passwords_handler = CommonPasswordsHandler()
    return temp_common_passwords_handler


@pytest.fixture()
def gender_handler():
    temp_gender_handler = GenderHandler()
    return temp_gender_handler


@pytest.fixture()
def date_handler():
    temp_date_handler = DateHandler('1900-01-01', '2021-01-01')
    return temp_date_handler


@pytest.fixture()
def password_handler():
    temp_password_handler = PasswordHandler()
    return temp_password_handler
