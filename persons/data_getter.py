import json
import os
import sys

import requests


class DataFromFile:
    def __init__(self, file_path):
        """
        Object that gets data from the json file

        :param file_path: <string>, file path
        """
        self.file_path = file_path

    def get_json_data(self):
        # Added os functions to handle the tests properly
        with open(os.path.join(os.path.dirname(__file__), self.file_path), encoding='utf8') as json_file:
            data = json.load(json_file)
        return data


class DataFromApi:
    def __init__(self, api_url):
        """
        Object that gets data from api

        :param api_url: <string>, url address
        """
        self.api_url = api_url

    def get_json_data_from_api(self):
        try:
            response = requests.get(self.api_url, timeout=10)
            # Handling: service temporarily unavailable error
            if response.status_code == 503:
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Oops! something unexpected happened. {e}. Try again.')
            sys.exit()
        except requests.exceptions.ConnectionError:
            print('Oops! Connection Error. Make sure you are connected to Internet.')
            sys.exit()
        return response.json()
