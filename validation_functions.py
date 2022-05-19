"""Moduł zawiera funkcje wykorzystywane do walidacji danych w programie

Zawiera definicje następujących funkcji:
    * user_choice_validation - służy do walidacji wyboru użytkownika
    * which_course_validation - sprawdza, czy użytkownik wprowadził odpowiedni numer dania
    * new_record_validation - pyta użytkownika, czy chce dodać lub usunąć kolejny rekord w tabeli
    * add_new_dish_validation - pyta użytkownika o nazwę dania, które chce wprowadzić do tabeli
    * delete_dish_validation - pyta użytkownika o nazwę dania, które chce usunąć z tabeli
    * lunch_planner_validation - pyta użytkownika o parametry dotyczące tworzonego planu obiadów
"""

import datetime


def user_choice_validation(possible_choices):
    """Służy do walidacji wyboru użytkownika w różych częściach programu

    Sprawdza czy wybór użytkownika znajduje się na przekazanej liście możliwych wyborów

    Parameters
    ----------
    possible_choices : list
        lista składająca się z liczb odpwoiadającyh możliwym wyborom uzytkownika

    Returns
    ----------
    user_choice : int
        zwalidowany wybór użytkownika

    Raises
    ----------
    ValueError
        zwraca wyjątek jeżeli wprowadzona przez użytkownika wartość nie może być zamieniona na liczbę całkowitą
    """

    while True:
        try:
            user_choice = int(input('Wpisz odpowiednią cyfrę: '))
            if user_choice in possible_choices:
                return user_choice
            else:
                print(f'Możliwe do wyboru są tylko cyfry: {possible_choices}')

        except ValueError:
            print('Podana wartość musi być liczbą!!!')


def which_course_validation():
    """Sprawdza, czy użytkownik wprowadził odpowiedni numer dania (1 lub 2)

    Wprowadzona przez użytkownika liczba powinna się znajdować na liście 'possible_choices'

    Returns
    ----------
    which_course : int
        liczba odpowiadająca kolejności dań - 1 lub 2

    Raises
    ----------`
    ValueError
        zwraca wyjątek, jeżeli wprowadzona prez użytkownika wartość nie może zostać zamieniona na liczbę całkowitą
    """
    possible_choices = [1, 2]

    while True:
        which_course = input("Które to jest danie, pierwsze czy drugie? Wpisz odpowiednio '1' lub '2': ")
        try:
            which_course = int(which_course)
            if which_course in possible_choices:
                return which_course
            else:
                print("Podano liczbę spoza dostępnych możliwości!")
        except ValueError:
            print("Możesz podać tylko liczbę!")


def new_record_validation(option):
    """Pyta użytkownika czy chce dodać/usunąć kolejny rekord w tabeli

    Parametr 'option' decyduje, czy funkcja pyta użytkownika o dodanie nowego rekordu czy o usunięcie
    Funkcja sprawdza czy odpowiedź wprowadzona przez użytkownika znajduje sie na liście możliwych
    odpowiedzi 'posssibe_choices'

    Parameters
    ----------
    option : str
        parametr ten wskazuje, czy funkcja powinna pytać użytkownika o dodanie czy usunięcie rekordu

    Returns
    ----------
    user_choice : str
        zwalidowana wartość wprowadzona przez użytkownika - "tak" lub "nie"
    """

    possible_options = ['tak', 'nie']

    if option == 'add':
        operation = 'dodać'
    else:
        operation = 'usunąć'

    while True:
        user_choice = input(f"Czy chcesz {operation} kolejne danie obiadowe w tej tabeli? Wpisz 'tak' lub 'nie': ")

        if user_choice in possible_options:
            return user_choice
        else:
            print("Podano wartość spoza dostepnych możliwości!")


def add_new_dish_validation(table):
    """Pyta użytkownika o nazwę dania, które chce wprowadzić do tabeli

    Sprwdza, czy danie znajduje się już w tabeli
    Jeżeli znajduje się - wyświetlany jest komunikat o niemożliwości ponownego wprowadzenia dania

    Parameters
    ----------
    table : obiekt klasy Table
        obiekt reprezentujący tabelę w bazie danych

    Returns
    ----------
    dish_name : str
        nazwa dania wprowadzanego do tabeli
    """
    unavailable_choices = [dish[0] for dish in table.list_dishes()]

    while True:
        dish_name = input("Nazwa dania: ")

        if dish_name not in unavailable_choices:
            return dish_name
        else:
            print(f"{dish_name.title()} już istnieje w tabeli! Podaj inne danie.")


def delete_dish_validation(table):
    """Pyta użytkownika o nazwę dania, które chce usunąć z tabeli

    Sprwdza, czy danie znajduje się w tabeli
    Jeżeli nie znajduje się - wyświetlany jest komunikat o niemożliwości usunięcia dania

    Parameters
    ----------
    table : obiekt klasy Table
        obiekt reprezentujący tabelę w bazie danych

    Returns
    ----------
    dish_name : str
        nazwa dania usuwanego z tabeli
    """

    available_choices = [dish[0] for dish in table.list_dishes()]

    while True:
        dish_name = input("Nazwa dania: ")

        if dish_name in available_choices:
            return dish_name
        else:
            print(f"{dish_name.title()} nie istnieje w tabeli! Podaj inne danie do usunięcia.")


def lunch_planner_validation(table):
    """Pyta użytkownika o parametry dotyczące tworzonego planu obiadów

    Parametrami tymi są:
        * lunch_plan_name (str) - nazwa tworzonego planu
        * start_date (obiekt klasy datetime.datetime) - data początkowa planu
        * end_date (obiekt klasy datetime.datetime) - data końcowa planu
        * min_time_interval (int) - odstęp czasu liczny w dniach, w którym obiad nie może się powtórzyć
    Powyższe parametry podlegaja odpowiedniej walidacji.

    Parameters
    ----------
    table : obiekt klasy Table
        obiekt reprezentujący tabelę w bazie danych

     Returns
     ----------
     tupla z wymienionymi wyżej parametrami
    """

    print('--'*20)
    print("Teraz podaj niezbędne dane do stworzenia planu obiadów dla dowolnego przedziału czasu.")
    print("W dowolnym momencie możesz również wpisać '0', aby powrócić do wyboru tabeli.")
    print()

    lunch_plan_name = input("Podaj dowolną nazwę dla tworzonego planu obiadów: ")

    if lunch_plan_name == '0':
        return '0'

    while True:
        try:
            start_date = input("Podaj datę początkową planu obiadów w formacie 'dzień-miesiąc-rok': ")
            if start_date == '0':
                return '0'
            else:
                start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').date()
                break
        except ValueError:
            print("Błąd w formatowaniu daty. Spróbuj ponownie wpisać datę w podanym formacie.")

    while True:
        try:
            end_date = input("Podaj datę końcową planu obiadów w formacie 'dzień-miesiąc-rok': ")
            if end_date == '0':
                return '0'
            else:
                end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
                if end_date < start_date:
                    print("Data końcowa nie może być wcześniejsza od daty początkowej! Spróbuj jeszcze raz wprowadzić "
                          "datę końcową.")
                    continue
                else:
                    break
        except ValueError:
            print("Błąd w formatowaniu daty. Spróbuj ponownie wpisać datę w podanym formacie.")

    while True:
        try:
            number_of_dishes = len(table.list_dishes())
            min_time_interval = input(f"Podaj minimalny odstęp czasu liczony w dniach, w którym żaden obiad nie może "
                                      f"się powtórzyć (większy lub równy 2, ale nie większy niż liczba dań w bazie "
                                      f"równa {number_of_dishes}): ")

            if min_time_interval == '0':
                return '0'
            else:
                min_time_interval = int(min_time_interval)
                if min_time_interval >= 2 and min_time_interval <= number_of_dishes:
                    break
                else:
                    print(f"Podaj liczbę większą lub równą 2 oraz nie większą niż {number_of_dishes}!")
        except ValueError:
            print("Możesz wpisać tylko liczbę całkowitą!")

    return lunch_plan_name, start_date, end_date, min_time_interval
