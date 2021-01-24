import pytest


@pytest.mark.query
def test_get_all_persons(database_with_data, query_handler):
    persons = query_handler.get_all_persons().dicts()
    assert persons[0]['gender'] == 'female'


@pytest.mark.query
def test_get_all_elements(query_handler):
    cities = query_handler.get_all_elements('location', 'city')
    assert cities[0] == 'Avignon'


@pytest.mark.query
def test_sort_dictionary_decreasing(common_elements_handler):
    dictionary = {'2': 2, '3': 3, '1': 1}
    sorted_dictionary = common_elements_handler.sort_dictionary_decreasing(dictionary)
    assert sorted_dictionary == [('3', 3), ('2', 2), ('1', 1)]


@pytest.mark.query
def test_get_count_and_elements(common_elements_handler):
    dictionary = {'France': 1}
    assert common_elements_handler.get_count_and_elements() == dictionary


@pytest.mark.query
def test_get_n_common_elements(common_elements_handler):
    assert common_elements_handler.get_n_common_elements(0) == []
    assert common_elements_handler.get_n_common_elements(1) == [('France', 1)]


@pytest.mark.query
def test_get_n_common_cities(common_cities_handler):
    assert common_cities_handler.get_n_common_cities(0) == []
    assert common_cities_handler.get_n_common_cities(1) == [('Avignon', 1)]


@pytest.mark.query
def test_get_n_common_passwords(common_passwords_handler):
    assert common_passwords_handler.get_n_common_passwords(0) == []
    assert common_passwords_handler.get_n_common_passwords(1) == [('r2d2', 1)]


@pytest.mark.query
def test_get_persons_by_gender(gender_handler):
    persons_by_gender = gender_handler.get_persons_by_gender('female').dicts()
    assert persons_by_gender[0]['gender'] == 'female'


@pytest.mark.query
def test_get_gender_percentage(gender_handler):
    assert gender_handler.get_gender_percentage('female') == 100
    assert gender_handler.get_gender_percentage('male') == 0


@pytest.mark.query
def test_get_average_gender_age(gender_handler):
    assert gender_handler.get_average_gender_age('all') == 54
    assert gender_handler.get_average_gender_age('male') == 0
    assert gender_handler.get_average_gender_age('female') == 54


@pytest.mark.query
def test_get_persons_born_between_dates(date_handler):
    assert date_handler.get_persons_born_between_dates()[0]['gender'] == 'female'


@pytest.mark.query
def test_get_all_passwords(password_handler):
    assert password_handler.get_all_passwords() == ['r2d2']


@pytest.mark.query
def test_get_safest_password(password_handler):
    """Also tests the 'rate_passwords' function."""
    assert password_handler.get_safest_password().__str__() == 'Password: r2d2, rating: 2'


@pytest.mark.query
def test_check_rating(password_handler, password):
    password.rating = 2
    password_handler.best_password.rating = 0
    password_handler.check_rating(password)
    assert password_handler.best_password.rating == 2
