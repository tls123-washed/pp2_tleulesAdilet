"""Practice 8 console phonebook."""

import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import Json

from connect import get_connection


def initialize_database(conn):
    folder = Path(__file__).resolve().parent
    with conn:
        with conn.cursor() as cur:
            for filename in ("functions.sql", "procedures.sql"):
                sql = (folder / filename).read_text(encoding="utf-8")
                cur.execute(sql)
    print("Table, functions and procedures are ready.")


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for contact_id, first_name, last_name, phone in rows:
        print(f"{contact_id}: {first_name} {last_name or ''} | {phone}")


def search_contacts(cur):
    pattern = input("Part of name, surname or phone: ").strip()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    print_contacts(cur.fetchall())


def upsert_contact(cur):
    name = input("First name: ").strip()
    phone = input("Phone: ").strip()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    return "Contact saved."


def insert_many_contacts(cur):
    count = int(input("How many contacts? "))
    if count < 1:
        raise ValueError("Enter a positive number of contacts.")

    contacts = []
    for index in range(count):
        print(f"Contact {index + 1}:")
        contacts.append({
            "first_name": input("First name: ").strip(),
            "last_name": input("Last name (optional): ").strip(),
            "phone": input("Phone: ").strip(),
        })

    cur.execute("CALL insert_many_contacts(%s::jsonb, '[]'::jsonb)", (Json(contacts),))
    rejected = cur.fetchone()[0]
    message = f"Inserted: {count - len(rejected)}. Rejected: {len(rejected)}."
    for item in rejected:
        contact = item["contact"]
        message += f"\n- {contact['first_name']} ({contact['phone']}): {item['reason']}"
    return message


def show_page(cur):
    page = int(input("Page number (starts at 1): "))
    limit = int(input("Contacts per page: "))
    if page < 1 or limit < 1:
        raise ValueError("Page number and page size must be positive.")

    offset = (page - 1) * limit
    cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
    print_contacts(cur.fetchall())


def delete_contacts(cur):
    mode = input("Delete by 1 - name (all exact matches), 2 - phone: ").strip()
    if mode == "1":
        name = input("First name: ").strip()
        phone = None
    elif mode == "2":
        name = None
        phone = input("Exact phone: ").strip()
    else:
        raise ValueError("Choose 1 or 2.")

    if name == "" or phone == "":
        raise ValueError("Enter a value to delete.")

    cur.execute("CALL delete_contacts(%s, %s, 0)", (name, phone))
    deleted_count = cur.fetchone()[0]
    return f"Deleted: {deleted_count}."


def run_menu(conn):
    actions = {
        "1": search_contacts,
        "2": upsert_contact,
        "3": insert_many_contacts,
        "4": show_page,
        "5": delete_contacts,
    }

    while True:
        print("\n1. Search\n2. Add or update\n3. Add many\n4. Show page\n5. Delete\n0. Exit")
        choice = input("Choice: ").strip()
        if choice == "0":
            break
        if choice not in actions:
            print("Unknown choice.")
            continue

        try:
            # Commit if the block succeeds; roll back if it raises an error.
            with conn:
                with conn.cursor() as cur:
                    message = actions[choice](cur)
            if message is not None:
                print(message)
        except (ValueError, psycopg2.Error) as error:
            print(f"Could not complete the operation: {error}")


def main():
    try:
        conn = get_connection()
    except psycopg2.Error as error:
        print(f"Connection failed: {error}")
        return 1

    try:
        if sys.argv[1:] == ["--init"]:
            initialize_database(conn)
        else:
            run_menu(conn)
    except (OSError, psycopg2.Error) as error:
        print(f"Error: {error}")
        return 1
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
