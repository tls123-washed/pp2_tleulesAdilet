-- Task 2: Add a name or update the phone of an existing contact.
CREATE OR REPLACE PROCEDURE upsert_contact(p_name text, p_phone text)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id integer;
    v_matches integer;
BEGIN
    IF p_name IS NULL OR char_length(btrim(p_name)) NOT BETWEEN 1 AND 50 THEN
        RAISE EXCEPTION 'Name must contain 1 to 50 characters';
    END IF;
    IF p_phone IS NULL OR p_phone !~ '^[+]?[0-9]{10,15}$' THEN
        RAISE EXCEPTION 'Phone must contain 10 to 15 digits, with optional leading +';
    END IF;

    SELECT count(*), min(c.id)
    INTO v_matches, v_id
    FROM phonebook AS c
    WHERE lower(c.first_name) = lower(btrim(p_name));

    IF v_matches > 1 THEN
        RAISE EXCEPTION 'More than one contact has this name';
    ELSIF v_matches = 1 THEN
        UPDATE phonebook SET phone = p_phone WHERE id = v_id;
    ELSE
        INSERT INTO phonebook (first_name, phone)
        VALUES (btrim(p_name), p_phone);
    END IF;
END;
$$;

-- Task 3: Insert valid entries and return rejected entries with reasons.
-- Input: [{"first_name":"Aida","last_name":"Lee","phone":"87071234567"}]
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_contacts jsonb,
    INOUT rejected jsonb
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact jsonb;
    v_name text;
    v_surname text;
    v_phone text;
    v_reason text;
BEGIN
    IF jsonb_typeof(p_contacts) IS DISTINCT FROM 'array' THEN
        RAISE EXCEPTION 'Contacts must be a JSON array';
    END IF;

    rejected := '[]'::jsonb;

    FOR v_contact IN SELECT value FROM jsonb_array_elements(p_contacts)
    LOOP
        v_name := btrim(v_contact ->> 'first_name');
        v_surname := NULLIF(btrim(v_contact ->> 'last_name'), '');
        v_phone := btrim(v_contact ->> 'phone');
        v_reason := NULL;

        IF v_name IS NULL OR char_length(v_name) NOT BETWEEN 1 AND 50 THEN
            v_reason := 'Name must contain 1 to 50 characters';
        ELSIF char_length(v_surname) > 50 THEN
            v_reason := 'Surname must contain at most 50 characters';
        ELSIF v_phone IS NULL OR v_phone !~ '^[+]?[0-9]{10,15}$' THEN
            v_reason := 'Invalid phone format';
        ELSE
            INSERT INTO phonebook (first_name, last_name, phone)
            VALUES (v_name, v_surname, v_phone)
            ON CONFLICT (phone) DO NOTHING;

            IF NOT FOUND THEN
                v_reason := 'Phone already exists';
            END IF;
        END IF;

        IF v_reason IS NOT NULL THEN
            rejected := rejected || jsonb_build_array(
                jsonb_build_object('contact', v_contact, 'reason', v_reason)
            );
        END IF;
    END LOOP;
END;
$$;

-- Task 5: Delete by one criterion. NULL means it was not selected.
CREATE OR REPLACE PROCEDURE delete_contacts(
    IN p_name text,
    IN p_phone text,
    INOUT deleted_count integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF (p_name IS NULL) = (p_phone IS NULL) THEN
        RAISE EXCEPTION 'Specify either a name or a phone';
    END IF;

    IF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    ELSE
        DELETE FROM phonebook WHERE lower(first_name) = lower(btrim(p_name));
    END IF;

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
END;
$$;
