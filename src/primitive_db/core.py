def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict | None:
    """
    Обновляет словарь с метаданными

    :param metadata: словарь с таблицами
    :param table_name: имя таблицы
    :param columns: колонки
    :return: обновленный metadata или None при ошибке
    """
    for table in metadata:
            if table_name == table:
                print(f'Ошибка: Таблица "{table_name}" уже существует.')
                return None

    for colum in columns:
        i = colum.find(":")

        if colum[i+1:] not in ("int", "str", "bool") or i == -1:
            print(f'Некорректное значение: {colum}. Попробуйте снова.')
            return None

    if "ID:int" not in columns:
        columns.insert(0, "ID:int")

    metadata[table_name] = columns
    return metadata
