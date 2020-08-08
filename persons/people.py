import models
from database import Database


class PercentagePeople(Database):
    def __init__(self, db_path):
        """
        Object that calculates the percentage of men and women in the database

        :param db_path: <string>, database path
        """
        super().__init__(db_path)

    def women_percentage(self):
        return self.calculate_percentage(self.count_only_gender('female'), self.count_all_people())

    def men_percentage(self):
        return self.calculate_percentage(self.count_only_gender('male'), self.count_all_people())

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
        percentage = 100 * got / total
        return round(percentage)

    def print_percentage_results(self):
        print(f'Percentage of women: {self.women_percentage()}%, men: {self.men_percentage()}%')
