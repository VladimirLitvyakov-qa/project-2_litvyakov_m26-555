import json
from pathlib import Path


def load_metadata(filepath: str) -> dict:
    """
    Загружает данные из JSON-файла

    :param filepath: относительный путь к файлу .json
    :return: словарь
    """
    if not isinstance(filepath, str):
        raise TypeError(f"filepath must be string, but got {type(filepath).__name__}")

    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """
    Сохраняет переданные данные в JSON-файл

    :param filepath: относительный путь к файлу .json
    :param data: словарь
    """
    if not isinstance(filepath, str):
        raise TypeError(f"filepath must be string, but got {type(filepath).__name__}")

    if not isinstance(data, dict):
        raise TypeError(f"data must be dict, but got {type(data).__name__}")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_table_data(table_name: str) -> dict:
    """
    Загружает данные из JSON-файла

    :param table_name: имя таблицы
    :return: словарь
    """
    if not isinstance(table_name, str):
        raise TypeError(
            f"table_name must be string, but got {type(table_name).__name__}"
        )

    try:
        with open(f"./data/{table_name}.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_table_data(table_name, data) -> None:
    """
    Сохраняет переданные данные в JSON-файл

    :param table_name: название таблицы
    :param data: словарь
    """
    if not isinstance(table_name, str):
        raise TypeError(
            f"table_name must be string, but got {type(table_name).__name__}"
        )

    if not isinstance(data, dict):
        raise TypeError(f"data must be dict, but got {type(data).__name__}")

    folder_path = Path("data")
    folder_path.mkdir(parents=True, exist_ok=True)
    with open(f"./data/{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
