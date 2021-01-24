import pytest

from database import Person


@pytest.mark.database
def test_create_table(database_handler):
    """This function is performed when the object is initialized."""
    assert database_handler.db.get_tables()[0] == 'person'


@pytest.mark.database
def test_insert_data_into_person(database_handler, json_loader_with_modified_data):
    """Also tests the 'insert_data' function"""
    database_handler.insert_data_into_person(json_loader_with_modified_data.data['results'])
    assert Person.select().dicts()[0]['gender'] == 'female'
