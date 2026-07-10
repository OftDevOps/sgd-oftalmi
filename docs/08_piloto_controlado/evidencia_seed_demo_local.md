# Evidencia de Seed Demo Local - PILOTO-P04

## 1. Proposito

Registrar la ejecucion controlada del seed demo en ambiente local Docker para validar que los datos definidos en PILOTO-P02 pueden cargarse de forma repetible y alimentar visor documental, reportes, exportaciones CSV y auditoria.

Esta validacion tecnica no inicia el piloto real con Organizacion y Metodos.

## 2. Ambiente validado

| Elemento | Resultado |
| --- | --- |
| Fecha de validacion | 2026-07-10 |
| Rama | `develop` |
| Commit base | `a8940a1 feat: add controlled pilot demo seed` |
| Ambiente | Docker Compose local |
| Servicios usados | `db`, `backend` |
| Datos usados | Ficticios demo definidos en PILOTO-P02 |

No se usaron datos productivos, usuarios reales ni documentos reales de Oftalmi.

## 3. Validaciones previas

Comandos ejecutados antes del seed:

```bash
git status
git log --oneline --decorate -20
make check
docker compose exec backend python manage.py makemigrations --check --dry-run
make test-base
make healthcheck
```

Resultados:

| Validacion | Resultado |
| --- | --- |
| `git status` | `develop` alineada con `origin/develop`; solo `docs/continuidad/` sin seguimiento y fuera de alcance. |
| `make check` | OK |
| `makemigrations --check --dry-run` | No changes detected |
| `make test-base` | 204 tests OK |
| `make healthcheck` | `200 {"status": "ok"}` |

## 4. Ejecucion de seeds

Comandos ejecutados:

```bash
docker compose exec backend python manage.py seed_base_catalogs
docker compose exec backend python manage.py seed_pilot_demo_data --dry-run
docker compose exec backend python manage.py seed_pilot_demo_data
docker compose exec backend python manage.py seed_pilot_demo_data
```

Resultados:

| Comando | Resultado |
| --- | --- |
| `seed_base_catalogs` | `0 created, 0 updated, 14 unchanged` |
| `seed_pilot_demo_data --dry-run` | Plan: `34 created, 9 updated, 0 existing` |
| `seed_pilot_demo_data` primera ejecucion | `34 created, 9 updated, 0 existing` |
| `seed_pilot_demo_data` segunda ejecucion | `0 created, 0 updated, 38 existing` |

La segunda ejecucion confirma idempotencia: no duplico usuarios, documentos, versiones, archivos, copias controladas ni registros de implementacion.

## 5. Datos demo validados

Consultas realizadas contra la base local:

| Dato | Resultado |
| --- | ---: |
| Usuarios demo | 7 |
| Unidades demo | 5 |
| Tipos documentales demo | 4 |
| Documentos demo | 5 |
| Versiones demo | 5 |
| Archivos PDF demo | 5 |
| Copias controladas demo | 4 |
| Registros de implementacion demo | 3 |
| Usuarios duplicados | 0 |
| Documentos duplicados | 0 |

## 6. Selectors de reportes

Resultados de selectors sobre datos demo:

| Selector | Registros demo devueltos |
| --- | ---: |
| Libro Maestro | 5 |
| Reporte mensual documental | 5 |
| Reporte de copias controladas | 4 |
| Reporte de implementacion/lectura | 3 |

## 7. Vistas y exportaciones de reportes

Las vistas se validaron con usuario `oym.admin.demo@oftalmi.test` y `HTTP_HOST=localhost`.

| Ruta | Resultado |
| --- | --- |
| `/app/reports/master-book/` | 200 |
| `/app/reports/monthly-documents/` | 200 |
| `/app/reports/controlled-copies/` | 200 |
| `/app/reports/implementation-records/` | 200 |
| `/app/reports/master-book/export.csv` | 200, `text/csv; charset=utf-8`, `attachment` |
| `/app/reports/monthly-documents/export.csv` | 200, `text/csv; charset=utf-8`, `attachment` |
| `/app/reports/controlled-copies/export.csv` | 200, `text/csv; charset=utf-8`, `attachment` |
| `/app/reports/implementation-records/export.csv` | 200, `text/csv; charset=utf-8`, `attachment` |

Validacion de seguridad documental en CSV:

| Control | Resultado |
| --- | --- |
| CSV sin `/media/` | OK |
| CSV sin `MEDIA_URL` | OK |
| CSV sin rutas fisicas de archivos | OK |

Auditoria generada por consulta/exportacion de reportes:

| Evento | Cantidad |
| --- | ---: |
| `AuditAction.REPORT_GENERATED` | 8 |
| `REPORT_VIEWED` | 4 |
| `REPORT_EXPORTED` | 4 |

## 8. Visor documental

Validacion con datos demo:

| Escenario | Resultado |
| --- | --- |
| `lector.produccion.demo@oftalmi.test` abre visor de `PROC-OYM-DEMO-001` | 200 |
| Entrega PDF protegida de `PROC-OYM-DEMO-001` | 200 |
| `Content-Type` de PDF | `application/pdf` |
| `Content-Disposition` de PDF | `inline; filename="proc-oym-demo-001-v1.pdf"` |
| `Cache-Control` de PDF | `no-store` |
| `sin.permiso.demo@oftalmi.test` intenta visor de `PROC-PROD-DEMO-002` | 403 |
| `sin.permiso.demo@oftalmi.test` intenta entrega PDF de `PROC-PROD-DEMO-002` | 403 |

Auditoria generada por visor/entrega documental:

| Evento | Cantidad |
| --- | ---: |
| `AuditAction.DOCUMENT_VIEWED` | 3 |
| `success` | 1 |
| `denied` | 2 |

## 9. Validaciones posteriores

Comandos ejecutados despues del seed:

```bash
git diff --check
python -m compileall backend
make check
docker compose exec backend python manage.py makemigrations --check --dry-run
docker compose exec backend python manage.py test apps.reports --settings=config.settings.test
make test-base
make healthcheck
```

Resultados:

| Validacion | Resultado |
| --- | --- |
| `git diff --check` | OK |
| `python -m compileall backend` | OK |
| `make check` | OK |
| `makemigrations --check --dry-run` | No changes detected |
| `apps.reports` | 74 tests OK |
| `make test-base` | 204 tests OK |
| `make healthcheck` | `200 {"status": "ok"}` |

## 10. Conclusiones

PILOTO-P04 confirma que el seed demo:

* Carga datos ficticios de forma controlada.
* Es idempotente.
* Alimenta visor documental, reportes y exportaciones CSV.
* Genera auditoria al consultar/exportar reportes.
* Genera auditoria al acceder o intentar acceder al documento controlado.
* No crea modelos ni migraciones.
* No inicia el piloto real.
* No usa datos reales ni productivos.

## 11. Pendiente sugerido

El siguiente punto recomendado es:

```text
PILOTO-P05 -> Guion de validacion funcional OyM
```

Ese punto debe preparar el guion funcional y operativo para una validacion formal posterior con Organizacion y Metodos. PILOTO-P04 no convoca usuarios ni ejecuta validacion funcional formal.
