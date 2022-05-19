"""Moduł zawiera definicje funkcji służących do wykonywania podstawowych operacji na bazie danych

Zawiera definicje następujących funkcji:
    * create_new_database - tworzy nową bazę danych w postaci pliku z rozszeszrzeniem .db
    * delete_database - usuwa wskazany plik z bazą danych
"""

from classes import Database


def create_new_database(database_list):
    """Tworzy nową bazę danych w postaci pliku z rozszeszrzeniem .db w katalogu 'databases'

    Funkcja pobiera od użytkownika nazwę bazy danych
    Gdy uzytkownik nie dopisze rozszerzenia .db - funkcja zrobi to za niego
    Funkcja sprawdza, czy dana baza znajduje się na liście istniejących baz danych
    Gdy dana baza już istnieje - wyswietlany jest stosowny komunikat
    Baza powstaje w momencie stworzenia instancji klasy Database

    Parameters
    ---------
    database_list : list
        lista z bazami danych istniejącymi w katalogu 'databases'
    """

    print('--' * 20)
    while True:
        print('Lista istniejących baz danych:', database_list)
        new_database = input("Podaj nazwę tworzonej bazy danych (nie musisz dodawac rozszerzenia .db)"
                             " lub wpisz '0', aby wrócić do menu głównego: ")
        if new_database == '0':
            break
        else:
            if new_database.endswith('.db'):
                new_database = new_database
            else:
                new_database = new_database + '.db'

            if new_database in database_list:
                print('Baza danych o podanej nazwie już istnieje. Wpisz inną nazwę!')
            else:
                db = Database(new_database)
                print(f"Pomyślnie utworzono bazę danych '{new_database}'.")
                db.close_connection()
                break


def delete_database(database_list):
    """Usuwa wskazany plik z bazą danych znajdujący się w katalogu 'databases'

    Funkcja odbiera od użykownika nazwę bazy, którą chce usunąć
    Gdy uzytkownik nie dopisze rozszerzenia .db - funkcja zrobi to za niego
    Funkcja sprawdza, czy dana baza znajduje się na liście istniejących baz danych
    Gdy dana baza nie istnieje - wyswietlany jest stosowny komunikat o niemożliwości jej usunięcia
    Baza zostaje usunięta w momencie wywołania metody 'delete_database' na obiekcie reprezentującym daną bazę
    """

    print('--' * 20)
    while True:
        print('Lista istniejących baz danych:', database_list)
        deleted_database = input("Podaj nazwę usuwanej bazy danych (nie musisz dodawac rozszerzenia .db)"
                                 " lub wpisz '0', aby wrócić do menu głównego: ")
        if deleted_database == '0':
            break
        else:
            if deleted_database.endswith('.db'):
                deleted_database = deleted_database
            else:
                deleted_database = deleted_database + '.db'

            if deleted_database not in database_list:
                print('Baza danych o podanej nazwie nie istnieje. Wpisz inną nazwę!')
            else:
                db = Database(deleted_database)
                db.delete_database()
                print(f"Pomyślnie usunięto bazę danych '{deleted_database}'.")
                db.close_connection()
                break
