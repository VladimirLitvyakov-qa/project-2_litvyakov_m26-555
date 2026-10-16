import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import create_table, drop_table, insert, select
from primitive_db.parser import parse_value, parse_where_and_set
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

PATH = "db_meta.json"


def print_help() -> None:
    """Печатает вспомогательные сообщения для верного выбора"""
    print("\n***Процесс работы с таблицей***")
    print("\nФункции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("\nФункции:")
    print(
        "<command> insert into <имя_таблицы> "
        "values (<значение1>, <значение2>, ...) - создать запись"
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию"
    )
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print(
        "<command> update <имя_таблицы> set <столбец1> = "
        "<новое_значение1> where <столбец_условия> = "
        "<значение_условия> - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись"
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице")

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
            case "insert":
                if len(args) < 3:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                start = user_input.find("(")
                end = user_input.find(")")

                if start == -1 or end == -1 or start >= end:
                    print("Некорректный формат записи.")
                    continue

                values = [
                    parse_value(v.strip())
                    for v in user_input[start + 1 : end].split(",")
                ]
                table_data = insert(metadata, args[2], values)

                if table_data:
                    save_table_data(args[2], table_data)
                    print(
                        f'Запись с ID={table_data[-1]["ID"]} успешно добавлена '
                        f'в таблицу "{args[2]}".'
                    )
            case "select":
                if len(args) < 3:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                if args[2] not in metadata:
                    print(f'Ошибка: Таблица "{args[2]}" не существует.')
                    continue

                table_data = load_table_data(args[2])

                if len(args) > 3 and args[3] == "where":
                    start = user_input.find("where ") + len("where ")
                    values = parse_where_and_set(user_input[start:])

                    if values is None:
                        continue

                    result = select(table_data, values)
                else:
                    result = select(table_data)

                table = PrettyTable()
                table.field_names = [k[: k.find(":")] for k in metadata[args[2]]]

                for row in result:
                    table.add_row(list(row.values()))

                print(table)
            case "update":
                ...
            case "delete":
                ...
            case "info":
                ...
            case "exit":
                break
            case "help":
                print_help()
            case _:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
