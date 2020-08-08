import pytest

from data_getter import DataFromFile


@pytest.fixture()
def file():
    file = DataFromFile('./persons.json')
    return file


def test_get_json_data(file):
    data = file.get_json_data()
    assert data['results'][0]['cell'] == '06-07-80-83-11'
    assert data['results'][-1]['email'] == 'tim.bardsen@example.com'
    return data


def test_get_persons_data(file):
    data = test_get_json_data(file)
    persons_data = data['results']
    assert persons_data[0]['cell'] == '06-07-80-83-11'
    assert persons_data[-1]['email'] == 'tim.bardsen@example.com'
