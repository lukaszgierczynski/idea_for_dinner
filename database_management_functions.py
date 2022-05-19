"""Moduł zawiera definicje funkcji służących do łączenia z bazą oraz do wykynywania operacji na tabelach

Zawiera definicje następujących funkcji:
    * connect_database - tworzy połączenie z bazą danych
    * database_management - odpowiada za obsługę działań na bazie wskazanych przez użytkownika
    * create_new_table - tworzy nową tabelę w bazie danych
    * drop_table - usuwa tabelę z bazy danych
    * add_record - dodaje nowe danie w bazie danych
    * delete_record - usuwa wskazane danie z bazy danych
    * add_csv - umożliwia użytkownikowi dodanie dań do tabeli przy użyciu pliku .csv
    * csv_reader - odczytuje dania z pliku csv i zapisuje je w tabeli
    * lunch_planner - tworzy plan obiadów na podstawie danej tabeli
"""


import csv
from classes import Database, Table, LunchPlan
from validation_functions import user_choice_validation, which_course_validation, new_record_validation, add_new_dish_validation, delete_dish_validation, lunch_planner_validation


def connect_database(database_list):
    """Tworzy połączenie z istniejącą bazą danych

    Po połączeniu z bazą wywyoływana jest funkcja 'database_management'
    Po zakończeniu działania funkcji 'database_management' połączenie z bazą
    jest zamykane

    Parameters
    ----------
    database_list : list
        lista z bazami danych istniejącymi w katalogu 'databases'
    """

    while True:
        print('--' * 20)
        print('Lista istniejących baz danych:', database_list)
        print()
        selected_database = input("Podaj nazwę bazy danych, z którą chcesz się połączyć (nie musisz dodawac"
                                  " rozszerzenia .db) lub wpisz '0', aby wrócić do menu głównego: ")

        if selected_database == '0':
            break
        else:
            if selected_database.endswith('.db'):
                selected_database = selected_database
            else:
                selected_database = selected_database + '.db'

        if selected_database not in database_list:
            print('Baza danych o podanej nazwie nie istnieje. Wpisz inną nazwę!')
        else:
            db = Database(selected_database)
            print(f"Pomyślnie połączono z bazą danych '{db.name}'.")
            database_management(db)
            db.close_connection()
            print("Pomyślnie rozłączono z bazą danych.")


def database_management(db):
    """Odpowiada za obsługę działań na bazie wskazanych przez użytkownika

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych, na której wykonywane są operacje
    """

    while True:
        print('--' * 20)
        print(f"Jesteś połączony z bazą danych '{db.name}'.")
        print(f"W bazie znajdują się następujące tabele: {db.list_tables()}.")
        print()
        print("""Wybierz, co chcesz zrobić:
        1 - stwórz nową tabelę z daniami obiadowymi,
        2 - usuń tabelę,
        3 - dodaj danie obiadowe w istniejącej tabeli,
        4 - usuń danie obiadowe z istniejącej tabeli,
        5 - dodaj kilka dań obiadowych na raz z pliku .csv,
        6 - stwórz plan obiadów na podstawie wybranej tabeli,
        0 - wróć do wyboru bazy danych
        """)
        possible_choices = [0, 1, 2, 3, 4, 5, 6]
        user_choice = user_choice_validation(possible_choices)

        if user_choice == 0:
            break
        elif user_choice == 1:
            create_new_table(db)
        elif user_choice == 2:
            drop_table(db)
        elif user_choice == 3:
            add_record(db)
        elif user_choice == 4:
            delete_record(db)
        elif user_choice == 5:
            add_csv(db)
        elif user_choice == 6:
            lunch_planner(db)


def create_new_table(db):
    """Tworzy nową tabelę w bazie danych

    Tabela przechowuje dane dotyczące dań obiadowych
    Tabela posiada trzy kolumny: id, dish_name (nazwa dania) oraz which_course (z informacją, które to jest danie -
    - pierwsze czy drugie)

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych
    """

    print('--'*20)

    while True:
        print(f"Lista istniejących tabel w bazie danych '{db.name}': {db.list_tables()}")
        # todo: napisac warunek obslugujacy tworzenie istniejacej tabeli (mozna sprobowac zrobic to w klasie)
        new_table = input("Podaj nazwę tworzonej tabeli z daniami obiadowymi lub wpisz '0', "
                          "aby wrócić do wyboru operacji na bazie danych: ")

        if new_table == '0':
            break
        else:
            if new_table in db.list_tables():
                print("Tabela o podanej nazwie już istnieje. Spróbuj podać inną nazwę.")
            else:
                db.create_table(new_table)
                print(f"Pomyślnie utworzono tabelę '{new_table}' w bazie danych '{db.name}'")
                break


def drop_table(db):
    """Usuwa tabelę z bazy danych

    Sprawdza czy dana tabela istnieje
    Jeżeli nie - wyświetlany jest stosowny komunikat

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych
    """

    print('--'*20)

    while True:
        print(f"Lista istniejących tabel w bazie danych '{db.name}': {db.list_tables()}")

        table = input("Podaj nazwę tabeli z daniami obiadowymi, którą chcesz usunąć lub wpisz '0', "
                      "aby wrócić do wyboru operacji na bazie danych: ")

        if table == '0':
            break
        else:
            if table not in db.list_tables():
                print("Tabela o podanej nazwie nie istnieje. Spróbuj podać inną nazwę.")
            else:
                db.drop_table(table)
                print(f"Pomyślnie usunięto tabelę '{table}' z bazy danych '{db.name}'")
                break


def add_record(db):
    """Dodaje nowy rekord (nowe danie) w tabeli

    Wprowadzone przez użytkownika wartości podlegają walidacji przy użyciu
    funkcji: add_new_dish_validation oraz which_course_validation
    Uzytkownik ma możliwość wprowadzania nowych rekordów do tabeli dopóki
    nie odpowie, że chciałby zakończyć ich wprowadzanie

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych
    """

    while True:
        print('--' * 20)
        print(f"Lista istniejących tabel w bazie danych '{db.name}': {db.list_tables()}")
        table_name = input("Podaj nazwę tabeli w której chcesz zapisać nowe danie obiadowe lub wpisz '0', "
                           "aby wrócić do wyboru operacji na bazie danych: ")

        if table_name == '0':
            break
        else:
            if table_name not in db.list_tables():
                print("Tabela o podanej nazwie nie istnieje. Podaj nazwę istniejącej tabeli.")
            else:
                print(f"Teraz możesz dodać nowe danie obiadowe do tabeli '{table_name}'. Podaj poniższe informacje.")
                while True:
                    table = Table(db, table_name)
                    dish_name = add_new_dish_validation(table)
                    which_course = which_course_validation()
                    table.insert(dish_name, which_course)
                    print(f"Pomyślnie dodano nowy zapis w tabeli '{table_name}' z bazy danych '{db.name}'")
                    user_choice = new_record_validation('add')

                    if user_choice == 'nie':
                        break


def delete_record(db):
    """Usuwa wskazany przez użytkownika rekord (danie) z tabeli

    Rekord usuwany jest na podstawie nazwy dania wprowadzonej przez użytkownika
    Nazwa dania podlega walidacji przy użyciu funkcji 'delete_dish_validation'

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych
    """

    while True:
        print('--' * 20)
        print(f"Lista istniejących tabel w bazie danych '{db.name}': {db.list_tables()}")
        table_name = input("Podaj nazwę tabeli w której chcesz usunąć danie obiadowe lub wpisz '0', "
                           "aby wrócić do wyboru operacji na bazie danych: ")

        if table_name == '0':
            break
        else:
            if table_name not in db.list_tables():
                print("Tabela o podanej nazwie nie istnieje. Podaj nazwę istniejącej tabeli.")
            else:
                print(f"Teraz możesz usunąć danie obiadowe z tabeli '{table_name}'. Podaj poniższe informacje.")
                while True:
                    table = Table(db, table_name)
                    dish_name = delete_dish_validation(table)
                    table.delete(dish_name)
                    print(f"Pomyślnie usunięto '{dish_name}' z tabeli '{table_name}' z bazy danych '{db.name}'")
                    user_choice = new_record_validation('delete')

                    if user_choice == 'nie':
                        break


def add_csv(db):
    """Umożliwia użytkownikowi dodanie rekordów (dań) do tabeli przy użyciu pliku .csv

    Funkcja pyta użytkownika o nazwę tabeli, do której mają zostać dodane rekordy
    a następnie wywołuje funkcję 'csv_reader' w celu dodania rekordów

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych
    """

    while True:
        print('--' * 20)
        print(f"Lista istniejących tabel w bazie danych '{db.name}': {db.list_tables()}")
        table_name = input("Podaj nazwę tabeli do której chcesz dodać dania obiadowe przy użyciu pliku .csv lub "
                           "wpisz '0', aby wrócić do wyboru operacji na bazie danych: ")

        if table_name == '0':
            break
        else:
            if table_name not in db.list_tables():
                print("Tabela o podanej nazwie nie istnieje. Podaj nazwę istniejącej tabeli.")
            else:
                print('**'*20)
                print(f"Teraz możesz dodać dania obiadowe do tabeli '{table_name}' przy użyciu pliku .csv.")
                print("W każdym wierszu pliku powinna znajdować się nazwa dania oraz cyfra (1 lub 2)"
                      " wskazująca na to, które to jest danie.")
                print("Dane w wierszu powinny być rozdzielone średnikiem np. 'pomidorowa;1'. Przykładowy plik"
                      " 'example_dishes.csv' znajduje się w katalogu roboczym.")
                print("W przypadku podania dania, które już jest zapisane w tabeli lub podania nieprawidłowej"
                      " cyfry dane z danego wiersza nie zostaną wprowadzone do tabeli.")
                print()
                table = Table(db, table_name)
                csv_reader(table)


def csv_reader(table):
    """Odczytuje dania z pliku csv i zapisuje je w tabeli

    Wykorzystuje funkcję 'reader' z modułu 'csv' do odczytania pliku
    Jeżeli danie już istnieje w tabeli - nie zostaje ono wprowadzone ponownie
    Jeżeli parametr 'which_course' nie jest cyfrą 1 lub 2 - danie również nie zostaje wprowadzone

    Parameters
    ----------
    table: obiekt klasy Table
        obiekt reprezentujący tabelę w bazie danych
    """

    while True:
        file_path = input("Podaj ścieżkę do pliku .csv lub wpisz '0', aby wrócić do wyboru tabeli: ")

        if file_path == '0':
            return
        else:
            try:
                with open(rf"{file_path}", 'r') as file:
                    try:
                        reader = csv.reader(file, delimiter=';')
                        for dish in reader:
                            table.insert(dish[0], int(dish[1]))
                        print(f"Pomyślnie dodano dania obiadowe z pliku .csv do tabeli '{table.table_name}' "
                              f"z bazy danych '{table.database.name}'")
                    except:
                        print("Wystąpił błąd podczas odczytu pliku. Spróbuj zmienić formatowanie pliku.")
            except:
                print(f"Coś poszło nie tak. Prawdopodbnie podana ścieżka jest nieprawidłowa.")


def lunch_planner(db):
    """Tworzy plan obiadów na podstawie danej tabeli

    Dane konieczne do stworzenia planu są pozyskiwane od użytkownika przy użyciu funkcji 'lunch_planner_validation'
    Funkcja tworzy plan, a następnie go wyświetla i zapisuje do pliku .txt w katalogu roboczym
    Funkcja ma również możliwość wyświetlenia planu na dzień dzisiejszy, jeżeli taki znajduje się w planie

    Parameters
    ----------
    db : obiekt klasy Database
        obiekt reprezentujący bazę danych
    """

    while True:
        print('--' * 20)
        print(f"Lista istniejących tabel w bazie danych '{db.name}': {db.list_tables()}")
        table_name = input("Podaj nazwę tabeli, którą chcesz wykorzystać do stworzenia planu obiadów"
                           " lub wpisz '0', aby wrócić do wyboru operacji na bazie danych: ")

        if table_name == '0':
            break
        else:
            if table_name not in db.list_tables():
                print("Tabela o podanej nazwie nie istnieje. Podaj nazwę istniejącej tabeli.")
            else:
                table = Table(db, table_name)
                lunch_planner_data = lunch_planner_validation(table)
                if lunch_planner_data == '0':
                    continue
                else:
                    lunch_plan = LunchPlan(db, table, lunch_planner_data)
                    lunch_plan.make_plan()
                    lunch_plan.print_plan()
                    lunch_plan.save_plan()
                    lunch_plan.lunch_for_today()
                    print("Teraz powrócisz do możliwości wyboru tabeli w celu stworzenia planu obiadów.")
