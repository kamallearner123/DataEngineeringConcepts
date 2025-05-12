#!/bin/zsh

# Configuration
SERVER_IP="0.0.0.0"
SERVER_PORT="8000"

# Postgres Configuration
# Start Postgres
# hceck this is MAC or Linux
if [ "$(uname)" = "Darwin" ]; then
    brew services start postgresql
else
    sudo service postgresql start
fi

# Create a new database
DB_NAME="data_engineering_db"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT="5432"
DB_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
export DATABASE_URL=$DB_URL
# Create the database if it doesn't exist
if ! psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    createdb $DB_NAME
fi



# This script is used to start the Data Engineering project.
# It sets up the environment and runs the main script.
# Usage: ./start.sh

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver ${SERVER_IP}:${SERVER_PORT}
