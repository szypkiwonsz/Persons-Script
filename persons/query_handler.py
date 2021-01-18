from database import Person
from password_rater import Password, PasswordRater
from utils import string_to_date


class QueryHandler:
    """Class storing methods for basics database queries."""

    @staticmethod
    def get_all_persons():
        """
        Gets all persons data from the database.
        :return: <peewee.ModelSelect> -> class with persons data
        """
        return Person.select()

    def get_all_elements(self, table_name, dict_key):
        """
        Gets list with values selected by database table name and dictionary key, because of how the json is formatted.
        :param table_name: <string> -> database table name
        :param dict_key: <string> -> dictionary key of the values will be retrieve from the database
        :return: <list> -> retrieved values from the database
        """
        persons = self.get_all_persons().dicts()
        return [person[table_name][dict_key] for person in persons]


class CommonElementsHandler(QueryHandler):
    """Inheriting class storing methods for getting common n elements from persons data."""

    def __init__(self, table_name, dict_key):
        self.table_name = table_name
        self.dict_key = dict_key

    @staticmethod
    def sort_dictionary_decreasing(dictionary):
        """
        Sorts dictionary decreasing.
        :param dictionary: <dict> -> dictionary to be sorted
        :return: <list> -> list of tuples sorted by dictionary values decreasing
        """
        return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    def get_count_and_elements(self):
        """
        Gets dictionary with key as selected element and the number of its repetitions as a value.
        :return: <dict> -> dictionary with key as selected element and value as the number of its repetitions
        """
        dictionary = {}
        for element in self.get_all_elements(self.table_name, self.dict_key):
            dictionary[element] = dictionary.setdefault(element, 0) + 1
        return dictionary

    def get_n_common_elements(self, n):
        """
        Gets n common elements form all selected elements.
        :param n: <int> -> number of elements to be shown
        :return: <list> -> list of selected elements
        """
        elements = self.sort_dictionary_decreasing(self.get_count_and_elements())
        return elements[:n]


class CommonCitiesHandler(CommonElementsHandler):
    """Inheriting class storing methods for getting common n cities from persons data."""

    def __init__(self):
        super().__init__('location', 'city')

    def get_n_common_cities(self, n):
        """
        Gets most n common cities from persons data.
        :param n: <int> -> number of cities to be shown
        :return: <list> -> list of n cities
        """
        return self.get_n_common_elements(n)


class CommonPasswordsHandler(CommonElementsHandler):
    """Inheriting class storing methods for getting common n passwords from persons data."""

    def __init__(self):
        super().__init__('login', 'password')

    def get_n_common_passwords(self, n):
        """
        Gets most n common passwords from persons data.
        :param n: <int> -> number of passwords to be shown
        :return: <list> -> list of n passwords
        """
        return self.get_n_common_elements(n)


class GenderHandler(QueryHandler):
    """Inheriting class storing methods related to database gender queries."""

    @staticmethod
    def get_persons_by_gender(gender):
        """
        Gets peoples from database by gender.
        :param gender: <string> -> gender of persons
        :return: <peewee.ModelSelect> -> persons objects from database by gender
        """
        return Person.select().where(Person.gender == gender)

    def get_gender_percentage(self, gender):
        """
        Gets gender percentage of persons in database by gender.
        :param gender: <string> -> gender of persons
        :return: <float> -> percentage of persons selected by gender
        """
        count_part = self.get_persons_by_gender(gender).count()
        count_all = self.get_all_persons().count()
        return round(100 * count_part / count_all, 2)

    def get_average_gender_age(self, gender):
        """
        Gets average age of persons in database by gender.
        :param gender: <string> -> gender of persons
        :return: <int> -> average age of persons in database selected by gender
        """
        if gender == 'all':
            return self.calculate_average_age(self.get_all_persons().dicts(), self.get_all_persons().count())
        return self.calculate_average_age(
            self.get_persons_by_gender(gender).dicts(), self.get_persons_by_gender(gender).count())

    @staticmethod
    def calculate_average_age(persons, count):
        """
        Calculates average age of persons.
        :param persons: <pewee.ModelSelect> -> persons objects from database
        :param count: <int> -> sum of persons
        :return: <int> -> average age of persons
        """
        temp_sum = 0
        for person in persons:
            temp_sum += int(person['dob']['age'])
        return temp_sum // count


class DateHandler(QueryHandler):
    """Class storing methods to select people born between two dates."""

    def __init__(self, first_date, second_date):
        self.first_date = string_to_date(first_date, '%Y-%m-%d')
        self.second_date = string_to_date(second_date, '%Y-%m-%d')

    def get_persons_born_between_dates(self):
        """
        Gets filtered persons born between two dates.
        :return: <list> -> list of dicts with persons data.
        """
        return list(filter(lambda person: self.first_date < string_to_date(
            person['dob']['date'], '%Y-%m-%dT%H:%M:%S.%fZ') < self.second_date, self.get_all_persons().dicts()))


class PasswordHandler(QueryHandler):
    """Inheriting class storing methods to get the most safest password from database."""

    def __init__(self):
        self.best_password = Password('')

    def get_all_passwords(self):
        """
        Gets all passwords from database.
        :return: <list> -> list of all persons passwords from database
        """
        return self.get_all_elements('login', 'password')

    def get_safest_password(self):
        """Gets safest password from database selected by password rater."""
        self.rate_passwords()
        return self.best_password

    def rate_passwords(self):
        """Rates all passwords from database."""
        for password in self.get_all_passwords():
            temp_password_rater = PasswordRater(password)
            temp_password_rater.rate_password()
            self.check_rating(temp_password_rater)

    def check_rating(self, password_with_rating):
        """
        Checks if given password is better than the stored one and if true, replaces it.
        :param password_with_rating: <password_rater.PasswordRater> -> password with calculated rating
        """
        if password_with_rating.rating > self.best_password.rating:
            self.best_password = password_with_rating
