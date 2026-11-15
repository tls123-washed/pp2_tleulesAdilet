"""TSIS1: extended console phonebook."""

import csv
import json
import sys
from datetime import date
from pathlib import Path

import psycopg2

from connect import get_connection


FOLDER = Path(__file__).resolve().parent
SORT_COLUMNS = {"1": "first_name, last_name", "2": "birthday", "3": "created_at"}
PAGE_SIZE = 5


def initialize_database(conn):
    with conn:
        with conn.cursor() as cur:
            for filename in ("schema.sql", "practice8_pagination.sql", "procedures.sql"):
                cur.execute((FOLDER / filename).read_text(encoding="utf-8"))
    print("TSIS1 schema, functions, and procedures are ready.")


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return
    for contact_id, first, last, email, birthday, group, created, phones in rows:
        numbers = ", ".join(f"{p['type']}: {p['phone']}" for p in phones) or "—"
        name = " ".join(part for part in (first, last) if part)
        print(f"{contact_id}: {name} | {email or '—'} | {birthday or '—'}"
              f" | {group} | added {created.date()} | {numbers}")


def search_contacts(cur):
    query = input("Part of name, surname, email or phone: ").strip()
    cur.execute("SELECT * FROM tsis1.search_contacts(%s) ORDER BY id", (query,))
    print_contacts(cur.fetchall())


def filter_and_sort(cur):
    group = input("Group (Enter for all): ").strip()
    email = input("Email contains (Enter for all): ").strip()
    choice = input("Sort: 1 name, 2 birthday, 3 date added [1]: ").strip() or "1"
    if choice not in SORT_COLUMNS:
        raise ValueError("Choose 1, 2, or 3.")
    # The column list comes from our dictionary, so users cannot inject SQL.
    order = SORT_COLUMNS[choice]
    cur.execute(
        f"""
        SELECT * FROM tsis1.contact_details
        WHERE (%s = '' OR lower(contact_group) = lower(%s))
          AND (%s = '' OR strpos(lower(coalesce(email, '')), lower(%s)) > 0)
        ORDER BY {order}, id
        """,
        (group, group, email, email),
    )
    print_contacts(cur.fetchall())


def read_page(cur, page):
    offset = (page - 1) * PAGE_SIZE
    cur.execute(
        """
        SELECT d.*
        FROM tsis1.get_contacts_page(%s, %s) AS page
        JOIN tsis1.contact_details AS d ON d.id = page.id
        ORDER BY d.id
        """,
        (PAGE_SIZE, offset),
    )
    return cur.fetchall()


def browse_pages(cur):
    page = 1
    rows = read_page(cur, page)
    while True:
        print(f"Page {page}")
        print_contacts(rows)
        command = input("next / prev / quit: ").strip().lower()
        if command == "quit":
            return
        if command == "next":
            next_rows = read_page(cur, page + 1)
            if next_rows:
                page += 1
                rows = next_rows
            else:
                print("No next page.")
        elif command == "prev":
            if page > 1:
                page -= 1
                rows = read_page(cur, page)
            else:
                print("Already on the first page.")
        else:
            print("Use next, prev, or quit.")


def add_phone(cur):
    name = input("Contact name (first or full): ").strip()
    phone = input("Phone: ").strip()
    kind = input("Type (home, work, mobile): ").strip()
    cur.execute("CALL tsis1.add_phone(%s, %s, %s)", (name, phone, kind))
    return "Phone added."


def move_to_group(cur):
    name = input("Contact name (first or full): ").strip()
    group = input("New group: ").strip()
    cur.execute("CALL tsis1.move_to_group(%s, %s)", (name, group))
    return "Contact moved."


def choose_path(prompt, default):
    value = input(f"{prompt} [default: {default.name}]: ").strip().strip('"')
    return Path(value).expanduser() if value else default


def export_json(cur):
    path = choose_path("JSON export path", FOLDER / "export.json")
    cur.execute("""
        SELECT first_name, last_name, email, birthday, contact_group, phones
        FROM tsis1.contact_details
        ORDER BY id
    """)
    records = [
        {
            "first_name": first, "last_name": last, "email": email,
            "birthday": birthday.isoformat() if birthday else None,
            "group": group, "phones": phones,
        }
        for first, last, email, birthday, group, phones in cur.fetchall()
    ]
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    return f"Exported {len(records)} contacts to {path.resolve()}."


def clean_text(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("Name, dates, email and phones must be text.")
    return value.strip()


def normalize_contact(record):
    if not isinstance(record, dict):
        raise ValueError("Each contact must be an object.")
    first = clean_text(record.get("first_name"))
    if not first:
        raise ValueError("First name is required.")
    phones = record.get("phones", [])
    if not isinstance(phones, list) or any(not isinstance(p, dict) for p in phones):
        raise ValueError(f"{first}: phones must be a list of objects.")
    birthday = clean_text(record.get("birthday"))
    return {
        "first_name": first,
        "last_name": clean_text(record.get("last_name")) or None,
        "email": clean_text(record.get("email")) or None,
        "birthday": date.fromisoformat(birthday) if birthday else None,
        "group": clean_text(record.get("group")) or None,
        "phones": [
            (clean_text(p.get("phone")), clean_text(p.get("type")).lower() or "mobile")
            for p in phones
        ],
    }


def find_duplicate(cur, first, last):
    cur.execute("""
        SELECT id FROM tsis1.contacts
        WHERE lower(first_name) = lower(%s)
          AND lower(coalesce(last_name, '')) = lower(coalesce(%s, ''))
    """, (first, last))
    row = cur.fetchone()
    return row[0] if row else None


def save_imported_contact(cur, record, contact_id, overwrite):
    group = record["group"]
    group_id = None
    if group is not None or contact_id is None or overwrite:
        cur.execute("""
            INSERT INTO tsis1.groups AS g(name) VALUES (%s)
            ON CONFLICT (lower(name)) DO UPDATE SET name = g.name
            RETURNING id
        """, (group or "Other",))
        group_id = cur.fetchone()[0]

    email, birthday = record["email"], record["birthday"]
    if contact_id is None:
        cur.execute("""
            INSERT INTO tsis1.contacts (first_name, last_name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (record["first_name"], record["last_name"], email, birthday, group_id))
        contact_id = cur.fetchone()[0]
    elif overwrite:
        cur.execute("""
            UPDATE tsis1.contacts SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s
        """, (email, birthday, group_id, contact_id))
        cur.execute("DELETE FROM tsis1.phones WHERE contact_id = %s", (contact_id,))
    else:
        # CSV can supply another phone while leaving personal fields blank.
        cur.execute("""
            UPDATE tsis1.contacts
            SET email = coalesce(%s, email), birthday = coalesce(%s, birthday),
                group_id = coalesce(%s, group_id)
            WHERE id = %s
        """, (email, birthday, group_id, contact_id))

    cur.executemany("""
        INSERT INTO tsis1.phones (contact_id, phone, type) VALUES (%s, %s, %s)
        ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type
    """, [(contact_id, phone, kind) for phone, kind in record["phones"]])


def import_json(cur):
    path = choose_path("JSON import path", FOLDER / "export.json")
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, list):
        raise ValueError("JSON must contain a list of contacts.")
    records = [normalize_contact(record) for record in raw]
    saved = skipped = 0

    for record in records:
        first, last = record["first_name"], record["last_name"]
        contact_id = find_duplicate(cur, first, last)
        if contact_id is not None:
            name = " ".join(part for part in (first, last) if part)
            while True:
                choice = input(f"{name} exists: skip or overwrite? ").strip().lower()
                if choice in {"skip", "overwrite"}:
                    break
                print("Type skip or overwrite.")
            if choice == "skip":
                skipped += 1
                continue
        save_imported_contact(cur, record, contact_id, overwrite=True)
        saved += 1
    return f"JSON import: saved {saved}, skipped {skipped}."


def import_csv(cur):
    path = choose_path("CSV import path", FOLDER / "contacts.csv")
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not {"first_name", "phone"} <= set(reader.fieldnames or []):
            raise ValueError("CSV needs first_name and phone column headers.")
        count = 0
        for row in reader:
            row["phones"] = [{"phone": row["phone"], "type": row.get("phone_type")}]
            record = normalize_contact(row)
            contact_id = find_duplicate(cur, record["first_name"], record["last_name"])
            save_imported_contact(cur, record, contact_id, overwrite=False)
            count += 1
    return f"CSV import: processed {count} rows."


def run_menu(conn):
    actions = {
        "1": search_contacts, "2": filter_and_sort, "3": browse_pages,
        "4": add_phone, "5": move_to_group, "6": export_json,
        "7": import_json, "8": import_csv,
    }
    while True:
        print("\n1. Search all fields\n2. Filter and sort\n3. Browse pages"
              "\n4. Add phone\n5. Move to group\n6. Export JSON"
              "\n7. Import JSON\n8. Import CSV\n0. Exit")
        choice = input("Choice: ").strip()
        if choice == "0":
            return
        action = actions.get(choice)
        if action is None:
            print("Unknown choice.")
            continue
        try:
            with conn:
                with conn.cursor() as cur:
                    message = action(cur)
            if message:
                print(message)
        except (ValueError, OSError, psycopg2.Error) as error:
            print(f"Could not complete the operation: {error}")


def main():
    if sys.argv[1:] not in ([], ["--init"]):
        print("Usage: python phonebook.py [--init]")
        return 1
    try:
        conn = get_connection()
        try:
            if sys.argv[1:]:
                initialize_database(conn)
            else:
                run_menu(conn)
        finally:
            conn.close()
    except (OSError, psycopg2.Error) as error:
        print(f"Error: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
