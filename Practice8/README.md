# Practice 8 — PostgreSQL PhoneBook

Console phonebook built with Python, Psycopg2, and PostgreSQL. The application calls PostgreSQL functions and stored procedures for the five tasks in Practice 8.

```text
Practice8/
├── phonebook.py
├── functions.sql
├── procedures.sql
├── config.py
├── connect.py
└── README.md
```

| File | Purpose |
| --- | --- |
| `config.py` | Reads connection settings and asks for the PostgreSQL password. |
| `connect.py` | Passes those settings to `psycopg2.connect()`. |
| `functions.sql` | Creates the table if needed; defines search and pagination. |
| `procedures.sql` | Defines add/update, bulk insert with validation, and deletion. |
| `phonebook.py` | Reads input, calls SQL routines, and displays results. |

## Запуск с нуля

1. Запусти PostgreSQL. В pgAdmin создай пустую базу `phonebook_db`: правой кнопкой на **Databases → Create → Database**. Старая Practice 7 для запуска не нужна. Если хочешь подключить существующую базу, в ней должна быть совместимая таблица `phonebook(id, first_name, last_name, phone)` с уникальным телефоном.
2. В терминале VS Code открой папку `Practice8` и выполни:

   ```powershell
   python -m pip install psycopg2-binary
   python phonebook.py --init
   python phonebook.py
   ```

   Если Windows находит Python по команде `py`, используй её вместо `python` во всех трёх командах.

3. Вводи пароль **пользователя PostgreSQL**. Символы пароля в терминале не отображаются. По умолчанию используются `localhost`, порт `5432`, база `phonebook_db` и пользователь `postgres`. Если параметры другие, задай нужные переменные в PowerShell перед запуском:

   ```powershell
   $env:PGHOST = "localhost"
   $env:PGPORT = "5432"
   $env:PGDATABASE = "phonebook_db"
   $env:PGUSER = "postgres"
   ```

`--init` выполняет оба SQL-файла по порядку. Вместо этой команды можно выполнить их в pgAdmin в нужной базе: сначала `functions.sql`, потом `procedures.sql`. Скрипты не удаляют существующие контакты. Пароль в проекте не хранится.

## Что показать на защите

| Пункт | Что сделать в меню | Что ожидается |
| --- | --- | --- |
| 2 — Add or update | Добавь `Aida` с `87071234567`, затем снова введи `Aida` с `87071234568`. | Та же запись получает новый номер. |
| 3 — Add many | Введи 2 контакта: `Mira Lee`, `87021234567` и `Tim Kay`, `123`. | Mira сохранится, Tim появится в списке отклонённых с причиной. |
| 1 — Search | Введи `lee` или `2345`. | Поиск по части фамилии или телефона. |
| 4 — Show page | Введи страницу `1`, размер `1`; повтори со страницей `2`. | По одному контакту, в порядке ID. |
| 5 — Delete | Выбери удаление по телефону и введи `87071234568`. | Программа покажет число удалённых строк. |

Телефон проходит проверку, если содержит 10–15 цифр и может начинаться с `+`. При массовой вставке номер, который уже есть в таблице, тоже попадает в отчёт. При обновлении имя сравнивается без учёта регистра. Если у двух контактов одинаковое имя, процедура сообщит об этом и не будет выбирать случайный контакт. При удалении по имени удаляются все точные совпадения; для одного контакта используй его уникальный телефон.

## Practice 7: что повторить перед Practice 8

Начни с одного запроса. После запуска `--init` создай временный учебный файл вне папки для сдачи или попробуй этот фрагмент из папки `Practice8`:

```python
from connect import get_connection

name = input("Имя: ")
conn = get_connection()
try:
    cur = conn.cursor()
    cur.execute(
        "SELECT first_name, phone FROM phonebook WHERE first_name = %s",
        (name,)
    )
    for row in cur.fetchall():
        print(row)
    cur.close()
finally:
    conn.close()
```

1. `get_connection()` возвращает подключение. `conn.cursor()` создаёт курсор — через него Python отправляет запрос.
2. `execute(запрос, параметры)` выполняет SQL. `%s` — место для значения, а `(name,)` — кортеж из одного значения. Запятая обязательна для такого кортежа.
3. `fetchall()` возвращает найденные строки. Для `INSERT`, `UPDATE` и `DELETE` без `RETURNING` строки не читают: после изменения нужен `commit()`. `rollback()` отменяет неподтверждённые изменения.
4. Для CSV используется `with open(...)`, `csv.reader()`, пропуск заголовка через `next(reader, None)` и вставка всех строк через `executemany()`.
5. Для Practice 8 замени обычный запрос на `SELECT * FROM search_contacts(%s)`. Python по-прежнему получает ввод и выводит результат. Условие поиска теперь хранится в `functions.sql`.

Мини-упражнение: сначала найди контакт по точному имени в примере, затем замени фильтр на `WHERE phone = %s` и передай введённый телефон. Когда оба запроса работают, переходи к функциям Practice 8.

## Что нового в Practice 8

- **Функция** поиска или пагинации вызывается через `SELECT`. `RETURN QUERY` возвращает строки; Python получает их через `fetchall()`.
- **Процедура** вызывается через `CALL`. Для массовой вставки Python собирает список словарей, а `Json(contacts)` передаёт его в PostgreSQL как JSON. Внутри процедуры `FOR` проходит по списку, а `IF` проверяет каждый контакт. Параметр `INOUT rejected` возвращает одну строку с JSON-списком отклонённых контактов; Python читает её через `fetchone()[0]`.
- **Пагинация**: `LIMIT` задаёт размер страницы, `OFFSET = (номер страницы − 1) × размер страницы` — сколько строк пропустить. `ORDER BY id` задаёт порядок.
- **Транзакции**: `with conn:` подтверждает транзакцию при успехе и откатывает её при исключении. Курсор закрывается при выходе из `with conn.cursor()`. Само соединение закрывается через `conn.close()`.

## Загрузка на GitHub

Распакуй архив и положи папку `Practice8` в корень своего репозитория. Из корня репозитория:

```bash
git add Practice8/README.md Practice8/config.py Practice8/connect.py Practice8/phonebook.py Practice8/functions.sql Practice8/procedures.sql
git commit -m "Add Practice 8 PostgreSQL phonebook"
git push origin main
```
