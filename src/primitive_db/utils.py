import json


def load_metadata(filepath: str) -> dict:
    """
    Загружает данные из JSON-файла

    :param filepath: относительный путь к файлу .json
    :return: словарь
    """
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
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)