.PHONY: help up down logs build shell test migrate makemigrations createsuperuser backup-db restore-db

help:
	@echo "Comandos disponibles:"
	@echo "  make up              Levantar servicios"
	@echo "  make down            Detener servicios"
	@echo "  make logs            Ver logs"
	@echo "  make build           Construir imagenes"
	@echo "  make shell           Shell backend"
	@echo "  make test            Ejecutar pruebas"
	@echo "  make migrate         Ejecutar migraciones"
	@echo "  make makemigrations  Crear migraciones"
	@echo "  make createsuperuser Crear superusuario"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

shell:
	docker compose exec backend bash

test:
	docker compose exec backend python manage.py test

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

backup-db:
	bash infrastructure/scripts/backup_db.sh

restore-db:
	bash infrastructure/scripts/restore_db.sh
