import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import create_table, delete, drop_table, insert, select, update
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
                if not metadata:
                    print("Таблицы отсутствуют")
                    continue

                for table in metadata:
                    print(f"- {table}")
            case "drop_table":
                if len(args) < 2:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue
                upd_data = drop_table(metadata, args[1])
                if upd_data is not None:
                    save_metadata(PATH, upd_data)
                    save_table_data(args[1], [])
                    print(f'Таблица "{args[1]}" успешно удалена.')
            case "insert":
                if len(args) < 3:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                table_name = args[2]
                start = user_input.find("(")
                end = user_input.find(")")

                if start == -1 or end == -1 or start >= end:
                    print("Некорректный формат записи.")
                    continue

                values = [
                    parse_value(v.strip())
                    for v in user_input[start + 1 : end].split(",")
                ]
                table_data = insert(metadata, table_name, values)

                if table_data:
                    save_table_data(table_name, table_data)
                    print(
                        f"Запись с ID={table_data[-1]['ID']} успешно добавлена "
                        f'в таблицу "{table_name}".'
                    )
            case "select":
                if len(args) < 3:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                table_name = args[2]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)

                if len(args) > 3 and args[3] == "where":
                    start = user_input.find("where ") + len("where ")
                    values = parse_where_and_set(user_input[start:])

                    if values is None:
                        continue

                    result = select(table_data, values)
                else:
                    result = select(table_data)

                if result is None:
                    continue

                table = PrettyTable()
                table.field_names = [k[: k.find(":")] for k in metadata[table_name]]

                for row in result:
                    table.add_row(list(row.values()))

                print(table)
            case "update":
                if len(args) < 2:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                table_name = args[1]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)

                if len(args) < 7 or args[2] != "set" or args[6] != "where":
                    print("Некорректное значение. Попробуйте снова.")
                    continue

                start_set = user_input.find("set ") + len("set ")
                end_set = user_input.find(" where")
                value_set = parse_where_and_set(user_input[start_set:end_set])

                if value_set is None:
                    continue

                start_where = user_input.find("where ") + len("where ")
                value_where = parse_where_and_set(user_input[start_where:])

                if value_where is None:
                    continue

                ids = [i["ID"] for i in select(table_data, value_where)]
                update_data = update(table_data, value_set, value_where)

                if update_data is None:
                    continue

                save_table_data(table_name, update_data)
                if len(ids) == 1:
                    print(
                        f"Запись с ID={ids[0]} в таблице "
                        f'"{table_name}" успешно обновлена.'
                    )
                elif len(ids) > 1:
                    print(
                        f"Записи с IDs={', '.join(map(str, ids))} в таблице "
                        f'"{table_name}" успешно обновлены.'
                    )
            case "delete":
                if len(args) < 3:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                table_name = args[2]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                table_data = load_table_data(table_name)

                if len(args) < 4 or args[3] != "where":
                    print("Некорректное значение. Попробуйте снова.")
                    continue

                start = user_input.find("where ") + len("where ")
                clause = parse_where_and_set(user_input[start:])

                if clause is None:
                    continue

                ids = [i["ID"] for i in select(table_data, clause)]
                delete_data = delete(table_data, clause)

                if delete_data is None:
                    continue

                save_table_data(table_name, delete_data)
                if len(ids) == 1:
                    print(
                        f"Запись с ID={ids[0]} успешно удалена "
                        f'из таблицы "{table_name}".'
                    )
                elif len(ids) > 1:
                    print(
                        f"Записи с IDs={', '.join(map(str, ids))} успешно удалены "
                        f'из таблицы "{table_name}".'
                    )
            case "info":
                if len(args) < 2:
                    print("Не указано имя таблицы. Попробуйте снова.")
                    continue

                table_name = args[1]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue

                count = len(load_table_data(table_name))

                print(f"Таблица: {table_name}")
                print(f"Столбцы: {', '.join(metadata[table_name])}")
                print(f"Количество записей: {count}")
            case "exit":
                break
            case "help":
                print_help()
            case _:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
