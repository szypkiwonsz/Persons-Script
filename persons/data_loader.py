import calendar
import json
from datetime import datetime

from data_getter import Api


class JsonLoader:
    """Class that loads and modifies data stored in json."""

    def __init__(self):
        self.data = {}

    def load_data_from_file(self, filename):
        """Load data from specified file into object data field."""
        with open(filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def load_data_from_api(self, n):
        """
        Load specified amount of people from api.
        :param n: <int> -> number of people to be loaded
        """
        self.data['results'] = (Api.get(f'https://randomuser.me/api/?results={str(n)}')["results"])

    def modify_data(self):
        """Modifies the data in accordance with the program assumptions (removes the photo field, clears the phone
        number and calculates the days to birth)."""
        for element in self.data['results']:
            element.pop('picture')
            self.fix_numbers(element)
            self.add_days_to_birthday(element)

    def fix_numbers(self, element):
        """
        Corrects numbers to contain only numbers.
        :param element: <dict> -> single person data
        """
        if element['phone'] is not None:
            element['phone'] = self.clean_string_to_number(element['phone'])
        if element['cell'] is not None:
            element['cell'] = self.clean_string_to_number(element['cell'])

    @staticmethod
    def clean_string_to_number(number):
        """
        Clears a number to one that contains only numbers.
        :param number: <string> -> string containing a number
        :return: <string> -> number containing only numbers
        """
        return ''.join(i for i in str(number) if i.isdigit())

    def add_days_to_birthday(self, element):
        """
        Adds a field for each element that shows the days until birthdays.
        :param element: <dict> -> single person data
        """
        if element['dob'] is not None:
            element['dtb'] = self.calculate_days_to_birthday(element['dob'])

    def calculate_days_to_birthday(self, dob):
        """
        Calculates the number of days until birthdays.
        :param dob: <dict> -> data dictionary field containing the key 'date'
        :return: <int> -> days to a person's birthday
        """
        date_of_birth = datetime.strptime(dob['date'], '%Y-%m-%dT%H:%M:%S.%f%z')
        today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        if self.day_not_exist(today.year + 1, date_of_birth.month, date_of_birth.day):
            delta1 = datetime(today.year, date_of_birth.month, date_of_birth.day - 1)
            delta2 = datetime(today.year + 1, date_of_birth.month, date_of_birth.day - 1)
        else:
            delta1 = datetime(today.year, date_of_birth.month, date_of_birth.day)
            delta2 = datetime(today.year + 1, date_of_birth.month, date_of_birth.day)
        if (delta1 - today).days > 0:
            delta = delta1
        else:
            delta = delta2
        days = (delta - today).days
        return days

    @staticmethod
    def day_not_exist(year, month, day):
        """
        Checks if the given day of the year exists.
        :param year: <int> -> year entered
        :param month: <int> -> month entered
        :param day: <int> -> day entered
        :return: <bool> -> False if exist, True if not
        """
        if not calendar.isleap(year) and month == 2 and day == 29:
            return True
        return False
