import pytest


@pytest.mark.password
def test_password_str(password):
    assert password.__str__() == f'Password: Qwertyu1?, rating: 0'


@pytest.mark.password
def test_rate_password(password_rater):
    password_rater.rate_password()
    assert password_rater.rating == 12
