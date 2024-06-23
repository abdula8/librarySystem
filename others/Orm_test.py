#  pip install peewee
#  pip install pymysql
from peewee import *
import pymysql
# db = SqliteDatabase('people.db')
# Connect to MySQL database on network
db = MySQLDatabase('myapp', user='root', password='01099110790aA@',
                            host='localhost', port=3306)
#db = SqliteDatabase('myapp.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  ##  This model uses the "people.dp" database

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db ## this model uses the "people.db" database

db.connect()
db.create_tables([Person, Pet])

