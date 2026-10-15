## Управление таблицами

### Запуск:

```
database
```

### Команды:

| Команды                                | Что делает             |
|----------------------------------------|------------------------|
| `create_table <имя> <столбец:тип> ...` | создать таблицу        |
| `list_tables`                          | показать список таблиц |
| `drop_table <имя>`                     | удалить таблицу        |
| `help`                                 | справка                |
| `exit`                                 | выход                  |

### Демонстрация

[![asciicast](https://asciinema.org/a/AOqFDUsGQ7ysPznO.svg)](https://asciinema.org/a/AOqFDUsGQ7ysPznO)

Типы столбцов: `int`, `str`, `bool`. 

Столбец `ID:int` добавляется автоматически.

### Пример:

```
>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
>>>Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.
>>>Введите команду: list_tables
- users
>>>Введите команду: drop_table users
Таблица "users" успешно удалена.
>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.
>>>Введите команду: exit
```