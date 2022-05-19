"""Główny skrypt programu służącego do tworzenia planów obiadów na podstawie baz danych SQLite.

Na początku skrypt importuje z innych modułów funkcje pomocnicze wykorzystane w głównej funkcji programu.
Następnie skrypt zawiera definicję głównej funkcji programu, która odpowiada za działanie całego programu.
Na koniec skryptu główna funkcja jest wywoływana.
"""

import os
from main_functions import create_new_database, delete_database
from database_management_functions import connect_database
from validation_functions import user_choice_validation


def main():
    """Główna funkcja programu odpowiadająca za całe jego działanie.

    Na początku funkcja zapisuje do listy 'database_list' nazwy wszystkich plików .db z bazami danych SQLite
    znajdujących się w katalogu 'databases' - dzięki temu możliwe jest wykonanie operacji na istniejącej bazie.
    Następnie funkcja wskazuje użytkownikowi możliwości operacji do wykonania na bazach danych oraz
    odbiera od użytkownika wartość wskazującą na wykonanie konkretnej operacji.
    Odebrana wartość podlega walidacji - może być jedną z wartości znajdujących się w zmiennej 'possible_choices'.
    Po zwalidowaniu wartości wywoływana jest funkcja odpowiadająca za wykonanie konkretnej operacji na bazach danych.
    Wszystkie powyższe instrukcje są powtarzane w pętli 'while'.
    Aby zakończyć działnie pętli i tym samym działanie programu użytkownik może wpisać wartość "0".
    """

    while True:
        database_list = [file for file in os.listdir(os.getcwd() + "/databases/") if file.endswith('.db')]

        print('--' * 20)
        print('Lista istniejących baz danych:', database_list)
        print()
        print("""Wybierz, co chcesz zrobić:
        1 - stwórz nową bazę danych,
        2 - usuń bazę danych,
        3 - wykonaj dowolną operację w istniejącej bazie danych,
        0 - wyłącz program
        """)
        possible_choices = [0, 1, 2, 3]
        user_choice = user_choice_validation(possible_choices)

        if user_choice == 0:
            break
        elif user_choice == 1:
            create_new_database(database_list)
        elif user_choice == 2:
            delete_database(database_list)
        elif user_choice == 3:
            connect_database(database_list)


if __name__ == "__main__":
    main()
