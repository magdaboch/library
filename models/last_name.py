from models.base_model import BaseModel
from peewee import *

class LastName(BaseModel):
    id = AutoField(
        column_name='ln_id',
        verbose_name='ID nazwiska'
    )
    name = CharField(
        column_name='last_name',
        verbose_name='Nazwisko',
        max_length=50,
        unique=True
    )

    class Meta:
        table_name = 'last_name'