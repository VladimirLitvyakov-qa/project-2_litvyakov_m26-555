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
