import requests


class Api:
    """Class storing method to get data from api."""

    @staticmethod
    def get(url):
        """
        Gets json data from api.
        :param url: <string> -> api url
        :return: <dict> -> json data from api
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}")
        else:
            return response.json()
