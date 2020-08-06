from peewee import *

# Defer initialization
# Pragma statements to increase performance of the database
db = SqliteDatabase(None, pragmas={
    'journal_mode': 'wal',
    'synchronous': 0,
    'locking_mode': 'EXCLUSIVE'
})


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    gender = CharField()
    email = CharField()
    phone = CharField()
    cell = CharField()
    nat = CharField()


class Name(BaseModel):
    person = ForeignKeyField(Person)
    title = CharField()
    first = CharField()
    last = CharField()


class Location(BaseModel):
    person = ForeignKeyField(Person)
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = IntegerField()


class Street(BaseModel):
    location = ForeignKeyField(Location)
    number = IntegerField()
    name = CharField()


class Coordinates(BaseModel):
    location = ForeignKeyField(Location)
    latitude = CharField()
    longitude = CharField()


class Timezone(BaseModel):
    location = ForeignKeyField(Location)
    offset = CharField()
    description = CharField()


class Login(BaseModel):
    person = ForeignKeyField(Person)
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()


class Dob(BaseModel):
    person = ForeignKeyField(Person)
    date = DateTimeField()
    age = IntegerField()


class Registered(BaseModel):
    person = ForeignKeyField(Person)
    date = DateTimeField()
    age = IntegerField()


class Id(BaseModel):
    person = ForeignKeyField(Person)
    name = CharField()
    value = CharField()


class Picture(BaseModel):
    person = ForeignKeyField(Person)
    large = CharField()
    medium = CharField()
    thumbnail = CharField()


MODELS = [Person, Name, Location, Street, Coordinates, Timezone, Login, Dob, Registered, Id, Picture]
