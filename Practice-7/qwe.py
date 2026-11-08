import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PP2",
    user="postgres",
    password="Shinobi890"
)

cursor = connection.cursor()

def search():
    number = input()
    cursor.execute(f"SELECT phone_number FROM PP2 IF {number} = phone_number")
    cursor.close()
    connection.close()

    