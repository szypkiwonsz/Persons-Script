import models


def test_existing_tables(database):
    tables = [
        'coordinates', 'dob', 'id', 'location', 'login', 'name', 'person', 'registered', 'street', 'timezone'
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
    assert database.db.is_closed() is False


def test_close_connection(database):
    database.close_connection()
    assert database.db.is_closed() is True


def test_reopen_connection(database):
    database.close_connection()
    assert database.db.is_closed() is True
    database.open_connection()
    assert database.db.is_closed() is False


def test_drop_table(database):
    database.drop_table(models.Street)
    assert 'street' not in database.db.get_tables()


def test_add_database_field(database):
    database.add_database_field(models.Registered, 'registered', 'new_field', models.CharField(null=True))
    assert database.check_if_column_exist('registered', 'new_field') is True
    assert database.check_if_column_exist('not_existing_table', 'not_existing_column') is False


def test_check_if_column_exist(database):
    assert database.check_if_column_exist('person', 'gender') is True
    assert database.check_if_column_exist('test', 'test') is False
