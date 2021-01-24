import pytest
from requests import HTTPError

from data_getter import Api


@pytest.mark.api
def test_get_200(requests_mock):
    requests_mock.get(f'https://randomuser.me/api/?results={str(1)}', json={'name': 'awesome-mock'})
    response = Api.get(f'https://randomuser.me/api/?results={str(1)}')
    assert response == {'name': 'awesome-mock'}


@pytest.mark.api
def test_get_404(requests_mock):
    requests_mock.get(f'https://randomuser.me/api/?results={str(1)}', status_code=404)
    with pytest.raises(HTTPError):
        response = Api.get(f'https://randomuser.me/api/?results={str(1)}')
