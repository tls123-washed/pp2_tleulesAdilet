import psycopg2
from config import load_config

def get_connection():
    """Connect to the PostgreSQL database server"""
    try:
        config = load_config()
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**config)
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Connection error: {error}")
        return None