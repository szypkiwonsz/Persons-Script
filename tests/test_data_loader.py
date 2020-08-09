import models


def test_add_days_to_birthday_to_data(loader):
    new_data_list = loader.add_days_to_birthday_to_data()
    for data in new_data_list:
        assert 'days_to_birthday' in data['dob']


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
