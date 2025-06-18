-- Run these as the 'postgres' user
CREATE DATABASE apidata;
CREATE USER trino WITH PASSWORD 'trino';
GRANT ALL PRIVILEGES ON DATABASE apidata TO trino;

\c apidata
ALTER SCHEMA public OWNER TO trino;
GRANT ALL ON SCHEMA public TO trino;
