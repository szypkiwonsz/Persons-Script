import argparse
import os
from datetime import datetime

import models
from data_getter import DataFromFile, DataFromApi
from data_loader import DataLoader
from people import PercentagePeople, AverageAge, MostCommonValue, RangeValueParameter, MostPointedValue
from utils import get_persons_data

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


def most_common_check_argument(x):
    try:
        x = int(x)
    except Exception:
        raise argparse.ArgumentTypeError('Argument has to be an int greater than 0')
    if x <= 0:
        raise argparse.ArgumentTypeError('Argument has to be an int greater than 0')
    return x


def dob_check_argument(x):
    try:
        x = datetime.strptime(x, '%Y-%m-%d')
    except Exception:
        raise argparse.ArgumentTypeError('Argument has to be an string in format YYYY-MM-DD')
    return x


def create_parser():
    parser = argparse.ArgumentParser(description='Human data operations')
    parser.add_argument(
        '-load-data-api', help='inserts data from API to the database, you have to specify number of people to add as '
                               'an argument (from 1 to 5000)', metavar='N', type=load_data_api_check_argument
    )
    parser.add_argument(
        '-percentage-people', action='store_true', help='shows the percentage of women and men in the database'
    )
    parser.add_argument(
        '-average-age', nargs='?', const='all', help='shows the average age of men women or all people in the database',
        choices=['male', 'female', 'all']
    )
    parser.add_argument(
        '-most-common-city', help='shows the most common city/cities in the database, you have to specify number of '
                                  'values to show (greater than 0)', type=most_common_check_argument, metavar='N'
    )
    parser.add_argument(
        '-most-common-password', help='shows the most common password/passwords in the database, you have to specify '
                                      'number of values to show (greater than 0)', type=most_common_check_argument,
        metavar='N'
    )
    parser.add_argument(
        '-range-dob', nargs=2, help='shows people born between the dates given as a parameter', type=dob_check_argument,
        metavar='YYYY-MM-DD'
    )
    parser.add_argument('-safest-password', action='store_true', help='shows the password with the most points')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # If the database has not been created before, create it and insert the data from the json file
    if not database_file_exist(DATABASE):
        file = DataFromFile(FILE)
        data = file.get_json_data()
        persons_data = get_persons_data(data)
        loader = DataLoader(DATABASE, persons_data)
        loader.insert_to_database()

    if not check_if_arguments(args):
        print('There are no arguments passed!')
    elif args.load_data_api:
        api_url = get_api_url(args.load_data_api)
        api = DataFromApi(api_url)
        data = api.get_json_data_from_api()
        persons_data = get_persons_data(data)
        loader = DataLoader(DATABASE, persons_data)
        loader.insert_to_database()
    elif args.percentage_people:
        people = PercentagePeople(DATABASE)
        people.print_percentage_results()
    elif args.average_age:
        average = AverageAge(DATABASE, args.average_age)
        average.print_average_results()
    elif args.most_common_city:
        city = MostCommonValue(DATABASE, args.most_common_city, models.Location, models.Location.city)
        city.print_most_common_values()
    elif args.most_common_password:
        password = MostCommonValue(DATABASE, args.most_common_password, models.Login, models.Login.password)
        password.print_most_common_values()
    elif args.range_dob:
        date = RangeValueParameter(DATABASE, args.range_dob[0], args.range_dob[1], models.Dob, models.Dob.date)
        date.print_results()
    elif args.safest_password:
        password = MostPointedValue(DATABASE, models.Login, models.Login.password)
        password.most_rated_value()


if __name__ == '__main__':
    main()
