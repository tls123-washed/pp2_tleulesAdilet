def load_config():
    """Returns a dictionary with database connection parameters."""
    return {
        "host": "localhost",
        "database": "postgres", # Или имя твоей БД, если создавал отдельную
        "user": "postgres",
        "password": "твой_пароль_от_pgadmin" 
    }