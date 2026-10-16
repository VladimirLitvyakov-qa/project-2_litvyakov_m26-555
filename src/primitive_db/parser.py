def parse_where_and_set(condition: str) -> dict | None:
    """
    Превращает строку условия в словарь

    :param condition: строка в виде "age = 25"
    :return: словарь в виде {"age": 25}
    """
    if not isinstance(condition, str):
        raise TypeError(f"condition must be str, but got {type(condition).__name__}")

    try:
        key, value = [x.strip() for x in condition.split("=", 1)]
    except ValueError:
        print(f"Некорректное значение: {condition}. Попробуйте снова.")
        return None

    if not value:
        print(f"Некорректное значение: {condition}. Попробуйте снова.")
        return None

    if value[0] == '"' and value[-1] == '"':
        value = value[1:-1]
    elif value == "True":
        value = True
    elif value == "False":
        value = False
    else:
        try:
            value = int(value)
        except ValueError:
            pass

    return {key: value}
