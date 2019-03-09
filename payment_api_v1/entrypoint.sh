#!/bin/bash

set -e

# create DB if not exists
psql -h $POSTGRES_PORT_5432_TCP_ADDR -U $PGPASSWORD -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB_NAME'" | \
grep -q 1 || psql -h $POSTGRES_PORT_5432_TCP_ADDR -U $PGPASSWORD -c "CREATE DATABASE $POSTGRES_DB_NAME"

exec "$@"