import csv
from connect import get_connection

def create_tables():
    """Создает таблицу phonebook"""
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone VARCHAR(20) UNIQUE NOT NULL
    );
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully.")

def insert_contact(first_name, last_name, phone):
    """Вставляет один контакт (Create)"""
    sql = "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s);"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (first_name, last_name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Contact {first_name} added.")

def insert_from_csv(filename):
    """Вставляет много контактов из CSV (Batch Insert)"""
    sql = "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT (phone) DO NOTHING;"
    
    # Читаем данные из файла
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Пропускаем заголовок
        data = [row for row in reader]

    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(sql, data) # executemany для вставки списка списков
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted.")

def get_contacts_by_name(first_name):
    """Ищет контакты по имени (Read)"""
    sql = "SELECT * FROM phonebook WHERE first_name = %s;"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (first_name,))
    
    rows = cur.fetchall() # Забираем все найденные строки
    print(f"--- Contacts with name {first_name} ---")
    for row in rows:
        print(row)
        
    cur.close()
    conn.close()

def update_phone(first_name, new_phone):
    """Обновляет номер телефона по имени (Update)"""
    sql = "UPDATE phonebook SET phone = %s WHERE first_name = %s;"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (new_phone, first_name))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Phone updated for {first_name}.")

def delete_contact(first_name):
    """Удаляет контакт по имени (Delete)"""
    sql = "DELETE FROM phonebook WHERE first_name = %s;"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (first_name,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Contact {first_name} deleted.")

if __name__ == '__main__':
    # 1. Создаем таблицу
    create_tables()
    
    # 2. Загружаем данные из CSV
    insert_from_csv('contacts.csv')
    
    # 3. Добавляем данные "из консоли" (имитация ввода)
    insert_contact('TestUser', 'TestSurname', '87770001122')
    
    # 4. Обновляем телефон (изменили номер у Адилета из CSV)
    update_phone('Adilet', '87000000000')
    
    # 5. Ищем контакты с именем Adilet
    get_contacts_by_name('Adilet')
    
    # 6. Удаляем тестовый контакт
    delete_contact('TestUser')