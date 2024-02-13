APP ?=
PORT ?= 8000
MANAGE = poetry run python manage.py

build: install migrate
	poetry run python manage.py collectstatic --no-input
	poetry run python manage.py createsu

dev:
	$(MANAGE) runserver

install:
	poetry install || true

lint:
	poetry run flake8 task_manager

makemigrations:
	$(MANAGE) makemigrations

migrate: makemigrations
	$(MANAGE) migrate

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

test:
	$(MANAGE) test task_manager$(APP)

translate:
	cd $(CURDIR)/task_manager && \
	poetry run django-admin makemessages --locale ru_RU --ignore=-_-* && \
	vim $(CURDIR)/task_manager/locale/ru_RU/LC_MESSAGES/django.po && \
	poetry run django-admin compilemessages

testcoverage:
	poetry run coverage run manage.py test && \
	poetry run coverage xml 

.PHONY: test
