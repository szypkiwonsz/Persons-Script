import argparse
import os

from data_getter import DataFromFile, DataFromApi
from data_loader import DataLoader
from people import PercentagePeople

DATABASE = 'persons.db'
FILE = 'persons.json'


def database_file_exist(db_path):
    return os.path.exists(db_path)


def check_if_arguments(args):
    if not any(vars(args).values()) and not any(vars(args).values()) == '0':
        return False
    else:
        return True


def get_api_url(number_of_people):
    return f'https://randomuser.me/api/?results={number_of_people}'


def load_data_api_check_argument(x):
    try:
        x = int(x)
    except Exception:
        raise argparse.ArgumentTypeError('Argument has to be an int from 1 to 5000')
    if x <= 0 or x > 5000:
        raise argparse.ArgumentTypeError('Argument has to be an int from 1 to 5000')
    return x


def create_parser():
    parser = argparse.ArgumentParser(description='Human data operations')
    parser.add_argument(
        '-load-data-api', help='inserts data from API to the database. You have to specify number of people to add as '
                               'an argument (from 1 to 5000)', metavar='N', type=load_data_api_check_argument
    )
    parser.add_argument(
        '-percentage-people', action='store_true', help='shows the percentage of women and men in the database'
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # If the database has not been created before, create it and insert the data from the json file
    if not database_file_exist(DATABASE):
        file = DataFromFile(FILE)
        persons_data = file.get_persons_data()
        loader = DataLoader(DATABASE, persons_data)
        loader.insert_to_database()

    if not check_if_arguments(args):
        print('There are no arguments passed!')
    elif args.load_data_api:
        api_url = get_api_url(args.load_data_api)
        api = DataFromApi(api_url)
        persons_data = api.get_persons_data()
        loader = DataLoader(DATABASE, persons_data)
        loader.insert_to_database()
    elif args.percentage_people:
        people = PercentagePeople(DATABASE)
        people.print_percentage_results()


if __name__ == '__main__':
    main()
