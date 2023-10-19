PORT ?= 8000

build: install
	psql -a -d $(DATABASE_URL) -f database.sql

dev:
	poetry run python manage.py runserver

install:
	poetry install || true

lint:
	poetry run flake8 task_manager

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi