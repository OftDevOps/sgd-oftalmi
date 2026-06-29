# SGD-OFTALMI

Sistema de Gestion Documental para Laboratorios Oftalmi.

## Alcance inicial

El MVP esta orientado a la Gestion Documental administrada por el Departamento de Organizacion y Metodos.

El Departamento de Calidad queda fuera del alcance funcional inicial, salvo como unidad usuaria o consultora cuando aplique.

## Bloques principales

- Backend Django
- Frontend React o interfaz definida para el MVP
- PostgreSQL
- Docker / Docker Compose
- Nginx
- Documentacion funcional y tecnica
- Auditoria y reportes

## Estado tecnico del backend base

La rama `develop` contiene la base Django del MVP con:

- Usuario personalizado por correo institucional.
- Roles base de usuario y grupos Django iniciales.
- Catalogos base de unidades ejecutoras y tipos documentales.
- Modelos base de documentos, versiones, archivos y secuencias de codigo.
- Solicitudes documentales base.
- Copias controladas base.
- Registros de implementacion base.
- Auditoria base.

La rama `main` se mantiene como version estable aprobada. El trabajo activo se realiza en `develop`.

## Ejecucion local con Docker

Crear un archivo `.env` a partir de `.env.example` y levantar servicios:

```bash
make up
```

Comandos utiles:

```bash
make check
make migrate
make test-base
make healthcheck
```

Ejecutar carga inicial controlada de catalogos base:

```bash
make seed-base-catalogs
```

Crear superusuario usando correo institucional:

```bash
make createsuperuser
```

## Operacion local basica

Respaldar PostgreSQL:

```bash
make backup-db
```

Restaurar PostgreSQL desde un archivo SQL:

```bash
make restore-db DB=backups/database/archivo.sql
```

Respaldar archivos de `storage/media`:

```bash
make backup-media
```

## Alcance pendiente

No estan implementados todavia workflows completos, API, frontend final, permisos por documento, visor documental, notificaciones, reportes/exportacion Excel ni auditoria automatica conectada a eventos reales.
