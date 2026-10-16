from primitive_db.utils import load_table_data


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
            print(f'Ошибка: Таблица "{table_name}" уже существует.')
            return None

    for colum in columns:
        if not isinstance(colum, str):
            raise TypeError(f"colum must be str, but got {type(colum).__name__}")

        i = colum.find(":")
        if colum[i + 1 :] not in ("int", "str", "bool") or i == -1:
            print(f"Некорректное значение: {colum}. Попробуйте снова.")
            return None

    if "ID:int" not in columns:
        columns.insert(0, "ID:int")

    metadata[table_name] = columns
    return metadata


def drop_table(metadata: dict, table_name: str) -> dict | None:
    """
    Удаляет информацию о таблице

    :param metadata: словарь с таблицами
    :param table_name: имя таблицы
    :return: обновленный metadata или None при ошибке
    """
    if not isinstance(metadata, dict):
        raise TypeError(f"metadata must be dict, but got {type(metadata).__name__}")

    if not isinstance(table_name, str):
        raise TypeError(f"table_name must be str, but got {type(table_name).__name__}")

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    del metadata[table_name]
    return metadata


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
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    if len(values) + 1 != len(metadata[table_name]):
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return None

    new_row = {}
    for table_value, value in zip(metadata[table_name][1:], values):
        i = table_value.find(":")
        if table_value[i + 1 :] != type(value).__name__:
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return None
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
