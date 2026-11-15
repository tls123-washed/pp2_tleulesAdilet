-- Practice 8 function reused unchanged, with its own schema/search path.
SET search_path TO tsis1, public;

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

ALTER FUNCTION tsis1.get_contacts_page(integer, integer)
    SET search_path TO tsis1, pg_catalog;

RESET search_path;
