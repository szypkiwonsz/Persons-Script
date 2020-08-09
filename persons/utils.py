import calendar
from datetime import datetime

import models


def count_only_gender(gender):
    query = models.Person.select().where(models.Person.gender == gender)
    return query.count()


def count_all_people():
    query = models.Person.select()
    return query.count()


def day_not_exist(year, month, day):
    if not calendar.isleap(year) and month == 2 and day == 29:
        return True


def calculate_days_to_birthday(date_of_birth):
    """
    :param date_of_birth: <datetime.date>, date of birth of the person
    :return: <int>, days to a person's birthday
    """
    today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    if day_not_exist(today.year + 1, date_of_birth.month, date_of_birth.day):
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


def get_persons_data(data):
    return data['results']
