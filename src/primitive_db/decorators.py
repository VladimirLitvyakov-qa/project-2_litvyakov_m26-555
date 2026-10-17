import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def handle_db_errors(func: Callable) -> Callable:
    """
    Перехватывает ошибки БД и выводит сообщение

    :param func: функция
    :return: обёрнутая функция
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name: str) -> Callable:
    """
    Запрашивает подтверждение перед выполнением функции

    :param action_name: название действия для вопроса
    :return: декоратор
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if answer == "y":
                return func(*args, **kwargs)
            print("Операция отменена")
            return None

        return wrapper

    return decorator


def log_time(func: Callable) -> Callable:
    """
    Замеряет время выполнения функции

    :param func: функция
    :return: обёрнутая функция
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        elapsed = end - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper


def create_cacher() -> Callable:
    """
    Создает кэш

    :return: функцию cache_result
    """

    cache = {}

    def cache_result(key: Any, value_func: Callable) -> Any:
        """
        Возвращает значение из кэша или вычисляет и сохраняет его

        :param key: ключ
        :param value_func: функция, которая вычисляет результат
        :return: значение из кэша или результат value_func
        """
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result

        return result

    return cache_result
