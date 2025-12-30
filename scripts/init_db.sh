#!/usr/bin/env bash
set -e

DB_NAME="canteen_db"
DB_OWNER="canteen_owner"
DB_OWNER_PASSWORD="canteen_owner_pass"


docker exec -i canteen_db psql -U postgres <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '${DB_OWNER}') THEN
    CREATE ROLE ${DB_OWNER} LOGIN PASSWORD '${DB_OWNER_PASSWORD}';
  END IF;
END
\$\$;

SELECT 'CREATE DATABASE ${DB_NAME} OWNER ${DB_OWNER}'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DB_NAME}')\\gexec

\\c ${DB_NAME}
CREATE EXTENSION IF NOT EXISTS pg_trgm;

ALTER DATABASE ${DB_NAME} OWNER TO ${DB_OWNER};
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_OWNER};
SQL

echo "OK: database '${DB_NAME}' created/verified. Owner: '${DB_OWNER}'. Extension pg_trgm enabled."
