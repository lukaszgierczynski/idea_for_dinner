"""Moduł zawiera definicje wszystkich klas wykorzystywanych w programie

Zawiera definicję nstępujących klas:
    * Database - klasa reprezenyująca bazę danych SQLite,
    * Table - klasa reprezentująca tabelę w bazie danych,
    * LunchPlan - klasa reprezentująca plan obiadów.
"""

import os
import sqlite3
import datetime
import random
import time


class Database:
    """
    Klasa reprezentująca bazę danych SQLite

    Attributes
    ----------
    name : str
        nazwa bazy danych w z rozszerzeniem '.db'
    connection : instancja klasy sqlite.Connection
        obiekt pozwalający na połączenie z bazą danych
    cursor : instancja klasy sqlite.Cursor
        kursor dla połączenia z bazą danych
    list_of_tables : list
        lista zawierająca nazwy wszystkich tabel znajdujących się w bazie danych

    Methods
    ----------
    close_connection()
        zamyka połączenie z bazą danych
    create_table(table_name)
        tworzy tabelę w bazie danych o nazwie table_name
    drop_table(table_name)
        usuwa z bazy danych tabelę o nazwie table_name
    list_tables()
        zwraca listę z nazwami wszystkich tabel znajdujących się w bazie danych
    delete_database()
        usuwa plik z bazą danych z katalogu 'databases'
    """

    def __init__(self, name):
        """Tworzy nową bazę danych w katalogu databases

        Parameters
        ----------
        name : str
            nazwa bazy danych w z rozszerzeniem '.db'
        """

        self.name = name
        self.connection = sqlite3.connect("databases\\" + self.name)
        self.cursor = self.connection.cursor()
        self.list_of_tables = []

    def __del__(self):
        """
        Zamyka połączenie z bazą danych w przypadku usunięcia obiektu tej klasy np. w przypadku wyłączenia programu
        """
        self.connection.close()

    def close_connection(self):
        """Zamyka połączenie z bazą danych """

        self.connection.close()

    def create_table(self, table_name):
        """Tworzy tabelę w bazie danych

        Parameters
        ----------
        table_name : str
            nazwa tworzonej tabeli
        """

        self.cursor.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, dish_name TEXT,"
                            f" which_course INTEGER)")
        self.connection.commit()

    def drop_table(self, table_name):
        """Usuwa tabelę w bazie danych

        Parameters
        ----------
        table_name : str
            nazwa usuwanej tabeli
        """

        self.cursor.execute(f'DROP TABLE {table_name}')
        self.connection.commit()

    def list_tables(self):
        """Wykonuje zapytanie do bazy danych dotyczące listy wszystkich tabel

        Returns
        -------
        list
            lista z nazwami wszystkich tabel znajdujących się w bazie
        """

        self.cursor.execute('SELECT name from sqlite_master where type= "table"')
        self.list_of_tables = [table[0] for table in self.cursor.fetchall()]
        return self.list_of_tables

    def delete_database(self):
        """Usuwa plik z bazą danych z katalogu 'databases'"""

        self.close_connection()
        os.remove(os.path.join(os.getcwd(), 'databases', self.name))


class Table:
    """Klasa reprezentująca tabelę w bazie danych

    Attributes
    ----------
    database : instancja klasy Database
        baza danych, w której znajduje się tabela
    table_name : str
        nazwa tabeli
    list_of_dishes : list
        lista zawierająca dane z poszczególnych wierszy znajdujących się w tabeli

    Methods
    ----------
    insert(dish_name, which_course)
        dodaje nowe danie w tabeli
    delete(dish_name)
        usuwa danie z tabeli
    list_dishes()
        zwraca listę zawierającą dane z poszczególnych wierszy znajdujących się w tabeli
    """

    def __init__(self, database, table_name):
        """
        Parameters
        ----------
        database : instancja klasy Database
            baza danych, w której znajduje się tabela
        table_name : str
            nazwa tabeli
        """
        self.database = database
        self.table_name = table_name

    def insert(self, dish_name, which_course):
        """Wprowadza do tabeli nowe danie, jeżeli się w niej nie znajduje
        Aby danie zostało wprowadzone parametr 'which_course' musi być cyfrą 1 lub 2

        Parameters
        ----------
        dish_name : str
            nazwa dania
        which_course : int
            numer dania - 1 lub 2
        """

        dishes_inserted = [dish[0] for dish in self.list_dishes()]
        available_courses = [1, 2]
        if dish_name not in dishes_inserted and which_course in available_courses:
            self.database.cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?)", (None, dish_name, which_course))
            self.database.connection.commit()

    def delete(self, dish_name):
        """Usuwa z tabeli danie o podanej nazwie

        Parameters
        ----------
        dish_name : str
            nazwa dania
        """

        self.database.cursor.execute(f"DELETE FROM {self.table_name} WHERE dish_name =?", (dish_name, ))
        self.database.connection.commit()

    def list_dishes(self):
        """Zwraca listę z danymi z poszczególnych rekordów w tabeli

        Returns
        ----------
        list_of_dishes : list
            lista z danymi z poszczególnych rekordów w tabeli w postaci krotek
        """

        self.database.cursor.execute(f"SELECT dish_name, which_course FROM {self.table_name}")
        self.list_of_dishes = [dish for dish in self.database.cursor.fetchall()]
        return self.list_of_dishes


class LunchPlan:
    """Klasa reprezentująca plan obiadów

    Attributes
    ----------
    database : instancja klasy Database
        baza danych, w której znajduje się tabela, na podstawie której tworzony jest plan
    table : instancja klasy Table
        tabela, na podstawie której tworzony jest plan
    name : str
        nazwa własna planu
    start_date : instancja klasy datetime.datetime
        data początkowa planu
    end_date : instancja klasy datetime.datetime
        data końcowa planu
    min_interval_time : int
        odstęp czasu liczony w dniach, w którym żaden obiad nie może się powtórzyć
    days : list
        lista z datami (instancje klasy datetime.datetime) pomiędzy datą poczatkową a końcową
    days_to_str : list
        lista z datami w postaci stringow pomiędzy datą początkową a końcową
    list_of_dishes : list
        lista z danymi z poszczególnych wierszy tabeli, na podstawie której tworzony jest plan
    lunch_plan : list
        lista z gotowym planem obiadów - składa się z krotek zawierających dane o dniu i obiedzie
    """

    def __init__(self, database, table, lunch_planner_data: tuple):
        """
        Parameters
        ----------
        database : instancja klasy Database
            baza danych, w której znajduje się tabela, na podstawie której tworzony jest plan
        table : instancja klasy Table
            tabela, na podstawie której tworzony jest plan
        lunch_planner_data: tuple
            krotka zawierajaca dane niezbędne do stworzenia planu: name, start_date, end_date, min_interval_time
        """

        self.database = database
        self.table = table
        self.name = lunch_planner_data[0]
        self.start_date = lunch_planner_data[1]
        self.end_date = lunch_planner_data[2]
        self.min_interval_time = lunch_planner_data[3]
        self.days = []
        self.days_to_str = []
        self.list_of_dishes = self.table.list_dishes()
        self.lunch_plan = []

    def make_plan(self):
        """ Zwraca wygenerowany plan obiadów w postaci listy

        Wykorzystuje funkcję choice z modułu random do wskazania losowego obiadu z tabeli
        Funkcja sprawdza, czy wylosowany obiad wystąpił w poprzednich dniach określonych przez atrybut min_interval_time
        Jeżeli wystąpił - losowany jest nowy obiad i ponownie wykonywane jest wspomniane sprawdzenie

        Returns
        ----------
        lunch_plan : list
            lista z gotowym planem obiadów - składa się z krotek zawierających dane o dniu i obiedzie
        """

        delta = self.end_date - self.start_date
        self.days = [self.start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]

        for date in self.days:
            while True:
                dinner = random.choice(self.list_of_dishes)
                if dinner[0] not in [x[1] for x in self.lunch_plan[-self.min_interval_time + 1:]]:
                    self.lunch_plan.append((date, dinner[0]))
                    break

        return self.lunch_plan

    def print_plan(self):
        """Wyświetla w konsoli plan obiadów

        Ponadto zamienia daty znajdujące się w tabeli lunch_plan na datę w formacie dzień-miesiąc-rok
        """

        start_date_str = self.start_date.strftime('%d-%m-%Y')
        end_date_str = self.end_date.strftime('%d-%m-%Y')

        print(f"Oto plan '{self.name}' wygenerowany dla okresu {start_date_str} - {end_date_str}:")
        for x in self.lunch_plan:
            print(f"{x[0].strftime('%d-%m-%Y')} --> {x[1]}")

    def save_plan(self):
        """Zapisuje plan obiadów do pliku z rozszerzeniem .txt

        Plik zapisywany jest w katalogu roboczym
        """

        file_name = f"{self.name}.txt"
        print("Plan w postaci pliku .txt zostanie zapisany w katalogu roboczym.")

        with open(file_name, 'w') as file:
            for x in self.lunch_plan:
                file.write(f"{x[0].strftime('%d-%m-%Y')} --> {x[1]}" + "\n")

        for x in range(3, 0, -1):
            print(x)
            time.sleep(1)

        if os.path.exists(file_name):
            print("Plik został pomyślnie zapisany w katalogu roboczym.")

    def lunch_for_today(self):
        """Pyta użytkownika, czy chce aby wyświetlony został obiad z planu na dzień dziesiejszy

        W przypadku twierdzącej odpowiedzi wyświetla obiad
        Gdy dzisiejszy dzień nie został uwzlędniony w planie - wyświetlony zostaje stosowny komunikat
        """

        today = datetime.date.today()
        today_str = today.strftime('%d-%m-%Y')

        while True:
            user_choice = input("Czy chcesz, aby wyświetlony został obiad na dzisiaj? Wpisz 'tak' lub 'nie': ")

            if user_choice == 'nie':
                break
            elif user_choice == 'tak':
                if today not in self.days:
                    print(f"Dzisiejszy dzień tj. {today_str} nie został uwzględniony w planie.")
                    break
                else:
                    for date, dinner in self.lunch_plan:
                        if date == today:
                            lunch_for_today = dinner
                            print(f"Obiad na dzisiaj ({today_str}) to: {lunch_for_today}.")
                            break
                    break
            else:
                print("Możesz wpisać tylko 'tak' lub 'nie'")
