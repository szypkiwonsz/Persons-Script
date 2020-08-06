import pytest

from database import Database


@pytest.fixture(scope='module')
def database():
    database = Database(':memory:')
    yield database


def test_existing_tables(database):
    tables = [
        'coordinates', 'dob', 'id', 'location', 'login', 'name', 'person', 'picture', 'registered', 'street', 'timezone'
    ]
    assert database.db.get_tables() == tables
    return tables


def test_existing_columns(database):
    tables = test_existing_tables(database)
    columns = {
        'coordinates': ['id', 'location_id', 'latitude', 'longitude'],
        'dob': ['id', 'person_id', 'date', 'age'],
        'id': ['id', 'person_id', 'name', 'value'],
        'location': ['id', 'person_id', 'city', 'state', 'country', 'postcode'],
        'login': ['id', 'person_id', 'uuid', 'username', 'password', 'salt', 'md5', 'sha1', 'sha256'],
        'name': ['id', 'person_id', 'title', 'first', 'last'],
        'person': ['id', 'gender', 'email', 'phone', 'cell', 'nat'],
        'picture': ['id', 'person_id', 'large', 'medium', 'thumbnail'],
        'registered': ['id', 'person_id', 'date', 'age'],
        'street': ['id', 'location_id', 'number', 'name'],
        'timezone': ['id', 'location_id', 'offset', 'description']
    }
    for i, table in enumerate(tables):
        for j, column in enumerate(columns[table]):
            assert database.db.get_columns(table)[j][0] == column


def test_connection(database):
    assert database.db.is_closed() == False


def test_close_connection(database):
    database.close_connection()
    assert database.db.is_closed() == True


def test_reopen_connection(database):
    database.close_connection()
    assert database.db.is_closed() == True
    database.open_connection()
    assert database.db.is_closed() == False
