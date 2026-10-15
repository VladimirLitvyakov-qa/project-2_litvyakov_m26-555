import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata

PATH = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print("Первая попытка запустить проект!")
    print()
    print(3 * "*")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        metadata = load_metadata(PATH)
        user_input = prompt.string(">>>Введите команду: ")
        args = shlex.split(user_input)

        match args[0]:
            case "create_table":
                upd_data = create_table(metadata, args[1], args[2:])
                if upd_data is not None:
                    save_metadata(PATH, upd_data)
            case "drop_table":
                upd_data = drop_table(metadata, args[1])
                if upd_data is not None:
                    save_metadata(PATH, upd_data)
            case "help":
                print_help()
            case "exit":
                break
            case _:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
