-- Use a separate schema in the same database as Practice 8.
CREATE SCHEMA IF NOT EXISTS tsis1;

CREATE TABLE IF NOT EXISTS tsis1.groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL CHECK (btrim(name) <> '')
);

CREATE UNIQUE INDEX IF NOT EXISTS groups_name_key
    ON tsis1.groups (lower(name));

INSERT INTO tsis1.groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (lower(name)) DO NOTHING;

CREATE TABLE IF NOT EXISTS tsis1.contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL CHECK (btrim(first_name) <> ''),
    last_name VARCHAR(50),
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER NOT NULL REFERENCES tsis1.groups(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Full name, ignoring case, is the duplicate rule for imports.
CREATE UNIQUE INDEX IF NOT EXISTS contacts_full_name_key
    ON tsis1.contacts (lower(first_name), lower(COALESCE(last_name, '')));

CREATE TABLE IF NOT EXISTS tsis1.phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES tsis1.contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL CHECK (phone ~ '^[+]?[0-9]{10,15}$'),
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);

-- Compatibility view for the unchanged Practice 8 pagination function.
-- It still reads one row per contact with the original four columns.
CREATE OR REPLACE VIEW tsis1.phonebook AS
SELECT c.id, c.first_name, c.last_name, p.phone
FROM tsis1.contacts AS c
LEFT JOIN LATERAL (
    SELECT n.phone FROM tsis1.phones AS n
    WHERE n.contact_id = c.id
    ORDER BY n.id
    LIMIT 1
) AS p ON true;

-- Common read view for display and JSON export. Keep one row per contact.
CREATE OR REPLACE VIEW tsis1.contact_details AS
SELECT c.id, c.first_name, c.last_name, c.email, c.birthday,
       g.name AS contact_group, c.created_at,
       COALESCE((
           SELECT jsonb_agg(jsonb_build_object('phone', p.phone, 'type', p.type)
                            ORDER BY p.id)
           FROM tsis1.phones AS p
           WHERE p.contact_id = c.id
       ), '[]'::jsonb) AS phones
FROM tsis1.contacts AS c
JOIN tsis1.groups AS g ON g.id = c.group_id;
