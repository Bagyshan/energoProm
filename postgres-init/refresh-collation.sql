DO
$$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT datname FROM pg_database WHERE datallowconn LOOP
        EXECUTE format('ALTER DATABASE %I REFRESH COLLATION VERSION;', r.datname);
    END LOOP;
END;
$$;