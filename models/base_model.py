from peewee import *
from settings import DATABASE_CONFIG

mysql = MySQLDatabase('library', **DATABASE_CONFIG)

class BaseModel(Model):
    class Meta:
        database = mysql
        legacy_table_names = False

