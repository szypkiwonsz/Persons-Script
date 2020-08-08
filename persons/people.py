import models
from database import Database


class PercentagePeople(Database):
    def __init__(self, db_path):
        """
        Object that calculates the percentage of men and women in the database

        :param db_path: <string>, database path
        """
        super().__init__(db_path)

    def gender_percentage(self, gender):
        try:
            return self.calculate_percentage(self.count_only_gender(gender), self.count_all_people())
        except ValueError:
            return 0

    @staticmethod
    def count_only_gender(gender):
        query = models.Person.select().where(models.Person.gender == gender)
        return query.count()

    @staticmethod
    def count_all_people():
        query = models.Person.select()
        return query.count()

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
