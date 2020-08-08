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
        """Rounding the result"""
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
        """Rounding the result"""
        try:
            average_age = self.get_only_gender_age(gender) / count_only_gender(gender)
        except TypeError as e:
            raise ValueError from e
        return round(average_age)

    def calculate_all_people_average(self):
        """Rounding the result"""
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
