import argparse

from data_getter import DataFromFile
from data_loader import DataLoader

parser = argparse.ArgumentParser(description='Human data operations')
parser.add_argument('-load-data-file', help='inserts data from JSON file to the database', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':

    DATABASE = 'persons.db'
    FILE = 'persons.json'

    if not any(vars(args).values()):
        print('There are no arguments passed!')
    elif args.load_data_file:
        file = DataFromFile(FILE)
        persons_data = file.get_persons_data()
        data = DataLoader(DATABASE, persons_data)
        data.insert_to_database()
