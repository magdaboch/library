from library_options.users import Users
from library_options.books import Books
from models.first_name import FirstName
from models.last_name import LastName

from models.author import Author
from models.rent_book import RentBook
from models.book_copy import BookCopy
# from DBcm import UseDatabase
# from settings import DATABASE_CONFIG
#
#
# def main():
#     with UseDatabase(DATABASE_CONFIG) as cursor:
#         sql = 'select * from first_name'
#         cursor.execute(sql)
#         data = cursor.fetchall()
#
#     print(data)
#
# if __name__ == '__main__':
#     main()

def main():
    print('Wybierz opcję:')
    print('1 - dodaj książkę')
    print('2 - znajdź książkę')
    print('3 - dodaj użytkownika')
    print('4 - znajdz ksiażki użytkownika')
    print('q - zakończ program')

    option = input('> ')
    if option == 'q':
        exit()

    try:
        option = int(option)
    except ValueError:
        main()

    if option == 3:
        user_id = Users().add()
        print(f'Dodano użytkownika o ID {user_id}')

    if option == 1:
        book_id = Books().add()
        print(f'Dodana książkę o ID {book_id}')

    if option == 2:
        book= Books().find_book()

        try:
            book_copy = BookCopy().get(book=book, is_available=True)
        except:
            print('Brak dostępnych egzemplarzy')
            main()

        print(f'Wybrano książkę "{book}"')
        print('Dostępne opcje')
        print(' 1 - Wypożycz książkę')
        print(' * - Powrót do głównego menu')

        sub_option = input('> ')

        if sub_option == '*':
            main()

        try:
            sub_option = int(sub_option)
        except ValueError:
            main()

        if sub_option == 1:
            user = Users().find()
            if input(f'Wypożyczyć książkę "{book}" czytelnkowi {user}? [t/n]') == 't':
                RentBook(book=book_copy, reader=user).save()
                print('Książka wypożyczona!')

    if option == 4:
        Users().find_by_last_name()

    main()
    # try:
    #     last_name = LastName().get_or_create(last_name='Kowalska')
    #     first_name = FirstName().get_or_create(name='Wojtek')
    #     print(first_name[0].name)
    #     print(last_name[0].last_name)
    # except:
    #     pass
    # first_name.name = 'Rafał'
    # first_name.save()
    # book = Book().get_by_id(1)
    # print(book.authors[0])

    # author = Author().select().join(LastName).where(LastName.name == 'sienkiewicz')
    #
    # for book in author[0].books:
    #     print(book)
    #
    # copies = BookCopy().select().where(BookCopy.book == 1)
    # for copy in copies:
    #     print(copy)
    #
    # rent = RentBook().select()
    # for i in rent:
    #     print(i)

    # client = LibraryClient().get_by_id(1)
    # print(client.first_name.name)


if __name__ == '__main__':
    main()
