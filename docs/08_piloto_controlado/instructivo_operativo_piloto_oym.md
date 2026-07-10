# Instructivo Operativo de Piloto OyM - PILOTO-P06

## 1. Objetivo operativo

Definir el procedimiento operativo para ejecutar, cuando sea autorizado, el piloto controlado del SGD-OFTALMI con Organizacion y Metodos.

Este documento deja preparada la ejecucion operativa, pero no inicia el piloto real, no convoca usuarios, no carga datos productivos y no autoriza despliegue productivo.

## 2. Alcance operativo

El instructivo cubre:

* Responsables funcionales y tecnicos.
* Ambiente objetivo.
* Precondiciones de arranque.
* Preparacion del ambiente.
* Carga o recarga de seed demo.
* URLs esperadas.
* Manejo seguro de credenciales demo.
* Uso del guion funcional OyM.
* Registro de observaciones e incidencias.
* Respaldo previo.
* Restauracion o rollback.
* Checklist de arranque.
* Checklist de cierre.
* Criterios para aprobar o suspender la ejecucion.

## 3. Ambiente objetivo

El piloto debe ejecutarse en un ambiente controlado no productivo.

Ambiente recomendado:

| Elemento | Criterio operativo |
| --- | --- |
| Rama | `develop` o commit aprobado para piloto. |
| Servicios | Docker Compose con `db` y `backend`. |
| Base de datos | PostgreSQL no productivo. |
| Archivos | PDFs demo ficticios generados o cargados por el seed. |
| Variables de entorno | No productivas y fuera del repositorio. |
| Usuarios | Solo usuarios demo definidos en PILOTO-P02. |
| Datos | Solo datos ficticios demo. |

No se debe ejecutar el piloto sobre base productiva, documentos reales ni cuentas de operacion diaria.

## 4. Responsables

| Rol | Responsable | Responsabilidad |
| --- | --- | --- |
| OyM funcional | Persona designada por Organizacion y Metodos | Validar escenarios, resultados funcionales y observaciones. |
| Sistemas tecnico | Persona designada por Sistemas | Preparar ambiente, respaldar, restaurar y dar soporte tecnico. |
| Soporte operativo | Sistemas o equipo asignado | Registrar incidencias, tiempos, evidencias y estado de servicios. |
| Observador o auditor | OyM, auditor interno o rol autorizado si aplica | Revisar trazabilidad y cumplimiento del guion sin modificar reglas funcionales. |

Sistemas no debe modificar reglas funcionales de OyM durante la ejecucion. Cualquier cambio funcional debe quedar como observacion para evaluacion posterior.

## 5. Precondiciones

Antes de autorizar la ejecucion del piloto deben cumplirse estas condiciones:

* Aprobacion explicita para ejecutar el piloto, separada de la aprobacion documental.
* Ambiente no productivo definido.
* Commit de referencia identificado.
* Variables de entorno no productivas configuradas.
* Contenedores `db` y `backend` operativos.
* Migraciones aplicadas y sin pendientes.
* `make check` aprobado.
* `make test-base` aprobado.
* `make healthcheck` con respuesta `200`.
* Respaldo previo planificado.
* Procedimiento de restauracion entendido por Sistemas.
* Datos demo definidos y autorizados.
* Guion funcional OyM revisado.
* Formato de observaciones disponible.
* Credenciales demo comunicadas fuera del repositorio.

## 6. Checklist de arranque

Antes de iniciar la sesion con OyM:

| Item | Estado |
| --- | --- |
| Confirmar autorizacion de ejecucion del piloto. | Pendiente |
| Confirmar ambiente no productivo. | Pendiente |
| Confirmar commit exacto a validar. | Pendiente |
| Ejecutar `git status`. | Pendiente |
| Ejecutar `make check`. | Pendiente |
| Ejecutar `makemigrations --check --dry-run`. | Pendiente |
| Ejecutar `make test-base`. | Pendiente |
| Ejecutar `make healthcheck`. | Pendiente |
| Ejecutar respaldo previo. | Pendiente |
| Confirmar restauracion o rollback disponible. | Pendiente |
| Confirmar seed demo cargado e idempotente. | Pendiente |
| Confirmar usuarios demo disponibles. | Pendiente |
| Confirmar credenciales demo entregadas por canal seguro. | Pendiente |
| Confirmar guion funcional abierto. | Pendiente |
| Confirmar formato de observaciones disponible. | Pendiente |

## 7. Procedimiento de preparacion del ambiente

1. Confirmar que se esta en la ruta local del proyecto.
2. Confirmar rama y commit:

```bash
git status
git log --oneline --decorate -5
```

3. Levantar servicios si no estan activos:

```bash
docker compose up -d db backend
```

4. Validar configuracion Django:

```bash
make check
docker compose exec backend python manage.py makemigrations --check --dry-run
make test-base
make healthcheck
```

5. Confirmar que no se usaran `.env`, respaldos, archivos ni credenciales productivas.
6. Registrar fecha, hora, responsable tecnico, commit y ambiente.

## 8. Procedimiento de carga seed demo

La carga demo debe ejecutarse solo cuando el ambiente este confirmado como no productivo.

Comandos esperados:

```bash
docker compose exec backend python manage.py seed_base_catalogs
docker compose exec backend python manage.py seed_pilot_demo_data --dry-run
docker compose exec backend python manage.py seed_pilot_demo_data
docker compose exec backend python manage.py seed_pilot_demo_data
```

La segunda ejecucion de `seed_pilot_demo_data` debe confirmar idempotencia y no duplicacion.

Si se requiere definir una contrasena demo temporal, debe usarse el parametro `--password` y comunicarse solo fuera del repositorio:

```bash
docker compose exec backend python manage.py seed_pilot_demo_data --password "<valor-temporal-fuera-del-repositorio>"
```

No se deben registrar contrasenas reales, productivas ni institucionales en documentacion, commits, logs compartidos o tickets.

## 9. URLs de acceso esperadas

Las URLs deben ajustarse al host del ambiente de piloto. En ambiente local Docker:

| Uso | URL esperada |
| --- | --- |
| Login | `http://localhost:8000/accounts/login/` |
| Dashboard | `http://localhost:8000/app/` |
| Documentos | `http://localhost:8000/app/documents/` |
| Solicitudes documentales | `http://localhost:8000/app/document-requests/` |
| Copias controladas | `http://localhost:8000/app/controlled-copies/` |
| Implementacion/lectura | `http://localhost:8000/app/implementation-records/` |
| Auditoria | `http://localhost:8000/app/audit/` |
| Libro Maestro | `http://localhost:8000/app/reports/master-book/` |
| Reporte mensual | `http://localhost:8000/app/reports/monthly-documents/` |
| Reporte copias controladas | `http://localhost:8000/app/reports/controlled-copies/` |
| Reporte implementacion/lectura | `http://localhost:8000/app/reports/implementation-records/` |
| Healthcheck | `http://localhost:8000/health/` |

No se debe acceder directamente a rutas fisicas de archivos ni a almacenamiento de media para documentos controlados.

## 10. Usuarios demo y manejo seguro de credenciales

Usuarios demo autorizados para el piloto:

| Usuario demo | Uso |
| --- | --- |
| `oym.admin.demo@oftalmi.test` | Validacion funcional OyM, reportes, auditoria y Libro Maestro. |
| `oym.analista.demo@oftalmi.test` | Operacion documental OyM. |
| `unidad.produccion.demo@oftalmi.test` | Solicitudes y consulta por unidad ejecutora. |
| `lector.produccion.demo@oftalmi.test` | Visor e implementacion/lectura. |
| `auditor.demo@oftalmi.test` | Auditoria. |
| `sistemas.demo@oftalmi.test` | Soporte tecnico y restricciones funcionales. |
| `sin.permiso.demo@oftalmi.test` | Escenarios negativos de permisos. |

Reglas de manejo:

* Las credenciales demo no deben quedar en el repositorio.
* La contrasena demo debe comunicarse por canal controlado y temporal.
* La contrasena demo debe cambiarse o invalidarse al cerrar el piloto.
* No se deben usar correos ni contrasenas reales.
* No se deben crear usuarios reales de operacion en este ambiente.

## 11. Guion de ejecucion referenciado

La ejecucion funcional debe seguir el guion:

```text
docs/08_piloto_controlado/guion_validacion_funcional_oym.md
```

Ese guion define escenarios, pasos, resultados esperados y evidencia requerida. Cualquier desviacion debe registrarse como observacion y no resolverse modificando reglas funcionales durante la sesion.

## 12. Formato de observaciones e incidencias

Las observaciones deben registrarse usando:

```text
docs/08_piloto_controlado/formato_observaciones_piloto.md
```

Cada observacion debe incluir:

* Codigo.
* Fecha y hora.
* Escenario.
* Usuario demo.
* Rol.
* Modulo.
* Resultado esperado.
* Resultado observado.
* Evidencia.
* Clasificacion.
* Responsable sugerido.
* Decision de cierre.

## 13. Clasificacion de hallazgos

| Clasificacion | Definicion | Accion |
| --- | --- | --- |
| Bloqueo | Impide continuar o compromete seguridad, permisos, datos o auditoria. | Suspender escenario o piloto segun impacto. |
| Alto | Afecta un flujo principal, pero permite continuar con controles temporales. | Priorizar correccion antes de despliegue interno. |
| Medio | Afecta usabilidad, texto, filtro o flujo secundario. | Registrar y planificar correccion. |
| Bajo | Observacion menor sin impacto funcional critico. | Registrar para mejora. |
| Mejora | Sugerencia futura fuera del alcance validado. | Evaluar para backlog posterior. |

## 14. Procedimiento de respaldo

Antes de iniciar la sesion:

1. Registrar commit, rama, fecha, ambiente y responsable.
2. Confirmar que la base no contiene datos productivos.
3. Generar respaldo de PostgreSQL del ambiente piloto.
4. Generar respaldo del almacenamiento de archivos demo si aplica.
5. Identificar respaldos con fecha, ambiente y commit.
6. Proteger respaldos contra acceso no autorizado.
7. Registrar ubicacion del respaldo fuera del repositorio.

Los respaldos no deben versionarse en Git.

## 15. Procedimiento de restauracion

La restauracion debe ejecutarse si existe bloqueo critico, corrupcion de datos demo o necesidad de repetir el piloto desde estado inicial.

Pasos:

1. Detener la sesion funcional.
2. Informar a OyM el motivo de restauracion.
3. Detener servicios si el procedimiento tecnico lo requiere.
4. Restaurar respaldo de PostgreSQL.
5. Restaurar archivos demo si aplica.
6. Levantar servicios.
7. Ejecutar `make healthcheck`.
8. Validar login con usuario demo autorizado.
9. Registrar resultado de restauracion.

No se debe restaurar desde respaldos productivos.

## 16. Checklist de cierre

Al finalizar la sesion:

| Item | Estado |
| --- | --- |
| Escenarios ejecutados registrados. | Pendiente |
| Observaciones clasificadas. | Pendiente |
| Evidencias recolectadas. | Pendiente |
| Incidencias bloqueantes identificadas. | Pendiente |
| Auditoria revisada. | Pendiente |
| Reportes y CSV revisados. | Pendiente |
| Resultado funcional emitido por OyM. | Pendiente |
| Resultado tecnico emitido por Sistemas. | Pendiente |
| Acciones correctivas preliminares definidas. | Pendiente |
| Credenciales demo revocadas, cambiadas o resguardadas segun decision. | Pendiente |
| Respaldo final o limpieza documentada. | Pendiente |
| Comunicacion de cierre enviada. | Pendiente |

## 17. Criterios para aprobar piloto

El piloto puede aprobarse si:

* OyM valida que los escenarios principales representan el MVP esperado.
* Los roles acceden solo a lo autorizado.
* Los usuarios sin permiso reciben denegacion donde corresponde.
* El visor no expone rutas directas de archivos.
* Los reportes muestran datos demo coherentes.
* La exportacion CSV no incluye PDFs, adjuntos ni rutas fisicas.
* La auditoria permite reconstruir acciones relevantes.
* No quedan bloqueos criticos abiertos.
* Sistemas valida operacion basica, respaldo, restauracion y healthcheck.

## 18. Criterios para suspender piloto

El piloto debe suspenderse si:

* Se detecta uso de datos productivos o sensibles.
* Falla el healthcheck y no puede recuperarse durante la ventana.
* Hay migraciones pendientes no controladas.
* Un usuario sin permiso accede a documentos, auditoria o reportes restringidos.
* Se exponen rutas fisicas, `/media/` o archivos documentales en reportes.
* No existe respaldo previo.
* La restauracion no es viable.
* OyM identifica una regla funcional incorrecta que invalida el flujo.
* Se requiere modificar codigo o reglas funcionales durante la sesion.

## 19. Comunicacion de cierre

Al cerrar la sesion, Sistemas y OyM deben emitir una comunicacion breve con:

* Fecha y duracion.
* Ambiente y commit probado.
* Participantes.
* Escenarios ejecutados.
* Resultado: aprobado, aprobado con observaciones, suspendido o rechazado.
* Hallazgos por clasificacion.
* Acciones requeridas.
* Decision sobre siguiente paso.

La comunicacion de cierre no reemplaza el registro de observaciones ni la evidencia tecnica.

## 20. Confirmacion explicita

PILOTO-P06 no inicia el piloto real con Organizacion y Metodos.

La ejecucion real del piloto requiere una autorizacion posterior y explicita, con fecha, responsables, ambiente y ventana definidos.

PILOTO-P06 no crea codigo funcional, modelos, migraciones, usuarios reales ni datos productivos.
