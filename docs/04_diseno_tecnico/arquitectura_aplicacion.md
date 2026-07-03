# Arquitectura de Aplicacion - SGD-OFTALMI

## 1. Proposito

Este documento describe la arquitectura tecnica de aplicacion para la Fase 2 del MVP.

La decision base de esta fase es construir una capa de acceso hibrida controlada:

```text
Django templates como interfaz principal del MVP
+ API interna DRF solo cuando sea necesaria
```

Esta arquitectura mantiene la prioridad del proyecto: trazabilidad, seguridad por roles, operacion interna reproducible y control funcional por Organizacion y Metodos.

---

## 2. Principios

* Mantener el backend Django como fuente principal de reglas y permisos.
* Evitar duplicar reglas entre vistas web, endpoints API y admin.
* Construir primero pantallas internas simples y auditables.
* Agregar API solo cuando exista una necesidad tecnica concreta.
* No exponer archivos documentales por rutas publicas directas.
* Mantener la operacion compatible con Docker Compose, Nginx y PostgreSQL.

---

## 3. Capas de la aplicacion

### 3.1 Presentacion web

La interfaz principal del MVP se construira con Django templates.

Uso esperado:

* Layout base.
* Login/logout con sesion Django.
* Dashboard base por rol.
* Pantallas de catalogos.
* Pantallas de documentos.
* Pantallas de solicitudes documentales.
* Pantallas de copias controladas.
* Pantallas de constancias.
* Pantallas de auditoria y reportes cuando correspondan.

### 3.2 API interna

La API interna se implementara con Django REST Framework solo cuando sea necesaria.

Uso esperado:

* Busquedas y autocompletados.
* Componentes dinamicos.
* Transiciones de estado.
* Registro de acciones desde componentes asincronos.
* Endpoints internos para visor documental futuro.
* Notificaciones internas futuras.

La API debera usar rutas versionadas:

```text
/api/v1/
```

No se considera API publica para esta fase.

### 3.3 Logica de negocio

La logica debe permanecer fuera de vistas y endpoints.

Ubicaciones esperadas:

```text
services.py
selectors.py
workflows.py
permissions.py
```

Las vistas Django y los endpoints DRF deben invocar estas capas.

### 3.4 Persistencia

La persistencia se mantiene en PostgreSQL mediante modelos Django.

Los archivos documentales deben persistirse fuera del contenedor de aplicacion, bajo almacenamiento configurado por volumen.

---

## 4. Autenticacion y autorizacion

La autenticacion inicial sera por sesion Django.

Criterios:

* Login con correo institucional.
* CSRF activo.
* Logout por POST y pantalla visual de sesion cerrada.
* Redireccion inicial por rol despues del login.
* Permisos por rol y modulo.
* Restricciones por unidad ejecutora cuando aplique.
* DRF, cuando se agregue, debera iniciar con autenticacion por sesion y permisos internos.

No se implementara JWT, OAuth externo, LDAP ni Active Directory en esta fase.

Redirecciones iniciales por rol:

| Rol | Destino inicial |
| --- | --- |
| OyM Administrador Funcional | `/app/documents/` |
| Analista OyM | `/app/documents/` |
| Unidad Ejecutora | `/app/document-requests/` |
| Usuario Lector | `/app/documents/` |
| Sistemas Administrador Tecnico | `/app/users/` |
| Auditor | `/app/audit/` |

---

## 5. Rutas previstas

Estructura inicial implementada:

```text
/                     Redireccion a /app/
/accounts/login/      Login con sesion Django
/accounts/logout/     Logout con sesion Django
/accounts/logged-out/ Pantalla de sesion cerrada
/admin/               Django admin
/health/              Health check tecnico
/app/                 Dashboard autenticado
/app/...              Vistas base por modulo
/api/v1/              Indice reservado de API interna
```

Las rutas de modulo se implementan con Django templates y permisos base:

```text
/app/users/
/app/catalogs/organizational-units/
/app/catalogs/organizational-units/<id>/
/app/catalogs/document-types/
/app/catalogs/document-types/<id>/
/app/documents/
/app/documents/<id>/
/app/document-requests/
/app/document-requests/new/
/app/document-requests/<id>/
/app/controlled-copies/
/app/controlled-copies/<id>/
/app/implementation-records/
/app/implementation-records/new/
/app/implementation-records/<id>/
/app/audit/
/app/audit/<id>/
/app/reports/
/app/notifications/
```

Esta estructura podra ajustarse durante la implementacion de Fase 2 si no contradice la decision ADR-001.

El dashboard base por rol muestra contenido orientativo y accesos principales segun perfil. No calcula metricas reales complejas, no implementa reportes y no consulta informacion documental sensible.

Las vistas iniciales de catalogos son de solo lectura. Permiten listar y consultar detalle basico de unidades ejecutoras y tipos documentales usando permisos existentes. La creacion, edicion y eliminacion desde vistas funcionales queda fuera de este punto.

Las vistas iniciales de documentos son de consulta base. Permiten listar, ver detalle, revisar versiones asociadas y consultar metadatos de archivos sin exponer descarga ni visor documental. La carga de archivos, aprobacion y cambios de estado quedan fuera de este punto.

Las vistas iniciales de solicitudes documentales permiten listado, detalle y creacion simple en estado borrador usando servicios existentes. El procesamiento operativo de solicitudes, aprobacion, rechazo, observaciones complejas y notificaciones quedan fuera de esta etapa.

Las vistas iniciales de copias controladas permiten listado y detalle base. OyM consulta todas las copias, mientras que destinatarios por usuario o unidad consultan solo las copias aplicables. La creacion, edicion, entrega, retiro, constancias, reportes y notificaciones quedan fuera de esta etapa.

Las vistas iniciales de registros de implementacion permiten listado, detalle y creacion simple de registro propio pendiente. La emision de certificados, firma formal, numeracion de constancias, PDF, reportes y notificaciones quedan fuera de esta etapa.

Las vistas iniciales de auditoria permiten listado y detalle base de eventos con acceso restringido por helpers existentes. La exportacion, reportes, filtros avanzados y modificacion de eventos quedan fuera de esta etapa.

Las vistas internas de Fase 2 deben usar `ModuleAccessMixin` o `ModuleIndexView` para asegurar login requerido, ejecucion del helper de permiso correspondiente y navegacion de modulo consistente. Las pruebas transversales por rol verifican los codigos 200/403 esperados para las rutas principales.

---

## 6. Cierre tecnico de Fase 2

La Fase 2 deja implementada una capa de acceso interna basada en Django templates, sesiones Django y permisos por rol apoyados en helpers existentes. La interfaz resultante es operativa para consulta y registro base, pero no sustituye workflows documentales completos ni implementa visor documental final.

### 6.1 Rutas actuales

| Ruta | Vista / proposito | Acceso |
| --- | --- | --- |
| `/` | Redireccion inicial segun autenticacion | Publica con redireccion |
| `/accounts/login/` | Login con correo institucional | Publica |
| `/accounts/logout/` | Logout de sesion | Usuario autenticado |
| `/accounts/logged-out/` | Confirmacion visual de cierre de sesion | Publica |
| `/app/` | Dashboard base por rol | Login requerido |
| `/app/users/` | Modulo base de usuarios | OyM Admin, Sistemas Tecnico |
| `/app/catalogs/organizational-units/` | Listado de unidades ejecutoras | Segun `can_view_organizational_units` |
| `/app/catalogs/organizational-units/<id>/` | Detalle de unidad ejecutora | Segun `can_view_organizational_units` |
| `/app/catalogs/document-types/` | Listado de tipos documentales | Segun `can_view_document_types` |
| `/app/catalogs/document-types/<id>/` | Detalle de tipo documental | Segun `can_view_document_types` |
| `/app/documents/` | Listado documental base | Segun `can_access_documents_module` |
| `/app/documents/<id>/` | Detalle documental con versiones y metadata de archivos | Segun `can_access_documents_module` y queryset visible |
| `/app/document-requests/` | Listado de solicitudes documentales | Segun `can_access_document_requests_module` |
| `/app/document-requests/new/` | Creacion simple de solicitud documental | Segun `can_create_document_request` |
| `/app/document-requests/<id>/` | Detalle de solicitud documental | Segun permisos de modulo y queryset visible |
| `/app/controlled-copies/` | Listado de copias controladas | Segun `can_view_controlled_copies` |
| `/app/controlled-copies/<id>/` | Detalle de copia controlada | Segun permisos de modulo y queryset visible |
| `/app/implementation-records/` | Listado de registros de implementacion | Usuario activo, con queryset segun rol |
| `/app/implementation-records/new/` | Registro simple propio de implementacion | Usuario activo |
| `/app/implementation-records/<id>/` | Detalle de registro de implementacion | Usuario activo, con queryset segun rol |
| `/app/audit/` | Listado restringido de auditoria | Segun `can_view_audit` |
| `/app/audit/<id>/` | Detalle restringido de evento de auditoria | Segun `can_view_audit` |
| `/app/reports/` | Modulo reservado de reportes | Segun `can_view_reports` |
| `/app/notifications/` | Modulo reservado de notificaciones | Usuario activo |
| `/api/v1/` | Indice reservado de API interna | Login requerido |
| `/admin/` | Django admin | Staff/admin Django |
| `/health/` | Health check tecnico | Operacion tecnica |

### 6.2 Permisos aplicados

Los permisos de Fase 2 se aplican mediante `ModuleAccessMixin`, `ModuleIndexView`, helpers de `permissions.py` y helpers de navegacion de `config.navigation`.

| Modulo | Helper principal | Roles con acceso actual |
| --- | --- | --- |
| Dashboard | `LoginRequiredMixin` + `get_module_navigation` | Todo usuario autenticado |
| Usuarios | `can_view_users` | OyM Admin, Sistemas Tecnico |
| Unidades ejecutoras | `can_view_organizational_units` | OyM Admin, Analista OyM, Sistemas Tecnico |
| Tipos documentales | `can_view_document_types` | OyM Admin, Analista OyM, Unidad Ejecutora |
| Documentos | `can_access_documents_module` | OyM Admin, Analista OyM, Unidad Ejecutora, Usuario Lector |
| Solicitudes documentales | `can_access_document_requests_module` | OyM Admin, Analista OyM, Unidad Ejecutora, Sistemas Tecnico |
| Crear solicitud documental | `can_create_document_request` | OyM Admin, Analista OyM, Unidad Ejecutora, Sistemas Tecnico |
| Copias controladas | `can_view_controlled_copies` | OyM Admin, Analista OyM, Unidad Ejecutora, Usuario Lector |
| Registros de implementacion | `can_access_implementation_records_module` | Todo usuario activo |
| Crear registro de implementacion | `is_active_user` | Todo usuario activo |
| Auditoria | `can_view_audit` | OyM Admin, Analista OyM, Auditor, Sistemas Tecnico |
| Reportes | `can_view_reports` | OyM Admin, Analista OyM |
| Notificaciones | `can_view_own_notifications` | Todo usuario activo |

Las vistas que muestran registros usan selectors o querysets acotados para no exponer informacion fuera del alcance del rol. Las pruebas integradas verifican login requerido, codigos 200/403, templates principales y navegacion visible por rol.

### 6.3 Validaciones de cierre

Validaciones tecnicas registradas al cierre de Fase 2:

```text
python -m compileall backend
docker compose exec backend python manage.py makemigrations --check --dry-run
make check
make test-base
make healthcheck
```

Resultado esperado y validado:

```text
compileall -> OK
makemigrations --check --dry-run -> No changes detected
make check -> OK
make test-base -> 179 tests OK
make healthcheck -> 200 {"status": "ok"}
```

### 6.4 Exclusiones confirmadas

Fase 2 no implementa:

* API funcional.
* Frontend SPA.
* Nuevos modelos o migraciones.
* Workflows documentales completos.
* Aprobaciones, rechazos u observaciones operativas completas.
* Reportes finales ni exportacion Excel.
* Visor documental final.
* Descarga controlada de archivos.
* Restricciones finales de impresion, copia o captura.
* Notificaciones operativas.
* Auditoria automatica adicional fuera de lo ya definido.

### 6.5 Pendientes para Fase 3

La Fase 3 debe enfocarse en visor documental y restricciones de consulta controlada:

* Definir el patron tecnico del visor documental.
* Evitar exposicion directa de archivos documentales.
* Registrar auditoria de visualizacion cuando aplique.
* Aplicar permisos por documento, version, usuario y unidad.
* Bloquear descargas directas para usuarios lectores desde la aplicacion.
* Agregar controles razonables contra impresion y copia desde la interfaz.
* Evaluar marcas de agua o metadatos visibles para trazabilidad.
* Mantener claro que estos controles no son proteccion absoluta contra capturas externas.
* Agregar pruebas especificas de acceso a documentos y archivos.

---

## 7. Frontend React/Vite

El directorio `frontend/` existe como base tecnica, pero no sera la interfaz principal inicial del MVP.

React/Vite queda reservado para:

* Componentes puntuales altamente interactivos.
* Visor documental especializado si se justifica.
* Una fase posterior de frontend separado.

No se construira una SPA completa sin una decision tecnica posterior.

---

## 8. Seguridad documental

La arquitectura debe preservar las reglas funcionales de consulta controlada:

* Usuarios lectores solo visualizan documentos asignados o aplicables.
* No se deben ofrecer descargas a usuarios lectores.
* No se deben exponer rutas directas de archivos documentales.
* La visualizacion debe auditarse cuando aplique.
* Las restricciones de copia, impresion y descarga son controles razonables de aplicacion, no proteccion absoluta.

La definicion tecnica inicial del visor documental se registra en:

```text
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

Esta decision establece que el visor debe iniciar con PDF como formato prioritario, que los archivos no deben exponerse por rutas directas, y que cada acceso debe pasar por una vista o servicio controlado con validacion de permisos y auditoria minima. Los archivos Office quedan pendientes de conversion previa a PDF o evaluacion tecnica posterior.

F3-P02 implementa la primera entrega controlada de archivos PDF mediante una ruta interna protegida del modulo `documents`. Esta ruta valida usuario, documento, version y archivo, registra auditoria de accesos permitidos y denegados, y no reemplaza todavia al visor visual final con marcas de agua o controles de interfaz.

F3-P03 fortalece el permiso fino del archivo: OyM conserva acceso funcional; Sistemas y Auditor no acceden al contenido documental por esta ruta; Unidad Ejecutora y Usuario Lector requieren relacion aplicable por unidad, copia controlada o registro de implementacion. La respuesta para usuarios autenticados sin permiso es `403`; las inconsistencias o inexistencia de documento, version, archivo o archivo fisico mantienen `404`.

Nota tecnica: la autorizacion documental actual se apoya en relaciones existentes del modelo (`rol`, `unidad organizativa`, `copia controlada`, `registro de implementacion`, `documento`, `version` y `archivo activo`). No existe todavia una matriz formal independiente `documento <-> usuario autorizado` o `documento <-> unidad autorizada`. Esa relacion no debe agregarse sin validacion funcional de Organizacion y Metodos. Queda pendiente evaluar dicha matriz si el proceso documental lo requiere.

---

## 9. Impacto DevOps

La decision hibrida mantiene el despliegue inicial simple:

* Backend Django.
* PostgreSQL.
* Nginx.
* Volumen persistente para archivos.
* Archivos estaticos servidos por Nginx en fases posteriores.

Cuando se agregue DRF no se requerira un servicio adicional. Si se activa React como frontend independiente, debera documentarse el impacto en Docker, Nginx, variables de entorno y despliegue.
