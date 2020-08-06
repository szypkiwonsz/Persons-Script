import json


class DataFromFile:
    def __init__(self, file_path):
        """
        Object that gets data from the json file

        :param file_path: <string>, file path
        """
        self.file_path = file_path

    def get_json_data(self):
        with open(self.file_path, encoding='utf8') as json_file:
            data = json.load(json_file)
        return data

    def get_persons_data(self):
        data = self.get_json_data()
        return data['results']
