import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata

PATH = "db_meta.json"


def print_help() -> None:
    """Печатает вспомогательные сообщения для верного выбора"""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run() -> None:
    """Запускает основной цикл. Читает команды пользователя и выполняет их"""
    print_help()

    while True:
        metadata = load_metadata(PATH)
        user_input = prompt.string(">>>Введите команду: ")

        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Некорректное значение: незакрытая кавычка. Попробуйте снова.")
            continue

        if len(args) < 1:
            print("Неизвестная команда. Попробуйте снова")
            continue

        match args[0]:
            case "create_table":
                if len(args) < 2:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue
                upd_data = create_table(metadata, args[1], args[2:])
                if upd_data is not None:
                    save_metadata(PATH, upd_data)
                    col = ", ".join(metadata[args[1]])
                    print(f'Таблица "{args[1]}" успешно создана со столбцами: {col}')
            case "list_tables":
                for table in metadata:
                    print(f"- {table}")
            case "drop_table":
                if len(args) < 2:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue
                upd_data = drop_table(metadata, args[1])
                if upd_data is not None:
                    save_metadata(PATH, upd_data)
                    print(f'Таблица "{args[1]}" успешно удалена.')
            case "exit":
                break
            case "help":
                print_help()
            case _:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
