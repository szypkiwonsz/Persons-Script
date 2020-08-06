import calendar
from datetime import datetime

import models
from database import Database


class DataLoader(Database):
    def __init__(self, db_path, data):
        """
        Object that inserts data into the database
        Adds the field 'days_to_birthday' to the 'dob' table in the database

        :param db_path: <string>, database path
        :param data: <list>, data to be inserted into the database
        """
        super().__init__(db_path)
        self.data = data
        self.add_database_field(models.Dob, 'dob', 'days_to_birthday', models.IntegerField(null=True))
        self.add_days_to_birthday_to_data()

    def add_days_to_birthday_to_data(self):
        new_list = []
        for person in self.data:
            date_of_birth = datetime.strptime(person['dob']['date'], "%Y-%m-%dT%H:%M:%S.%f%z").date()
            days_to_birthday = self.calculate_days_to_birthday(date_of_birth)
            person['dob']['days_to_birthday'] = days_to_birthday
            new_list.append(person)
        self.data = new_list
        return new_list

    def calculate_days_to_birthday(self, date_of_birth):
        """
        :param date_of_birth: <datetime.date>, date of birth of the person
        :return: <int>, days to a person's birthday
        """
        today = datetime.today()
        delta1 = datetime(today.year, date_of_birth.month, date_of_birth.day)
        if self.day_not_exist(today.year + 1, date_of_birth.month, date_of_birth.day):
            delta2 = datetime(today.year + 1, date_of_birth.month, date_of_birth.day - 1)
        else:
            delta2 = datetime(today.year + 1, date_of_birth.month, date_of_birth.day)
        if (delta1 - today).days > 0:
            delta = delta1
        else:
            delta = delta2
        days = (delta - today).days
        return days

    @staticmethod
    def day_not_exist(year, month, day):
        if not calendar.isleap(year) and month == 2 and day == 29:
            return True

    def insert_to_database(self):
        with self.db.atomic():
            for person in self.data:
                person_obj = models.Person(
                    gender=person['gender'], email=person['email'], phone=person['phone'], cell=person['cell'],
                    nat=person['nat']
                )
                person_obj.save()
                name_obj = models.Name(
                    person=person_obj, title=person['name']['title'], first=person['name']['first'],
                    last=person['name']['last']
                )
                name_obj.save()
                location_obj = models.Location(
                    person=person_obj, city=person['location']['city'], state=person['location']['state'],
                    country=person['location']['country'], postcode=person['location']['postcode']
                )
                location_obj.save()
                street_obj = models.Street(
                    location=location_obj, number=person['location']['street']['number'],
                    name=person['location']['street']['name']
                )
                street_obj.save()
                coordinates_obj = models.Coordinates(
                    location=location_obj, latitude=person['location']['coordinates']['latitude'],
                    longitude=person['location']['coordinates']['longitude']
                )
                coordinates_obj.save()
                timezone_obj = models.Timezone(
                    location=location_obj, offset=person['location']['timezone']['offset'],
                    description=person['location']['timezone']['description']
                )
                timezone_obj.save()
                login_obj = models.Login(
                    person=person_obj, uuid=person['login']['uuid'], username=person['login']['username'],
                    password=person['login']['password'], salt=person['login']['salt'], md5=person['login']['md5'],
                    sha1=person['login']['sha1'], sha256=person['login']['sha256']
                )
                login_obj.save()
                dob_obj = models.Dob(
                    person=person_obj, date=person['dob']['date'], age=person['dob']['age'],
                    days_to_birthday=person['dob']['days_to_birthday']
                )
                dob_obj.save()
                registered_obj = models.Registered(
                    person=person_obj, date=person['registered']['date'], age=person['registered']['date']
                )
                registered_obj.save()
                id_obj = models.Id(
                    person=person_obj, name=person['id']['name'], value=person['id']['value']
                )
                id_obj.save()
                picture_obj = models.Picture(
                    person=person_obj, large=person['picture']['large'], medium=person['picture']['medium'],
                    thumbnail=person['picture']['thumbnail']
                )
                picture_obj.save()
