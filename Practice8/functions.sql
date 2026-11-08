-- Create the Practice 7 table if starting with an empty database.
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    phone VARCHAR(20) UNIQUE NOT NULL
);

-- Task 1: Search by part of a first name, last name, or phone.
CREATE OR REPLACE FUNCTION search_contacts(p_pattern text)
RETURNS SETOF phonebook
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.*
    FROM phonebook AS c
    WHERE strpos(lower(c.first_name), lower(p_pattern)) > 0
       OR strpos(lower(c.last_name),  lower(p_pattern)) > 0
       OR strpos(c.phone, p_pattern) > 0
    ORDER BY c.id;
END;
$$;

-- Task 4: Return up to p_limit rows after skipping p_offset rows.
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit integer, p_offset integer)
RETURNS SETOF phonebook
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_limit IS NULL OR p_limit <= 0 OR p_offset IS NULL OR p_offset < 0 THEN
        RAISE EXCEPTION 'Limit must be positive and offset must be non-negative';
    END IF;

    RETURN QUERY
    SELECT c.*
    FROM phonebook AS c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;
