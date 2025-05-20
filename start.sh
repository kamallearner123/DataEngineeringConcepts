#!/bin/zsh

# Configuration
SERVER_IP="0.0.0.0"
SERVER_PORT="8000"


# This script is used to start the Data Engineering project.
# It sets up the environment and runs the main script.
# Usage: ./start.sh

python3 manage.py makemigrations
python manage.py collectstatic
python3 manage.py migrate
python3 manage.py runserver ${SERVER_IP}:${SERVER_PORT}
