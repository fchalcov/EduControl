#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")"

export DJANGO_SETTINGS_MODULE=config.settings

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
