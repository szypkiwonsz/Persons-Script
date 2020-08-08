import calendar
from datetime import datetime

import models
from database import Database
from utils import calculate_days_to_birthday


class DataLoader(Database):
    def __init__(self, db_path, data):
        """
        Object that inserts data into the database
        Adds the field 'days_to_birthday' to the 'dob' table in the database
        Adds the days until the person's birthday to the given data
        Adds the cleaned up person's phone number to the given data
        Deletes 'picture' table

        :param db_path: <string>, database path
        :param data: <list>, data to be inserted into the database
        """
        super().__init__(db_path)
        self.data = data
        self.add_database_field(models.Dob, 'dob', 'days_to_birthday', models.IntegerField(null=True))
        self.add_days_to_birthday_to_data()
        self.add_cleaned_phone_number_to_data()
        self.drop_table(models.Picture)

    def add_days_to_birthday_to_data(self):
        new_list = []
        for person in self.data:
            date_of_birth = datetime.strptime(person['dob']['date'], "%Y-%m-%dT%H:%M:%S.%f%z").date()
            days_to_birthday = calculate_days_to_birthday(date_of_birth)
            person['dob']['days_to_birthday'] = days_to_birthday
            new_list.append(person)
        self.data = new_list
        return new_list

    @staticmethod
    def day_not_exist(year, month, day):
        if not calendar.isleap(year) and month == 2 and day == 29:
            return True

    def add_cleaned_phone_number_to_data(self):
        new_list = []
        for person in self.data:
            person['phone'] = self.clean_string_to_number(person['phone'])
            person['cell'] = self.clean_string_to_number(person['cell'])
            new_list.append(person)
        self.data = new_list
        return new_list

    @staticmethod
    def clean_string_to_number(string):
        return ''.join(i for i in str(string) if i.isdigit())

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
