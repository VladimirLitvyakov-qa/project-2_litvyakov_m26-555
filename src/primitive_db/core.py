from decorators import confirm_action, create_cacher, handle_db_errors, log_time
from primitive_db.utils import load_table_data

cacher = create_cacher()


@handle_db_errors
def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict | None:
    """
    Обновляет словарь с метаданными

    :param metadata: словарь с таблицами
    :param table_name: имя таблицы
    :param columns: колонки
    :return: обновленный metadata или None при ошибке
    """
    if not isinstance(metadata, dict):
        raise TypeError(f"metadata must be dict, but got {type(metadata).__name__}")

    if not isinstance(table_name, str):
        raise TypeError(f"table_name must be str, but got {type(table_name).__name__}")

    if not isinstance(columns, list):
        raise TypeError(f"columns must be list, but got {type(columns).__name__}")

    for table in metadata:
        if table_name == table:
            raise ValueError(f'таблица "{table_name}" уже существует.')

    for colum in columns:
        if not isinstance(colum, str):
            raise TypeError(f"colum must be str, but got {type(colum).__name__}")

        i = colum.find(":")
        if colum[i + 1 :] not in ("int", "str", "bool") or i == -1:
            raise ValueError(f"некорректное значение: {colum}. Попробуйте снова.")

    if "ID:int" not in columns:
        columns.insert(0, "ID:int")

    metadata[table_name] = columns
    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata: dict, table_name: str) -> dict | None:
    """
    Удаляет информацию о таблице

    :param metadata: словарь с таблицами
    :param table_name: имя таблицы
    :return: обновленный metadata или None при ошибке или отмене
    """
    if not isinstance(metadata, dict):
        raise TypeError(f"metadata must be dict, but got {type(metadata).__name__}")

    if not isinstance(table_name, str):
        raise TypeError(f"table_name must be str, but got {type(table_name).__name__}")

    if table_name not in metadata:
        raise KeyError(table_name)

    del metadata[table_name]
    return metadata


@log_time
@handle_db_errors
def insert(metadata: dict, table_name: str, values: list) -> list | None:
    """
    Добавляет новую запись в таблицу

    :param metadata: словарь с таблицами
    :param table_name: имя таблицы
    :param values: новые значения
    :return: таблица с данными или None
    """
    if not isinstance(metadata, dict):
        raise TypeError(f"metadata must be dict, but got {type(metadata).__name__}")

    if not isinstance(table_name, str):
        raise TypeError(f"table_name must be str, but got {type(table_name).__name__}")

    if not isinstance(values, list):
        raise TypeError(f"values must be list, but got {type(values).__name__}")

    if table_name not in metadata:
        raise KeyError(table_name)

    if len(values) + 1 != len(metadata[table_name]):
        raise ValueError(f"некорректное значение: {values}. Попробуйте снова.")

    new_row = {}
    for table_value, value in zip(metadata[table_name][1:], values):
        i = table_value.find(":")
        if table_value[i + 1 :] != type(value).__name__:
            raise ValueError(f"некорректное значение: {value}. Попробуйте снова.")
        new_row[table_value[:i]] = value

    table_data = load_table_data(table_name)
    ids = [data["ID"] for data in table_data]
    if table_data:
        new_id = max(ids) + 1
    else:
        new_id = 1

    result_row = {"ID": new_id} | new_row
    table_data.append(result_row)
    return table_data


@log_time
@handle_db_errors
def select(table_data: list[dict], where_clause: dict = None) -> list[dict] | None:
    """
    Возвращает данные по условию where_clause, если данные отсутствуют,
    возвращает все данные

    :param table_data: таблица с данными
    :param where_clause: условие выборки
    :return: результирующий список или None
    """
    if not isinstance(table_data, list):
        raise TypeError(f"table_data must be list, but got {type(table_data).__name__}")

    if where_clause is None:
        return table_data

    if not isinstance(where_clause, dict):
        raise TypeError(
            f"where_clause must be dict, but got {type(where_clause).__name__}"
        )

    if len(where_clause) > 1:
        raise ValueError(f"некорректное значение: {where_clause}. Попробуйте снова.")

    cache_key = f"{table_data}{where_clause}"

    def filter_data() -> list[dict]:
        """Фильтрует записи по условию where_clause"""
        result = []
        for data in table_data:
            for key, value in where_clause.items():
                if data.get(key) == value:
                    result.append(data)

        return result

    return cacher(cache_key, filter_data)


def update(table_data: list[dict], set_clause: dict, where_clause: dict) -> list[dict]:
    """
    Находит записи по условию where_clause и обновляет в
    найденных записях поля согласно set_clause

    :param table_data: таблица с данными
    :param set_clause: данные для обновления
    :param where_clause: условия выборки
    :return: таблица с данными
    """
    if not isinstance(table_data, list):
        raise TypeError(f"table_data must be list, but got {type(table_data).__name__}")

    if not isinstance(set_clause, dict):
        raise TypeError(f"set_clause must be dict, but got {type(set_clause).__name__}")

    if not isinstance(where_clause, dict):
        raise TypeError(
            f"where_clause must be dict, but got {type(where_clause).__name__}"
        )

    for data in table_data:
        for k1, v1 in where_clause.items():
            if data.get(k1) == v1:
                for k2, v2 in set_clause.items():
                    if data.get(k2) is not None:
                        data[k2] = v2

    return table_data


@confirm_action("удаление записи")
def delete(table_data: list, where_clause: dict) -> list:
    """
    Находит записи по where_clause и удаляет их

    :param table_data: таблица с данными
    :param where_clause: условия для выборки
    :return: таблица с данными
    """
    if not isinstance(table_data, list):
        raise TypeError(f"table_data must be list, but got {type(table_data).__name__}")

    if not isinstance(where_clause, dict):
        raise TypeError(
            f"where_clause must be dict, but got {type(where_clause).__name__}"
        )

    result = []
    for data in table_data:
        for key, value in where_clause.items():
            if data.get(key) == value:
                continue
            result.append(data)

    return result
