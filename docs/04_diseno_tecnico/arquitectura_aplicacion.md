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

---

## 6. Frontend React/Vite

El directorio `frontend/` existe como base tecnica, pero no sera la interfaz principal inicial del MVP.

React/Vite queda reservado para:

* Componentes puntuales altamente interactivos.
* Visor documental especializado si se justifica.
* Una fase posterior de frontend separado.

No se construira una SPA completa sin una decision tecnica posterior.

---

## 7. Seguridad documental

La arquitectura debe preservar las reglas funcionales de consulta controlada:

* Usuarios lectores solo visualizan documentos asignados o aplicables.
* No se deben ofrecer descargas a usuarios lectores.
* No se deben exponer rutas directas de archivos documentales.
* La visualizacion debe auditarse cuando aplique.
* Las restricciones de copia, impresion y descarga son controles razonables de aplicacion, no proteccion absoluta.

---

## 8. Impacto DevOps

La decision hibrida mantiene el despliegue inicial simple:

* Backend Django.
* PostgreSQL.
* Nginx.
* Volumen persistente para archivos.
* Archivos estaticos servidos por Nginx en fases posteriores.

Cuando se agregue DRF no se requerira un servicio adicional. Si se activa React como frontend independiente, debera documentarse el impacto en Docker, Nginx, variables de entorno y despliegue.
