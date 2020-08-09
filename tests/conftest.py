import sys

import pytest

sys.path.append('./persons')

import models
from database import Database
from data_loader import DataLoader
from people import PercentagePeople, AverageAge, MostCommonValue, RangeValueParameter, MostPointedValue
from utils import get_persons_data
from data_getter import DataFromFile


@pytest.fixture()
def database():
    database = Database(':memory:')
    yield database
    database.db.close()


@pytest.fixture()
def loader():
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    return loader


@pytest.fixture()
def file():
    file = DataFromFile('./persons.json')
    return file


@pytest.fixture(scope='module')
def percentage():
    percentage = PercentagePeople(':memory:')
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    loader.insert_to_database()
    yield percentage
    loader.db.close()


@pytest.fixture(scope='module')
def average():
    average = AverageAge(':memory:', '')
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    loader.insert_to_database()
    yield average
    loader.db.close()


@pytest.fixture(scope='module')
def most_common_city():
    city = MostCommonValue(':memory:', 5, models.Location, models.Location.city)
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    loader.insert_to_database()
    yield city
    loader.db.close()


@pytest.fixture(scope='module')
def most_common_password():
    password = MostCommonValue(':memory:', 5, models.Login, models.Login.password)
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    loader.insert_to_database()
    yield password
    loader.db.close()


@pytest.fixture(scope='module')
def range_dob():
    range_dob = RangeValueParameter(':memory:', '1950-08-02', '1950-12-02', models.Dob, models.Dob.date)
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    loader.insert_to_database()
    yield range_dob
    loader.db.close()


@pytest.fixture(scope='module')
def safest_password():
    safest_password = MostPointedValue(':memory:', models.Login, models.Login.password)
    file = DataFromFile('./persons.json')
    data = file.get_json_data()
    persons_data = get_persons_data(data)
    loader = DataLoader(':memory:', persons_data)
    loader.insert_to_database()
    yield safest_password
    loader.db.close()
