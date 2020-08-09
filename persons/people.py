from operator import itemgetter

import models
from database import Database
from utils import count_all_people, count_only_gender


class PercentagePeople(Database):
    def __init__(self, db_path):
        """
        Object that calculates the percentage of men and women in the database

        :param db_path: <string>, database path
        """
        super().__init__(db_path)

    def gender_percentage(self, gender):
        try:
            return self.calculate_percentage(count_only_gender(gender), count_all_people())
        except ValueError:
            return 0

    @staticmethod
    def calculate_percentage(got, total):
        # Rounding the result
        try:
            percentage = 100 * got / total
        except ZeroDivisionError as e:
            raise ValueError from e
        return round(percentage)

    def print_percentage_results(self):
        print(f'Percentage of women: {self.gender_percentage("female")}%, men: {self.gender_percentage("male")}%')


class AverageAge(Database):
    def __init__(self, db_path, parameter):
        """
        Object that returns the average age of women, men, or all people in the database

        :param db_path: <string>, database path
        :param parameter: <string>, entered parameter
        """
        super().__init__(db_path)
        self.parameter = parameter.lower()

    @staticmethod
    def get_only_gender_age(gender):
        query = models.Dob.select(
            models.fn.SUM(models.Dob.age).alias('sum')).join(
            models.Person).where(
            models.Person.gender == gender
        ).scalar()
        return query

    @staticmethod
    def get_all_people_age():
        query = models.Dob.select(models.fn.SUM(models.Dob.age).alias('sum')).scalar()
        return query

    def calculate_average_gender(self, gender):
        # Rounding the result
        try:
            average_age = self.get_only_gender_age(gender) / count_only_gender(gender)
        except TypeError as e:
            raise ValueError from e
        return round(average_age)

    def calculate_all_people_average(self):
        # Rounding the result
        try:
            average_age = self.get_all_people_age() / count_all_people()
        except ZeroDivisionError as e:
            raise ValueError from e
        return round(average_age)

    def print_average_results(self):
        try:
            if self.parameter == 'male':
                print(self.calculate_average_gender('male'))
            elif self.parameter == 'female':
                print(self.calculate_average_gender('female'))
            else:
                print(self.calculate_all_people_average())
        except ValueError:
            print('No data in the database.')


class MostCommonValue(Database):
    def __init__(self, db_path, parameter, model, column):
        """
        Object that returns the 'n' most common values for the selected column

        :param db_path: <string>, database path
        :param parameter: <int>, entered parameter (number of results to be returned)
        :param model: <peewee.ModelBase>, e.g. ---> models.Location
        :param column: <peewee.CharField>, e.g. ---> models.Location.city
        """
        super().__init__(db_path)
        self.parameter = parameter
        self.model = model
        self.column = column

    def select_most_common_values(self):
        # Get the name and number of results, grouped by column and sorted by the counted results in descending order,
        # the parameter is the limit of the results
        query = self.model.select(
            self.column.alias('name'), models.fn.COUNT(self.column).alias('counted')).group_by(
            self.column).order_by(
            models.fn.COUNT(self.column).desc()
        ).limit(self.parameter)
        return query

    def print_most_common_values(self):
        for value in self.select_most_common_values():
            print(f'{value.name}, {value.counted}')


class RangeValueParameter(Database):
    def __init__(self, db_path, first_parameter, second_parameter, model, column):
        """
        Object returning people who fall within the range of values ​​of the given parameters, of the selected column

        :param db_path: <string>, database path
        :param first_parameter: <string>, first entered parameter
        :param second_parameter: <string>, second entered parameter
        :param model: <peewee.ModelBase>, e.g. ---> models.Dob
        :param column: <peewee.CharField>, e.g. ---> models.Dob.date
        """
        super().__init__(db_path)
        self.first_parameter = first_parameter
        self.second_parameter = second_parameter
        self.model = model
        self.column = column

    def select_values_in_range(self):
        query = models.Name.select(
            models.Person, self.column, models.Name).join(
            models.Person).join(
            self.model).where(
            (self.first_parameter < self.column) & (self.column < self.second_parameter)
        )
        return query

    def print_results(self):
        for name in self.select_values_in_range():
            print(f'{name.first} {name.last}')


class MostPointedValue(Database):
    def __init__(self, db_path, model, column):
        """
        Object that returns the value of the selected column with the most points

        :param db_path: <string>, database path
        :param model: <peewee.ModelBase>, e.g. ---> models.Login
        :param column: <peewee.CharField>, e.g. ---> models.Login.password
        """
        super().__init__(db_path)
        self.model = model
        self.column = column

    def get_all_values_as_list(self):
        query = self.model.select(self.column.alias('value'))
        return [data.value for data in query]

    @staticmethod
    def check_lowercase(value):
        if any(c.islower() for c in value):
            return True

    @staticmethod
    def check_uppercase(value):
        if any(c.isupper() for c in value):
            return True

    @staticmethod
    def check_length(value, length):
        if len(value) >= length:
            return True

    @staticmethod
    def check_special_character(value):
        sum_special_characters = 0
        for c in value:
            if not c.isalnum():
                sum_special_characters += 1
        return sum_special_characters

    def rate_values(self, values):
        new_list_values = []
        for value in values:
            points = 0
            if self.check_lowercase(value):
                points += 1
            if self.check_uppercase(value):
                points += 2
            if self.check_length(value, 8):
                points += 5
            if self.check_special_character(value):
                sum_special_characters = self.check_special_character(value)
                points += 3 * sum_special_characters
            new_list_values.append((value, points))
        return new_list_values

    def most_rated_value(self):
        all_values = self.get_all_values_as_list()
        results = self.rate_values(all_values)
        try:
            result = max(results, key=itemgetter(1))
        except ValueError:
            print('No data in the database.')
        else:
            value, points = result
            print(f'{value}, {points}')
            return result
