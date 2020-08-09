import pytest


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


def test_select_most_common_values_city(most_common_city):
    values = most_common_city.select_most_common_values()
    names = ['Gisborne', 'Lower Hutt', 'Napier', 'Queanbeyan', 'Van']
    counted = [7, 5, 5, 5, 5]
    for i, value in enumerate(values):
        assert value.name == names[i]
        assert value.counted == counted[i]


def test_select_most_common_values_password(most_common_password):
    values = most_common_password.select_most_common_values()
    names = ['achtung', 'surf', '1030', '1223', '1228']
    counted = [3, 3, 2, 2, 2]
    for i, value in enumerate(values):
        assert value.name == names[i]
        assert value.counted == counted[i]


def test_select_values_in_range(range_dob):
    names = range_dob.select_values_in_range()
    first_names = ['Laura', 'Douglas', 'Eliott', 'Tristan', 'Josefina', 'Kasimir']
    last_names = ['Cook', 'Gregory', 'Girard', 'Nielsen', 'Soto', 'Bücker']
    for i, name in enumerate(names):
        assert name.first == first_names[i]
        assert name.last == last_names[i]


def test_get_all_values_as_list(safest_password):
    values_list = safest_password.get_all_values_as_list()
    assert values_list[0] == 'r2d2'
    assert values_list[1] == '0101'


def test_check_lowercase(safest_password):
    assert safest_password.check_lowercase('lower') is True
    assert safest_password.check_lowercase('UPPER') is None
    assert safest_password.check_lowercase('Capital') is True


def test_check_uppercase(safest_password):
    assert safest_password.check_uppercase('lower') is None
    assert safest_password.check_uppercase('UPPER') is True
    assert safest_password.check_uppercase('Capital') is True


def test_check_length(safest_password):
    assert safest_password.check_length('lower', 3) is True
    assert safest_password.check_length('UPPER', 8) is None
    assert safest_password.check_length('Capital', 7) is True


def test_check_special_character(safest_password):
    assert safest_password.check_special_character('lower') == 0
    assert safest_password.check_special_character('UPPER-') == 1
    assert safest_password.check_special_character('C.api-tal?') == 3
    assert safest_password.check_special_character('Capital124') == 0


def test_rate_values(safest_password):
    passwords = ['password', 'pa2p-xX', 'Password_Md2']
    good_points = [6, 6, 11]
    new_list = safest_password.rate_values(passwords)
    for i, value in enumerate(new_list):
        value, points = new_list[i]
        assert points == good_points[i]


def test_most_rated_value(safest_password):
    value, points = safest_password.most_rated_value()
    assert value == 'films+pic+galeries'
    assert points == 12
