from datetime import datetime


def string_to_date(string, date_format):
    """
    Changes string to date format.
    :param string: <str> -> date of type string
    :param date_format: <string> -> format of date to get
    :return: <datetime.date> -> date from provided string
    """
    return datetime.strptime(string, date_format).date()
