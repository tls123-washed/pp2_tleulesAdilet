"""Read PostgreSQL settings without storing a password in the project."""

import os
from getpass import getpass


def load_config():
    password = os.getenv("PGPASSWORD")
    if password is None:
        password = getpass("PostgreSQL password: ")

    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": os.getenv("PGPORT", "5432"),
        "dbname": os.getenv("PGDATABASE", "phonebook_db"),
        "user": os.getenv("PGUSER", "postgres"),
        "password": password,
    }
