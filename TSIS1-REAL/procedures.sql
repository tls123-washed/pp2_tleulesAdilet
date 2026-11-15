-- Shared lookup. A unique first name works, or enter the full name.
CREATE OR REPLACE FUNCTION tsis1.find_contact_id(p_name text)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
    v_id integer;
    v_count bigint;
BEGIN
    SELECT min(c.id), count(*) INTO v_id, v_count
    FROM tsis1.contacts AS c
    WHERE lower(concat_ws(' ', c.first_name, c.last_name)) = lower(btrim(p_name));

    IF v_count = 0 THEN
        SELECT min(c.id), count(*) INTO v_id, v_count
        FROM tsis1.contacts AS c
        WHERE lower(c.first_name) = lower(btrim(p_name));
    END IF;

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact not found: %', p_name;
    ELSIF v_count > 1 THEN
        RAISE EXCEPTION 'Multiple contacts match %. Enter the full name.', p_name;
    END IF;
    RETURN v_id;
END;
$$;

CREATE OR REPLACE PROCEDURE tsis1.add_phone(
    p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id integer;
    v_phone text := btrim(p_phone);
    v_type text := lower(btrim(p_type));
BEGIN
    v_id := tsis1.find_contact_id(p_contact_name);
    IF v_phone IS NULL OR v_phone !~ '^[+]?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'A phone must have 10 to 15 digits, with an optional leading +';
    END IF;
    IF v_type IS NULL OR v_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile';
    END IF;
    INSERT INTO tsis1.phones(contact_id, phone, type) VALUES (v_id, v_phone, v_type);
END;
$$;

CREATE OR REPLACE PROCEDURE tsis1.move_to_group(
    p_contact_name VARCHAR, p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id integer;
    v_group_id integer;
    v_group_name text := btrim(p_group_name);
BEGIN
    v_contact_id := tsis1.find_contact_id(p_contact_name);
    IF v_group_name IS NULL OR char_length(v_group_name) NOT BETWEEN 1 AND 50 THEN
        RAISE EXCEPTION 'A group name must have 1 to 50 characters';
    END IF;

    INSERT INTO tsis1.groups AS g(name) VALUES (v_group_name)
    ON CONFLICT (lower(name)) DO UPDATE SET name = g.name
    RETURNING id INTO v_group_id;

    UPDATE tsis1.contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;

-- TSIS1 extends the Practice 8 search to email and the separate phones table.
CREATE OR REPLACE FUNCTION tsis1.search_contacts(p_query TEXT)
RETURNS SETOF tsis1.contact_details
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT d.*
    FROM tsis1.contact_details AS d
    WHERE strpos(lower(concat_ws(' ', d.first_name, d.last_name)), lower(p_query)) > 0
       OR strpos(lower(coalesce(d.email, '')), lower(p_query)) > 0
       OR EXISTS (
           SELECT 1 FROM tsis1.phones AS p
           WHERE p.contact_id = d.id AND strpos(p.phone, p_query) > 0
       )
    ORDER BY d.id;
END;
$$;
