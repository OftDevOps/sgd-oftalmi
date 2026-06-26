.PHONY: help up down logs build shell check test test-base migrate makemigrations showmigrations createsuperuser backup-db restore-db backup-media healthcheck deploy

help:
	@echo "Comandos disponibles:"
	@echo "  make up              Levantar servicios"
	@echo "  make down            Detener servicios"
	@echo "  make logs            Ver logs"
	@echo "  make build           Construir imagenes"
	@echo "  make shell           Shell backend"
	@echo "  make check           Ejecutar manage.py check"
	@echo "  make test            Ejecutar pruebas"
	@echo "  make test-base       Ejecutar pruebas de modulos base"
	@echo "  make migrate         Ejecutar migraciones"
	@echo "  make makemigrations  Crear migraciones"
	@echo "  make showmigrations  Ver migraciones"
	@echo "  make createsuperuser Crear superusuario"
	@echo "  make backup-db       Crear respaldo de PostgreSQL"
	@echo "  make restore-db      Restaurar respaldo DB=archivo.sql"
	@echo "  make backup-media    Crear respaldo de storage/media"
	@echo "  make healthcheck     Validar endpoint /health/"
	@echo "  make deploy          Flujo local: build, up, migrate, check"

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

check:
	docker compose exec backend python manage.py check

test:
	docker compose exec backend python manage.py test

test-base:
	docker compose exec backend python manage.py test apps.accounts apps.organizational_units apps.document_types apps.documents apps.document_requests apps.controlled_copies apps.implementation_records apps.audit --settings=config.settings.test

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

showmigrations:
	docker compose exec backend python manage.py showmigrations

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

backup-db:
	bash infrastructure/scripts/backup_db.sh

restore-db:
	bash infrastructure/scripts/restore_db.sh $(DB)

backup-media:
	bash infrastructure/scripts/backup_media.sh

healthcheck:
	bash infrastructure/scripts/healthcheck.sh

deploy:
	bash infrastructure/scripts/deploy.sh
