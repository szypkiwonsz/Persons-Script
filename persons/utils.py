import models


def count_only_gender(gender):
    query = models.Person.select().where(models.Person.gender == gender)
    return query.count()


def count_all_people():
    query = models.Person.select()
    return query.count()
