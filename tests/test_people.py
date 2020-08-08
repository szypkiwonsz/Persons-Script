import pytest

import models
from data_getter import DataFromFile
from data_loader import DataLoader
from people import PercentagePeople, AverageAge, MostCommonValue


@pytest.fixture(scope='module')
def percentage():
    percentage = PercentagePeople(':memory:')
    file = DataFromFile('./persons.json')
    data = file.get_persons_data()
    loader = DataLoader(':memory:', data)
    loader.insert_to_database()
    yield percentage
    loader.db.close()


@pytest.fixture(scope='module')
def average():
    average = AverageAge(':memory:', '')
    file = DataFromFile('./persons.json')
    data = file.get_persons_data()
    loader = DataLoader(':memory:', data)
    loader.insert_to_database()
    yield average
    loader.db.close()


@pytest.fixture(scope='module')
def most_common_city():
    city = MostCommonValue(':memory:', 5, models.Location, models.Location.city)
    file = DataFromFile('./persons.json')
    data = file.get_persons_data()
    loader = DataLoader(':memory:', data)
    loader.insert_to_database()
    yield city
    loader.db.close()


def test_gender_percentage(percentage):
    assert percentage.gender_percentage('female') == 50
    assert percentage.gender_percentage('male') == 50


def test_calculate_percentage(percentage):
    assert percentage.calculate_percentage(2, 10) == 20
    with pytest.raises(ValueError):
        percentage.calculate_percentage(0, 0)


def test_get_only_gender_age(average):
    assert average.get_only_gender_age('male') == 24450
    assert average.get_only_gender_age('female') == 24658


def test_get_all_people_age(average):
    assert average.get_all_people_age() == 49108


def test_calculate_average_gender(average):
    assert average.calculate_average_gender('male') == 49
    assert average.calculate_average_gender('female') == 50


def test_calculate_all_people_average(average):
    assert average.calculate_all_people_average() == 49


def test_select_most_common_values(most_common_city):
    values = most_common_city.select_most_common_values()
    names = ['Gisborne', 'Lower Hutt', 'Napier', 'Queanbeyan', 'Van']
    counted = [7, 5, 5, 5, 5]
    for i, value in enumerate(values):
        assert value.name == names[i]
        assert value.counted == counted[i]
