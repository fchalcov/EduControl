#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")"

export DJANGO_SETTINGS_MODULE=config.settings

chmod +x start.sh

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
