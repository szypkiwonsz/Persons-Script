import requests


class Api:

    @staticmethod
    def get(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}")
        else:
            return response.json()
