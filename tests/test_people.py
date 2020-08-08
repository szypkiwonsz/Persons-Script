import pytest

from data_getter import DataFromFile
from data_loader import DataLoader
from people import PercentagePeople


@pytest.fixture(scope='module')
def people():
    people = PercentagePeople(':memory:')
    file = DataFromFile('./persons.json')
    data = file.get_persons_data()
    loader = DataLoader(':memory:', data)
    loader.insert_to_database()
    yield people
    loader.db.close()
    people.db.close()


def test_gender_percentage(people):
    assert people.gender_percentage('female') == 50
    assert people.gender_percentage('male') == 50


def test_count_only_gender(people):
    assert people.count_only_gender('male') == 502
    assert people.count_only_gender('female') == 498


def test_count_all_people(people):
    assert people.count_all_people() == 1000


def test_calculate_percentage(people):
    assert people.calculate_percentage(2, 10) == 20
    with pytest.raises(ValueError):
        people.calculate_percentage(0, 0)
