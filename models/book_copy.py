from peewee import *

from models.base_model import BaseModel
from models.book import Book


class BookCopy(BaseModel):
    BOOK_CONDITIONS = ('new', 'good', 'bad', 'worn_out')

    id = AutoField(column_name='book_copy_id')
    condition = CharField(column_name='book_copy_condition', choices=BOOK_CONDITIONS, default='good')
    is_available = BooleanField(column_name='book_copy_available', default=True)
    book = ForeignKeyField(Book, column_name='bc_book_id', null=False)

    def __str__(self):
        return f'{self.book} [{self.id}]'