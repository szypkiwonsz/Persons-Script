import argparse
import os

from data_getter import DataFromFile
from data_loader import DataLoader


def database_file_exist(db_path):
    return os.path.exists(db_path)


parser = argparse.ArgumentParser(description='Human data operations')
args = parser.parse_args()

if __name__ == '__main__':

    DATABASE = 'persons.db'
    FILE = 'persons.json'

    # If the database has not been created before, create it and insert the data from the json file
    if not database_file_exist(DATABASE):
        file = DataFromFile(FILE)
        persons_data = file.get_persons_data()
        data = DataLoader(DATABASE, persons_data)
        data.insert_to_database()

    if not any(vars(args).values()):
        print('There are no arguments passed!')
