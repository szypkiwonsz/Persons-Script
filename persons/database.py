import json

from peewee import SqliteDatabase, Model, chunked, TextField


class DatabaseHandler:
    """A class that manages the connection to the database, creates tables and enters data."""
    # database connection by pewee
    # pragma statements to increase performance of the database
    db = SqliteDatabase('database.db', pragmas={
        'journal_mode': 'wal',
        'synchronous': 0,
    })

    def __init__(self):
        """It initiates when creating a new object."""
        self.create_table(Person)

    @staticmethod
    def create_table(table_class):
        """Creates table in the database."""
        table_class.create_table()

    def insert_data_into_person(self, data):
        """
        Enters data into the 'person' table.
        :param data: <list> -> data about persons
        """
        self.insert_data(data, Person)

    def insert_data(self, data, table_class):
        """
        Inserts data into the database.
        :param data: <list> -> data about persons
        :param table_class: <peewee.ModelBase> -> class representing the table
        """
        with self.db.atomic():
            for batch in chunked(data, 10):
                table_class.insert_many(batch).execute()


class Person(Model):
    """Class representing the 'person' table in the database."""

    class MyJsonField(TextField):
        """Class for translating strings with json format into strings and vice-versa."""

        def db_value(self, value):
            return json.dumps(value)

        def python_value(self, value):
            if value is not None:
                return json.loads(value)
            return None

    gender = TextField()
    name = MyJsonField()
    location = MyJsonField()
    email = TextField()
    login = MyJsonField()
    dob = MyJsonField()
    dtb = TextField()
    registered = MyJsonField()
    phone = TextField()
    cell = TextField()
    id = MyJsonField()
    nat = TextField()

    class Meta:
        """Meta class for a database connection."""
        database = DatabaseHandler.db
