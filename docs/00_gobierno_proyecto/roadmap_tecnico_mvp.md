# Roadmap Técnico MVP - SGD-OFTALMI

## 1. Propósito del documento

Este documento define la ruta técnica de la primera fase del MVP del proyecto **SGD-OFTALMI**, correspondiente al backend base del Sistema de Gestión Documental administrado por Organización y Métodos.

Su propósito es mantener trazabilidad entre:

* El alcance funcional validado con Organización y Métodos.
* La documentación técnica del proyecto.
* Las tareas ejecutadas con apoyo de Codex.
* Los commits realizados en el repositorio.
* Los puntos pendientes antes de pasar a fases posteriores.

Este roadmap funciona como bitácora técnica del MVP y debe mantenerse actualizado a medida que se completen nuevos puntos.

---

## 2. Contexto del MVP

SGD-OFTALMI es una aplicación interna para la Gestión Documental de Laboratorios L.O. Oftalmi C.A.

El dueño funcional del MVP es **Organización y Métodos**.

La Unidad de Soporte y Desarrollo Tecnológico, en adelante Sistemas, administra la plataforma técnica, infraestructura, despliegue, soporte y operación. Sistemas no define las reglas funcionales del proceso documental.

La Gerencia de Garantía de la Calidad no es dueña funcional del MVP. Puede actuar como unidad usuaria, consultora o destinataria si sus documentos se gestionan bajo metodología de Organización y Métodos.

La primera fase técnica busca construir y estabilizar el backend base antes de avanzar a:

* API.
* Frontend.
* Vistas web definitivas.
* Visor documental.
* Reportes.
* Notificaciones.
* Workflows completos.
* Despliegue productivo definitivo.

---

## 3. Criterios de gobierno técnico

El desarrollo técnico del MVP se rige por los siguientes criterios:

1. La rama `develop` es la rama de trabajo activo.
2. La rama `main` se conserva como versión estable aprobada.
3. No se debe hacer push a `main` sin instrucción explícita.
4. No se debe usar `force push`.
5. Cada punto técnico debe cerrar con:

   * Código implementado si aplica.
   * Migraciones limpias si aplica.
   * Pruebas unitarias o integradas si aplica.
   * Validaciones ejecutadas.
   * Commit separado y descriptivo.
   * Push únicamente a `origin/develop`.
6. Las reglas funcionales no deben inventarse si requieren validación de Organización y Métodos.
7. La lógica de negocio debe separarse progresivamente en servicios, selectors, workflows o helpers, evitando concentrarla en admin, vistas o APIs.
8. El backend debe mantenerse reproducible mediante Docker, Makefile, scripts y documentación operativa.
9. La documentación debe reflejar el estado real del proyecto.

---

## 4. Alcance de la primera fase técnica

La primera fase técnica corresponde al **backend MVP base**.

Incluye:

* Configuración inicial del backend.
* Modelo de usuarios con email como identificador.
* Catálogos base.
* Modelo documental base.
* Solicitudes documentales base.
* Copias controladas base.
* Registros de implementación base.
* Auditoría base.
* Roles y permisos base.
* Servicios/selectors base.
* Transiciones controladas de estado.
* Consolidación técnica del backend.
* Roadmap técnico formal.
* Preparación para carga inicial de catálogos.

No incluye todavía:

* Frontend.
* API completa.
* Vistas definitivas.
* Visor documental.
* Bloqueo real de descarga, impresión o copia.
* Reportes Excel.
* Libro Maestro automatizado.
* Notificaciones.
* Correos automáticos.
* Firma electrónica avanzada.
* Constancias formales con numeración.
* Workflows completos de aprobación.
* Integración con Wazuh/SIEM.
* Despliegue productivo definitivo.

---

## 5. Roadmap de 25 puntos

La primera fase técnica del MVP queda organizada en 25 puntos principales, con una tarea documental intercalada denominada **Punto 19B**.

| Punto     | Nombre                                                                 | Estado     |
| --------- | ---------------------------------------------------------------------- | ---------- |
| Punto 01  | Levantamiento funcional inicial con OyM                                | Completado |
| Punto 02  | Identificación de documentos rectores y procesos de gestión documental | Completado |
| Punto 03  | Validación del alcance MVP con OyM                                     | Completado |
| Punto 04  | Definición de reglas funcionales base                                  | Completado |
| Punto 05  | Definición de roles y permisos funcionales preliminares                | Completado |
| Punto 06  | Definición del modelo preliminar de datos                              | Completado |
| Punto 07  | Definición de estructura del repositorio                               | Completado |
| Punto 08  | Definición de AGENTS.md para Codex                                     | Completado |
| Punto 09  | Creación de documentación base del proyecto                            | Completado |
| Punto 10  | Validación documental previa al desarrollo                             | Completado |
| Punto 11  | Configuración técnica inicial Django/Docker/PostgreSQL                 | Completado |
| Punto 12  | Catálogos base: unidades organizativas y tipos documentales            | Completado |
| Punto 13  | Modelo documental base                                                 | Completado |
| Punto 14A | Secuencias base de codificación documental                             | Completado |
| Punto 14B | Solicitudes documentales base                                          | Completado |
| Punto 15  | Copias controladas base                                                | Completado |
| Punto 16  | Constancias base / ImplementationRecord                                | Completado |
| Punto 17  | Auditoría base                                                         | Completado |
| Punto 18  | Roles y permisos base                                                  | Completado |
| Punto 19  | Consolidación técnica del backend base                                 | Completado |
| Punto 19B | Documentación formal del roadmap técnico MVP                           | Completado |
| Punto 20  | Servicios/selectors base del núcleo documental                         | Completado |
| Punto 21  | Permisos finos por acción/módulo                                       | Completado |
| Punto 22  | Transiciones de estados documentales                                   | Completado |
| Punto 23  | Transiciones de estados de solicitudes documentales                    | Completado |
| Punto 24  | Servicios de auditoría automática controlada                           | Completado |
| Punto 25  | Carga inicial / seed de catálogos base                                 | Completado |

---

## 6. Estado actual de avance

La primera fase técnica del backend base se encuentra completada en la rama `develop`.

Último avance técnico registrado:

```text
Punto 23 -> Transiciones de estados de solicitudes documentales
Punto 24 -> Servicios de auditoría automática controlada
Punto 25 -> Carga inicial / seed de catálogos base
F2-P01  -> Decisión técnica de capa de acceso
F2-P02  -> Estructura base de URLs, vistas y capa de acceso
F2-P03  -> Login, logout y redirección por rol
F2-P04  -> Dashboard base por rol
F2-P05  -> Catálogos: vistas de unidades organizativas y tipos documentales
F2-P06  -> Documentos: listado, detalle y consulta base
F2-P07  -> Solicitudes documentales: creación y consulta base
F2-P08  -> Copias controladas: consulta base
F2-P09  -> Implementation records: consulta y registro base
F2-P10  -> Auditoría: consulta restringida base
F2-P11  -> Aplicación transversal de permisos por rol en vistas
F2-P12  -> Pruebas integradas de capa de acceso
F2-P13  -> Documentación técnica de cierre de Fase 2
F3-P01  -> Definición técnica del visor documental
F3-P02  -> Servicio de entrega controlada de archivos
F3-P03  -> Validación de acceso por usuario/unidad/documento
F3-P04  -> Vista de consulta documental controlada
F3-P05  -> Registro de acceso a documentos
F3-P06  -> Restricción de descarga según viabilidad técnica
F3-P07  -> Restricción de impresión según viabilidad técnica
F3-P08  -> Marca de agua o identificación de usuario
F3-P09  -> Pruebas de seguridad del visor
F3-P10  -> Documentación de limitaciones reales del visor
F4-P01  -> Definición técnica y funcional de reportes y Libro Maestro
F4-P02  -> Selectors base de reportes
F4-P03  -> Vista de Libro Maestro documental
F4-P04  -> Filtros de Libro Maestro
F4-P05  -> Reporte mensual documental
```

Último commit técnico conocido en `develop`:

```text
fcf887c docs: close phase 2 access layer documentation
```

Estado de ramas conocido:

```text
develop -> trabajo activo
main    -> versión estable aprobada
```

La rama `main` permanece estable en:

```text
b599e00 chore: configure initial Django backend
```

---

## 7. Puntos completados

### Punto 01 - Levantamiento funcional inicial con OyM

**Estado:** Completado.

**Descripción:**
Se inició el levantamiento funcional con Organización y Métodos para identificar el alcance preliminar del sistema de gestión documental.

**Resultado:**
Se confirmó que el sistema debe responder a necesidades de gestión documental administradas por OyM.

**Evidencia:**
Documentación de levantamiento funcional y validaciones posteriores de OyM.

---

### Punto 02 - Identificación de documentos rectores y procesos de gestión documental

**Estado:** Completado.

**Descripción:**
Se revisaron documentos rectores, documentos complementarios y procesos asociados a la gestión documental.

**Resultado:**
Se identificaron procesos como codificación, solicitudes, recepción, control, archivo, modificación, difusión, implementación, desincorporación y copias controladas.

**Evidencia:**
Documentos base de levantamiento y validaciones OyM.

---

### Punto 03 - Validación del alcance MVP con OyM

**Estado:** Completado.

**Descripción:**
Se validó con OyM el alcance funcional inicial del MVP.

**Resultado:**
Se confirmó que OyM es el dueño funcional del MVP y que Calidad queda fuera como dueño funcional del sistema.

**Evidencia:**
`docs/00_gobierno_proyecto/alcance_mvp.md`
`docs/01_levantamiento_oym/validaciones_oym.md`

---

### Punto 04 - Definición de reglas funcionales base

**Estado:** Completado.

**Descripción:**
Se definieron reglas iniciales sobre documentos, usuarios, roles, obsolescencia, lectura, implementación, reportes y restricciones.

**Resultado:**
El sistema debe soportar consulta controlada, confirmación de lectura/implementación, trazabilidad y reportes para OyM.

**Evidencia:**
`docs/02_requerimientos/reglas_negocio.md`

---

### Punto 05 - Definición de roles y permisos funcionales preliminares

**Estado:** Completado.

**Descripción:**
Se definieron roles funcionales preliminares para OyM, Sistemas, unidades ejecutoras, lectores y auditoría.

**Resultado:**
Se estableció la base para roles como OyM Admin, Analista OyM, Sistemas Técnico, Unidad Ejecutora, Lector y Auditor.

**Evidencia:**
`docs/03_diseno_funcional/roles_permisos.md`

---

### Punto 06 - Definición del modelo preliminar de datos

**Estado:** Completado.

**Descripción:**
Se definió el modelo preliminar de entidades principales del sistema.

**Resultado:**
Se identificaron entidades como User, OrganizationalUnit, DocumentType, Document, DocumentVersion, DocumentFile, DocumentRequest, ControlledCopy, ImplementationRecord y AuditEvent.

**Evidencia:**
`docs/04_diseno_tecnico/modelo_datos.md`

---

### Punto 07 - Definición de estructura del repositorio

**Estado:** Completado.

**Descripción:**
Se definió la estructura de carpetas y apps del repositorio.

**Resultado:**
El repositorio quedó organizado por backend, apps, infraestructura, documentación, scripts y almacenamiento.

**Evidencia:**
Estructura del repositorio `sgd-oftalmi`.

---

### Punto 08 - Definición de AGENTS.md para Codex

**Estado:** Completado.

**Descripción:**
Se creó o actualizó `AGENTS.md` para orientar a Codex en el contexto del proyecto.

**Resultado:**
Codex cuenta con instrucciones de alcance, restricciones, stack técnico, reglas funcionales y flujo de trabajo.

**Evidencia:**
`AGENTS.md`

---

### Punto 09 - Creación de documentación base del proyecto

**Estado:** Completado.

**Descripción:**
Se crearon documentos base de gobierno, levantamiento, requerimientos, diseño funcional y diseño técnico.

**Resultado:**
El proyecto cuenta con documentación inicial para sustentar el desarrollo técnico.

**Evidencia:**
Carpetas bajo `docs/`.

---

### Punto 10 - Validación documental previa al desarrollo

**Estado:** Completado.

**Descripción:**
Se consolidó la documentación validada antes de iniciar la implementación técnica principal.

**Resultado:**
Se contó con base suficiente para iniciar el backend sin improvisar el alcance funcional.

**Evidencia:**
Documentos actualizados en `docs/`.

---

### Punto 11 - Configuración técnica inicial Django/Docker/PostgreSQL

**Estado:** Completado.

**Descripción:**
Se configuró el backend Django inicial, entorno Docker, PostgreSQL, settings por ambiente y usuario personalizado.

**Resultado:**
Proyecto Django operativo con PostgreSQL, Docker Compose, CustomUser con email como identificador y pruebas iniciales.

**Evidencia técnica:**
Commit:

```text
b599e00 chore: configure initial Django backend
```

---

### Punto 12 - Catálogos base: unidades organizativas y tipos documentales

**Estado:** Completado.

**Descripción:**
Se implementaron los modelos base de catálogos funcionales.

**Resultado:**
Se agregaron:

* `OrganizationalUnit`
* `DocumentType`

**Evidencia técnica:**
Commit:

```text
dbe7dec feat: add base catalog models
```

---

### Punto 13 - Modelo documental base

**Estado:** Completado.

**Descripción:**
Se implementó el modelo documental base.

**Resultado:**
Se agregaron:

* `Document`
* `DocumentVersion`
* `DocumentFile`
* `DocumentStatus`

**Evidencia técnica:**
Commit:

```text
457a08c feat: add base document models
```

---

### Punto 14A - Secuencias base de codificación documental

**Estado:** Completado.

**Descripción:**
Se implementó la estructura base para secuencias de codificación documental.

**Resultado:**
Se agregó:

* `DocumentCodeSequence`

No se implementó generación automática de códigos ni correlativos activos.

**Evidencia técnica:**
Commit:

```text
f1c88b2 feat: add document code sequence model
```

---

### Punto 14B - Solicitudes documentales base

**Estado:** Completado.

**Descripción:**
Se implementó el modelo base de solicitudes documentales.

**Resultado:**
Se agregaron:

* `DocumentRequest`
* `DocumentRequestType`
* `DocumentRequestStatus`

**Evidencia técnica:**
Commit:

```text
850ce99 feat: add base document request model
```

---

### Punto 15 - Copias controladas base

**Estado:** Completado.

**Descripción:**
Se implementó la estructura base para copias controladas.

**Resultado:**
Se agregaron:

* `ControlledCopy`
* `ControlledCopyStatus`

**Evidencia técnica:**
Commit:

```text
c5cecad feat: add base controlled copy model
```

---

### Punto 16 - Constancias base / ImplementationRecord

**Estado:** Completado.

**Descripción:**
Se implementó el registro base de lectura, aceptación, interpretación o implementación documental.

**Resultado:**
Se agregaron:

* `ImplementationRecord`
* `ImplementationRecordStatus`

No se implementó todavía `ImplementationCertificate` formal.

**Evidencia técnica:**
Commit:

```text
4c00e1b feat: add base implementation record model
```

---

### Punto 17 - Auditoría base

**Estado:** Completado.

**Descripción:**
Se implementó el modelo mínimo de eventos de auditoría.

**Resultado:**
Se agregaron:

* `AuditAction`
* `AuditResult`
* `AuditEvent`

El admin de auditoría quedó como solo lectura.

**Evidencia técnica:**
Commit:

```text
7cd2811 feat: add base audit event model
```

---

### Punto 18 - Roles y permisos base

**Estado:** Completado.

**Descripción:**
Se implementaron roles base de usuario y grupos iniciales.

**Resultado:**
Se agregaron:

* `UserRole`
* `ROLE_GROUP_NAMES`
* Campo `role` en `User`
* Campo `organizational_unit` en `User`
* Campo `is_technical_user` en `User`
* Helpers de rol
* Grupos base vía migración de datos

Grupos base:

* `OYM_ADMIN`
* `OYM_ANALYST`
* `EXECUTING_UNIT`
* `READER`
* `SYSTEMS_TECH_ADMIN`
* `AUDITOR`

**Evidencia técnica:**
Commit:

```text
d51f18c feat: add base user roles
```

---

### Punto 19 - Consolidación técnica del backend base

**Estado:** Completado.

**Descripción:**
Se consolidó la operación técnica del backend mediante Makefile, README y scripts.

**Resultado:**
Se actualizaron:

* `Makefile`
* `README.md`
* Scripts en `infrastructure/scripts/`

Se agregaron comandos reproducibles para:

* Check.
* Test base.
* Healthcheck.
* Backup DB.
* Restore DB.
* Backup media.
* Deploy local backend.

**Evidencia técnica:**
Commit:

```text
0bbdb13 chore: consolidate backend technical baseline
```

---

### Punto 19B - Documentación formal del roadmap técnico MVP

**Estado:** En curso.

**Descripción:**
Se crea este documento para formalizar el roadmap técnico de la primera fase del MVP.

**Resultado esperado:**
Contar con una bitácora oficial de 25 puntos que permita controlar avance, pendientes, exclusiones y criterios de cierre de la primera fase.

**Evidencia técnica esperada:**
Archivo:

```text
docs/00_gobierno_proyecto/roadmap_tecnico_mvp.md
```

Commit esperado:

```text
docs: add technical MVP roadmap
```

---

### Punto 20 - Servicios/selectors base del núcleo documental

**Estado:** Completado.

**Descripción:**
Se implementaron servicios y selectors base para separar consultas y operaciones de negocio iniciales.

**Resultado:**
Se creó una base para evitar que la lógica futura quede dispersa en admin, vistas o APIs.

**Evidencia técnica:**
Implementación en servicios/selectors de apps principales del backend.

---

### Punto 21 - Permisos finos por acción/módulo

**Estado:** Completado.

**Descripción:**
Se agregaron helpers de permisos por módulo y acción.

**Resultado:**
Se agregaron helpers en `permissions.py` para:

* `accounts`
* `organizational_units`
* `document_types`
* `documents`
* `document_requests`
* `controlled_copies`
* `implementation_records`
* `audit`
* `reports`
* `notifications`

Cubren permisos base por rol para:

* OyM Admin.
* Analista OyM.
* Unidad Ejecutora.
* Lector.
* Sistemas Técnico.
* Auditor.

**Evidencia técnica:**
Commit:

```text
87de533 feat: add module permissions and document status transitions
```

---

### Punto 22 - Transiciones de estados documentales

**Estado:** Completado.

**Descripción:**
Se implementó la matriz de transiciones permitidas para estados documentales.

**Resultado:**
Se agregaron:

* `backend/apps/documents/workflows.py`
* Matriz explícita de transiciones permitidas para `DocumentStatus`
* `document_transition_status()` en `documents/services.py`
* Validación con `ValidationError` para transiciones no permitidas

**Evidencia técnica:**
Commit:

```text
87de533 feat: add module permissions and document status transitions
```

---

## 8. Cierre de la primera fase

### Punto 23 - Transiciones de estados de solicitudes documentales

**Estado:** Completado.

**Descripción:**
Se implementó una matriz explícita de transiciones permitidas para `DocumentRequestStatus`.

**Resultado:**

* `backend/apps/document_requests/workflows.py`.
* Servicio de transición en `document_requests/services.py`.
* Validación de transiciones permitidas y no permitidas.
* Pruebas unitarias.
* Sin aprobaciones multinivel ni workflow operativo completo.

**Evidencia:**

```text
2b5e0e7 feat: add document request status transitions
```

---

### Punto 24 - Servicios de auditoría automática controlada

**Estado:** Completado.

**Descripción:**
Se crearon servicios mínimos para registrar eventos de auditoría desde operaciones controladas del sistema.

**Resultado:**

* Creación centralizada de eventos de auditoría.
* Registro de actor, acción, resultado, objeto afectado, descripción y metadata.
* Sin auditoría automática global por middleware.
* Sin reportes ni exportación.

**Evidencia:**

```text
75c7e7f feat: add controlled automatic audit services
```

---

### Punto 25 - Carga inicial / seed de catálogos base

**Estado:** Completado.

**Descripción:**
Se creó un mecanismo controlado para cargar datos base iniciales del MVP.

**Resultado:**

* Seed de roles/grupos base.
* Seed de tipos documentales básicos validados por documentación existente.
* Seed de unidades organizativas base.
* Comando reproducible o fixture controlado.
* Sin datos productivos sensibles.
* Sin catálogos no validados.

**Evidencia:**

```text
7d11339 feat: add base catalog seed command
```

---

## 9. Exclusiones de esta fase

La primera fase técnica no incluye todavía:

* API pública o interna completa.
* Frontend.
* Vistas web definitivas.
* Visor documental.
* Bloqueo real de descarga.
* Bloqueo real de impresión.
* Bloqueo real de copia.
* Reportes Excel.
* Libro Maestro automatizado.
* Notificaciones.
* Correos automáticos.
* Firma electrónica avanzada.
* `ImplementationCertificate` formal.
* Workflows completos de aprobación.
* Aprobaciones multinivel.
* Motor completo de permisos por documento.
* Integración con Wazuh/SIEM.
* Integración con Active Directory o Microsoft 365.
* Despliegue productivo definitivo.
* Carga de documentos productivos reales.

---

## 10. Criterios para cerrar la primera fase

La primera fase técnica podrá considerarse cerrada cuando:

1. Los 25 puntos estén completados.
2. La suite base de pruebas pase correctamente.
3. No existan migraciones pendientes.
4. El healthcheck responda `200`.
5. El working tree esté limpio.
6. `develop` esté alineado con `origin/develop`.
7. `main` permanezca como rama estable hasta aprobación explícita.
8. El README refleje el estado real del backend.
9. Este roadmap refleje el estado real de avance.
10. No existan cambios funcionales fuera de alcance sin documentar.
11. Los pendientes para fases posteriores estén claramente identificados.

Comandos mínimos esperados de cierre:

```bash
git status
python -m compileall backend
make check
docker compose exec backend python manage.py makemigrations --check --dry-run
docker compose exec backend python manage.py migrate
make test-base
make healthcheck
```

---

## 11. Relación con fases posteriores

Una vez cerrada la primera fase técnica, el proyecto podrá avanzar a fases posteriores.

### Fase 2 - Capa de acceso

Posibles decisiones:

* API interna con Django REST Framework.
* Vistas web con Django templates.
* Enfoque híbrido.

Esta decisión debe tomarse antes de construir pantallas o endpoints definitivos.

#### F2-P01 - Decisión técnica de capa de acceso

**Estado:** Completado.

**Decisión:** Enfoque híbrido controlado.

El MVP usará Django templates como interfaz principal y Django REST Framework solo para API interna cuando una pantalla, componente o integración lo justifique.

No se construirá una API pública ni una SPA React completa como primera interfaz del MVP.

**Evidencia:**

```text
docs/00_gobierno_proyecto/decisiones_arquitectura.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
docs/04_diseno_tecnico/api_spec.md
```

#### F2-P02 - Estructura base de URLs, vistas y capa de acceso

**Estado:** Completado.

**Resultado:**

* Rutas principales para login, logout, dashboard y healthcheck.
* Prefijo funcional `/app/` con vistas base por modulo.
* Indice reservado `/api/v1/` sin endpoints funcionales.
* Templates base para interfaz interna con sesion Django.
* Pruebas de autenticacion, permisos base y rutas iniciales.

**Evidencia:**

```text
backend/config/urls.py
backend/config/app_urls.py
backend/config/access.py
backend/config/navigation.py
backend/templates/
backend/apps/*/views.py
backend/apps/*/urls.py
backend/apps/accounts/tests/test_access_urls.py
```

#### F2-P03 - Login, logout y redirección por rol

**Estado:** Completado.

**Resultado:**

* Login visual basado en correo institucional.
* Redirección posterior al login según rol del usuario.
* Respeto de `next` cuando la URL de destino es segura.
* Logout por POST con pantalla visual de sesión cerrada.
* Redirección de raíz `/` según autenticación y rol.
* Pruebas de login, logout, `next` y redirecciones por rol.

**Evidencia:**

```text
backend/apps/accounts/redirects.py
backend/apps/accounts/views.py
backend/config/urls.py
backend/config/views.py
backend/templates/accounts/login.html
backend/templates/accounts/logged_out.html
backend/apps/accounts/tests/test_access_urls.py
```

#### F2-P04 - Dashboard base por rol

**Estado:** Completado.

**Resultado:**

* Dashboard protegido por login.
* Contenido minimo diferenciado por rol.
* Accesos principales por perfil usando rutas ya existentes.
* Sin metricas reales complejas.
* Sin modelos nuevos ni migraciones.
* Sin reportes ni frontend avanzado.
* Pruebas de contenido por rol.

**Evidencia:**

```text
backend/apps/accounts/dashboard.py
backend/config/views.py
backend/templates/app/dashboard.html
backend/apps/accounts/tests/test_access_urls.py
```

#### F2-P05 - Catálogos: vistas de unidades organizativas y tipos documentales

**Estado:** Completado.

**Resultado:**

* Listado de unidades ejecutoras.
* Detalle básico de unidad ejecutora.
* Listado de tipos documentales.
* Detalle básico de tipo documental.
* Acceso protegido por login.
* Permisos por rol usando helpers existentes.
* Sin crear, editar ni eliminar desde vistas funcionales.
* Sin APIs, modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/organizational_units/views.py
backend/apps/organizational_units/urls.py
backend/apps/organizational_units/tests/test_views.py
backend/apps/document_types/views.py
backend/apps/document_types/urls.py
backend/apps/document_types/tests/test_views.py
backend/templates/catalogs/
```

#### F2-P06 - Documentos: listado, detalle y consulta base

**Estado:** Completado.

**Resultado esperado:**

* Listado de documentos.
* Detalle básico de documento.
* Visualización de versiones asociadas.
* Visualización de archivos asociados como metadatos.
* Acceso protegido por login.
* Permisos por rol usando helpers existentes.
* Sin carga, descarga ni visor documental.
* Sin cambios de estado ni aprobaciones desde vistas.

**Evidencia:**

```text
backend/apps/documents/views.py
backend/apps/documents/urls.py
backend/apps/documents/tests/test_views.py
backend/templates/documents/
```

#### F2-P07 - Solicitudes documentales: creación y consulta base

**Estado:** Completado.

**Resultado:**

* Listado de solicitudes documentales.
* Detalle básico de solicitud.
* Formulario simple para crear solicitud.
* Acceso protegido por login.
* Permisos por rol usando helpers existentes.
* Unidad ejecutora puede crear solicitudes.
* OyM puede consultar todas las solicitudes.
* Usuarios no OyM con acceso solo consultan solicitudes propias.
* Sin workflow completo, aprobacion, rechazo, notificaciones ni modelos nuevos.

**Evidencia:**

```text
backend/apps/document_requests/forms.py
backend/apps/document_requests/views.py
backend/apps/document_requests/urls.py
backend/apps/document_requests/tests/test_views.py
backend/templates/document_requests/
```

#### F2-P08 - Copias controladas: consulta base

**Estado:** Completado.

**Resultado:**

* Listado de copias controladas.
* Detalle básico de copia controlada.
* Acceso protegido por login.
* Permisos por rol usando helpers existentes.
* OyM puede ver todas las copias controladas.
* Unidad o usuario destinatario puede consultar sus copias aplicables.
* Sistemas Técnico y Auditor permanecen sin acceso si el helper no les otorga permiso.
* Sin creación, edición, retiro, workflow de entrega, constancias, notificaciones ni reportes desde vistas.

**Evidencia:**

```text
backend/apps/controlled_copies/permissions.py
backend/apps/controlled_copies/views.py
backend/apps/controlled_copies/urls.py
backend/apps/controlled_copies/tests/test_permissions.py
backend/apps/controlled_copies/tests/test_views.py
backend/templates/controlled_copies/
```

#### F2-P09 - Implementation records: consulta y registro base

**Estado:** Completado.

**Resultado:**

* Listado de registros de implementacion.
* Detalle basico de registro.
* Formulario simple para crear registro propio pendiente.
* Acceso protegido por login.
* Permisos por rol usando helpers existentes.
* OyM puede consultar todos los registros.
* Usuario autenticado puede consultar sus propios registros.
* Sin `ImplementationCertificate`, firma formal, numeracion de constancias, PDF, notificaciones ni reportes.
* Sin modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/implementation_records/forms.py
backend/apps/implementation_records/views.py
backend/apps/implementation_records/urls.py
backend/apps/implementation_records/tests/test_views.py
backend/templates/implementation_records/
```

#### F2-P10 - Auditoría: consulta restringida base

**Estado:** Completado.

**Resultado:**

* Listado de eventos de auditoria.
* Detalle basico de evento.
* Acceso protegido por login.
* Acceso restringido con helpers existentes.
* OyM Admin, Analista OyM, Auditor y Sistemas Tecnico pueden consultar segun permisos actuales.
* Solo lectura.
* Sin exportacion, reportes, filtros avanzados, modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/audit/permissions.py
backend/apps/audit/views.py
backend/apps/audit/urls.py
backend/apps/audit/tests/test_permissions.py
backend/apps/audit/tests/test_views.py
backend/templates/audit/
```

#### F2-P11 - Aplicación transversal de permisos por rol en vistas

**Estado:** Completado.

**Resultado:**

* Revision de vistas creadas en Fase 2.
* Confirmacion de login requerido en rutas internas.
* Confirmacion de permisos por rol mediante helpers existentes.
* Confirmacion de respuestas 403 donde corresponde.
* Centralizacion de navegacion de modulo en `ModuleAccessMixin`.
* Pruebas transversales por rol sobre rutas principales de Fase 2.
* Sin modelos nuevos, migraciones, APIs, reportes ni frontend avanzado.

**Evidencia:**

```text
backend/config/access.py
backend/apps/accounts/tests/test_phase2_permissions.py
```

#### F2-P12 - Pruebas integradas de capa de acceso

**Estado:** Completado.

**Resultado:**

* Refuerzo de pruebas integradas de navegacion de Fase 2.
* Validacion de rutas principales por rol.
* Validacion de redirects a login para usuarios anonimos.
* Validacion de respuestas 403 segun permisos existentes.
* Validacion de templates esperados para paginas principales.
* Validacion de navegacion visible por rol en dashboard.
* Confirmacion de ausencia de migraciones pendientes.
* Sin modelos nuevos, APIs, nuevas funcionalidades ni cambios de reglas funcionales.

**Evidencia:**

```text
backend/apps/accounts/tests/test_phase2_permissions.py
```

#### F2-P13 - Documentación técnica de cierre de Fase 2

**Estado:** Completado.

**Resultado:**

* Actualizacion del roadmap tecnico MVP con cierre documental de Fase 2.
* Actualizacion de arquitectura de aplicacion con rutas actuales.
* Documentacion de permisos aplicados por modulo y rol.
* Documentacion de validaciones tecnicas de Fase 2.
* Documentacion de pendientes y limites para Fase 3.
* Sin codigo nuevo, modelos, migraciones, APIs ni nuevas reglas funcionales.

**Evidencia:**

```text
docs/00_gobierno_proyecto/roadmap_tecnico_mvp.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

---

### Fase 3 - Visor documental y restricciones de consulta

**Estado:** Iniciada formalmente.

Objetivo futuro:

* Visualización controlada de documentos.
* Restricciones de descarga.
* Restricciones de impresión.
* Restricciones de copia.
* Trazabilidad de acceso.

Debe definirse con cuidado porque algunas restricciones dependen del navegador, del formato documental y de políticas técnicas realistas.

#### F3-P01 - Definición técnica del visor documental

**Estado:** Completado.

**Resultado:**

* Definicion documental de la arquitectura tecnica del visor documental.
* Definicion de entrega controlada de archivos sin rutas directas.
* Priorizacion de PDF como formato inicial de visualizacion.
* Registro explicito de restricciones viables y no garantizables.
* Definicion de trazabilidad minima por usuario, documento y version.
* Identificacion de riesgos tecnicos reales y controles compensatorios.
* Pendientes definidos para F3-P02.
* Sin implementacion funcional, codigo, modelos, migraciones, APIs, templates ni cambios de infraestructura.

**Evidencia:**

```text
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P02 - Servicio de entrega controlada de archivos

**Estado:** Completado.

**Resultado:**

* Vista protegida por login para entregar archivos documentales controlados.
* Validacion de permisos por usuario, documento, version y archivo.
* Entrega inicial limitada a PDF.
* Respuesta `403` para usuarios sin permiso.
* Respuesta `404` cuando documento, version o archivo no existen.
* Auditoria minima para accesos permitidos y denegados.
* Pruebas automatizadas para flujo permitido, denegado y ausencia de URL directa.
* Sin modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/documents/views.py
backend/apps/documents/urls.py
backend/apps/documents/permissions.py
backend/apps/documents/selectors.py
backend/apps/documents/services.py
backend/apps/documents/tests/test_views.py
```

#### F3-P03 - Validación de acceso por usuario/unidad/documento

**Estado:** Completado.

**Resultado:**

* Fortalecimiento del helper de permiso fino por documento, version y archivo.
* Reglas explicitas para OyM, Sistemas, Auditor, Unidad Ejecutora y Usuario Lector.
* Validacion de acceso por unidad organizativa cuando existe relacion aplicable.
* Validacion de relacion directa por registro de implementacion o copia controlada.
* Mantenimiento de `403` para usuario autenticado sin permiso.
* Mantenimiento de `404` para documento, version, archivo o archivo fisico inexistente.
* Pruebas automatizadas por rol, unidad y relacion directa.
* Sin modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/documents/permissions.py
backend/apps/documents/tests/test_views.py
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P04 - Vista de consulta documental controlada

**Estado:** Completado.

**Resultado:**

* Vista y template base del visor documental.
* Integracion con la ruta protegida de entrega controlada de PDF creada en F3-P02.
* Visualizacion inline mediante `iframe`.
* Metadatos basicos de documento, version y archivo.
* Login obligatorio.
* Validacion de permisos con reglas existentes de F3-P03.
* Mensaje controlado para acceso denegado o archivo no disponible.
* Navegacion desde detalle documental hacia visor cuando aplica.
* Pruebas automatizadas de acceso permitido, denegado, login requerido y archivo no disponible.
* Sin modelos nuevos, migraciones, APIs, PDF.js custom, marcas de agua, conversion Office ni bloqueo avanzado de descarga o impresion.

**Evidencia:**

```text
backend/apps/documents/views.py
backend/apps/documents/urls.py
backend/templates/documents/document_viewer.html
backend/templates/documents/document_detail.html
backend/apps/documents/tests/test_views.py
```

#### F3-P05 - Registro de acceso a documentos

**Estado:** Completado.

**Resultado:**

* Revision y normalizacion de eventos `DOCUMENT_VIEWED`.
* Confirmacion de registro de acceso permitido, denegado y fallido por archivo no disponible.
* Trazabilidad sobre `AuditEvent` con usuario, documento, version, archivo, IP, user agent, accion, resultado y fecha/hora.
* Metadata documental normalizada en `after_data`.
* Descripciones estandarizadas para visor documental.
* Pruebas especificas de evidencia de trazabilidad.
* Sin modelo `DocumentAccessLog`, sin modelos nuevos y sin migraciones.

**Evidencia:**

```text
backend/apps/documents/services.py
backend/apps/documents/views.py
backend/apps/documents/tests/test_views.py
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P06 - Restricción de descarga según viabilidad técnica

**Estado:** Completado.

**Resultado:**

* Confirmacion de entrega PDF con `Content-Disposition: inline`.
* Confirmacion de ausencia de `Content-Disposition: attachment`.
* Mantenimiento de `Cache-Control: no-store`.
* Entrega en iframe limitada a mismo origen.
* Fragmento de visor nativo para reducir exposicion de toolbar cuando el navegador lo soporte.
* Controles HTML/JS razonables para desalentar menu contextual y atajos de guardar, imprimir o copiar desde la pagina del visor.
* Confirmacion de que no se expone URL fisica del archivo ni enlaces directos de descarga en la interfaz.
* Documentacion explicita de que el navegador puede seguir ofreciendo opciones nativas de guardar o imprimir.
* Pruebas automatizadas sobre headers y ausencia de enlaces directos.
* Sin modelos nuevos, migraciones, PDF.js custom, marcas de agua ni bloqueo avanzado de descarga o impresion.

**Evidencia:**

```text
backend/apps/documents/views.py
backend/templates/documents/document_viewer.html
backend/apps/documents/tests/test_views.py
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P07 - Restricción de impresión según viabilidad técnica

**Estado:** Completado.

**Resultado:**

* Mantenimiento de controles JS razonables para desalentar `Ctrl/Cmd + P`.
* Reglas CSS `@media print` para ocultar visualmente el iframe del visor al imprimir la pagina.
* Mensaje impreso: `La impresion de documentos controlados no esta permitida desde el visor.`
* Confirmacion de ausencia de botones o enlaces de impresion en la interfaz.
* Documentacion explicita de que no se puede impedir al 100% la impresion desde visor nativo, navegador o sistema operativo.
* Mantenimiento de trazabilidad documental existente.
* Pruebas automatizadas sobre ausencia de controles de impresion y presencia de CSS print/mensaje.
* Sin modelos nuevos, migraciones, PDF.js custom, marcas de agua ni bloqueo avanzado de impresion.

**Evidencia:**

```text
backend/templates/documents/document_viewer.html
backend/static/css/app.css
backend/apps/documents/tests/test_views.py
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P08 - Marca de agua o identificación de usuario

**Estado:** Completado.

**Resultado:**

* Marca de agua visual en la pagina del visor documental.
* Identificacion visible de usuario autenticado, unidad cuando aplica, documento, version y fecha/hora.
* Marca de agua superpuesta al area del visor sin alterar la entrega PDF controlada.
* No se modifica el archivo PDF original.
* No se generan copias fisicas ni archivos derivados del PDF.
* No se agregan modelos, migraciones, PDF.js custom ni librerias externas.
* Pruebas automatizadas de presencia de marca de agua y estilos de overlay.
* Documentacion explicita de que la marca de agua es control disuasivo y evidencia visual, no proteccion absoluta frente a captura, fotografia externa o herramientas del sistema operativo.

**Evidencia:**

```text
backend/templates/documents/document_viewer.html
backend/static/css/app.css
backend/apps/documents/tests/test_views.py
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P09 - Pruebas de seguridad del visor

**Estado:** Completado.

**Resultado:**

* Revision y fortalecimiento de pruebas automatizadas del visor documental.
* Cobertura de login requerido, acceso permitido, acceso denegado y rutas inexistentes.
* Cobertura de documento inexistente, version inexistente, archivo inexistente, archivo inactivo y archivo fisico no disponible.
* Cobertura de archivo no soportado para entrega controlada inicial limitada a PDF.
* Validacion de ausencia de rutas fisicas o `MEDIA_URL` en interfaces de consulta.
* Validacion de headers de seguridad: `Cache-Control: no-store`, `Content-Disposition: inline`, `X-Frame-Options`, `X-Content-Type-Options` y `Content-Security-Policy`.
* Validacion de iframe con `sandbox` sin `allow-downloads`.
* Validacion de ausencia de botones de descarga e impresion, presencia de mensaje de impresion restringida y marca de agua.
* Validacion de auditoria `success`, `denied` y `failure`.
* Sin modelos nuevos, migraciones, PDF.js custom ni cambios funcionales.

**Evidencia:**

```text
backend/apps/documents/tests/test_views.py
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
```

#### F3-P10 - Documentación de limitaciones reales del visor

**Estado:** Completado.

**Resultado:**

* Consolidacion documental de controles implementados en F3-P01 a F3-P09.
* Documentacion explicita de limitaciones reales del visor documental.
* Registro de riesgos residuales: captura de pantalla, fotografia externa, impresion desde visor nativo, descarga con herramientas avanzadas, OCR y exposicion por mala configuracion de Nginx, `MEDIA_URL` o storage.
* Consolidacion de controles compensatorios: permisos por rol/unidad/relacion documental, entrega controlada, auditoria `DOCUMENT_VIEWED`, headers de cache, entrega `inline`, CSP, iframe sandbox, reduccion de toolbar, marca de agua visual y politica interna de uso.
* Confirmacion documental de que el PDF original no se modifica y no se generan copias derivadas.
* Registro de que archivos Office quedan pendientes de conversion o evaluacion tecnica posterior.
* Criterios de aceptacion de cierre de Fase 3 documentados.
* Sin codigo nuevo, modelos, migraciones, PDF.js custom ni cambios funcionales.

**Evidencia:**

```text
docs/06_fase_3_visor_documental/definicion_tecnica_visor_documental.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

---

### Fase 4 - Reportes y Libro Maestro

Objetivo:

Construir reportes operativos y el Libro Maestro de Control Documental para Organización y Métodos, respetando permisos, trazabilidad y exportación controlada.

Puntos propuestos:

```text
F4-P01 -> Definición técnica y funcional de reportes y Libro Maestro
F4-P02 -> Selectors base de reportes
F4-P03 -> Vista de Libro Maestro documental
F4-P04 -> Filtros base del Libro Maestro
F4-P05 -> Reporte mensual documental
F4-P06 -> Reportes de solicitudes documentales
F4-P07 -> Reportes de copias controladas
F4-P08 -> Reportes de implementación
F4-P09 -> Exportación CSV/Excel base
F4-P10 -> Auditoría de consulta/exportación de reportes
F4-P11 -> Pruebas y cierre documental de Fase 4
```

#### F4-P01 - Definición técnica y funcional de reportes y Libro Maestro

**Estado:** Completado.

**Resultado:**

* Inicio formal de Fase 4.
* Definición del objetivo funcional y técnico de reportes y Libro Maestro.
* Alcance del Libro Maestro documental.
* Reportes incluidos en el MVP según reglas de negocio de OyM.
* Filtros esperados por tipo documental, unidad, estado, vigencia y fechas.
* Fuentes de datos existentes para reportes.
* Permisos por rol, manteniendo reportes exclusivos para OyM.
* Decisión de exportación progresiva: CSV como salida técnica simple inicial y Excel como objetivo MVP con dependencia justificada.
* Auditoría esperada con `AuditAction.REPORT_GENERATED`.
* Riesgos, límites y puntos F4-P01 a F4-P11 documentados.
* Sin código nuevo, templates, vistas, URLs, modelos ni migraciones.

**Evidencia:**

```text
docs/07_fase_4_reportes_libro_maestro/definicion_reportes_libro_maestro.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

#### F4-P02 - Selectors base para reportes documentales

**Estado:** Completado.

**Resultado:**

* Capa base de selectors centralizada para reportes y Libro Maestro.
* Selectors para Libro Maestro documental, reporte mensual, copias controladas e implementacion.
* Filtros preparativos para tipo documental, unidad organizativa, estado, vigencia, fechas, codigo, responsable y version.
* Querysets de solo lectura con uso razonable de `select_related`.
* Sin dependencia de `request`, sin exportacion y sin logica de presentacion.
* Pruebas unitarias para filtros base, relaciones esperadas y rango de fechas.
* Sin modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/reports/selectors.py
backend/apps/reports/tests/test_selectors.py
docs/07_fase_4_reportes_libro_maestro/definicion_reportes_libro_maestro.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

#### F4-P03 - Vista de Libro Maestro documental

**Estado:** Completado.

**Resultado:**

* Vista web base de solo lectura para el Libro Maestro documental.
* Ruta interna protegida `/app/reports/master-book/`.
* Reutilizacion directa de `get_master_book_queryset`.
* Acceso restringido a roles OyM mediante `can_view_reports`.
* Tabla con codigo documental, titulo, tipo documental, unidad responsable, estado, version vigente o actual, fecha de emision/creacion y fecha de vigencia.
* Sin exportaciones, filtros avanzados, exposicion de archivos, modelos nuevos ni migraciones.
* Pruebas de login requerido, acceso autorizado, acceso denegado, render de documentos y uso del selector.

**Evidencia:**

```text
backend/apps/reports/views.py
backend/apps/reports/urls.py
backend/templates/reports/master_book.html
backend/apps/reports/tests/test_views.py
docs/07_fase_4_reportes_libro_maestro/definicion_reportes_libro_maestro.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

#### F4-P04 - Filtros de Libro Maestro

**Estado:** Completado.

**Resultado:**

* Filtros GET agregados a `/app/reports/master-book/`.
* Validacion simple de filtros mediante formulario Django de solo lectura.
* Reutilizacion de `get_master_book_queryset` sin duplicar consultas en la vista.
* Filtros por tipo documental, unidad responsable, estado documental, vigencia, codigo documental, titulo y rango de fecha de creacion.
* La vigencia se interpreta con los grupos de estado ya definidos en el selector; no recalcula vencimientos ni inventa reglas de corte.
* Filtros invalidos no rompen la vista y devuelven el Libro Maestro sin aplicar criterios invalidos.
* Filtros seleccionados se conservan en pantalla.
* Sin exportaciones, modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/reports/forms.py
backend/apps/reports/selectors.py
backend/apps/reports/views.py
backend/templates/reports/master_book.html
backend/apps/reports/tests/test_views.py
docs/07_fase_4_reportes_libro_maestro/definicion_reportes_libro_maestro.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

#### F4-P05 - Reporte mensual documental

**Estado:** Completado.

**Resultado:**

* Vista base del reporte mensual documental en `/app/reports/monthly-documents/`.
* Acceso protegido por login y restringido a OyM mediante `can_view_reports`.
* Reutilizacion de `get_monthly_document_report_queryset`.
* Periodo por defecto basado en mes y ano actuales.
* Filtros GET por mes, ano, tipo documental, unidad responsable y estado.
* Tabla de actividad con codigo documental, titulo, tipo documental, unidad responsable, estado, version, fecha de creacion/emision y ultima actualizacion del documento.
* Resumen basico con total del periodo, totales por estado y totales por tipo documental.
* El periodo mensual usa `DocumentVersion.published_at` como campo real de actividad publicada.
* Sin exportaciones, modelos nuevos ni migraciones.

**Evidencia:**

```text
backend/apps/reports/forms.py
backend/apps/reports/views.py
backend/apps/reports/urls.py
backend/templates/reports/monthly_documents.html
backend/apps/reports/tests/test_views.py
docs/07_fase_4_reportes_libro_maestro/definicion_reportes_libro_maestro.md
docs/04_diseno_tecnico/arquitectura_aplicacion.md
```

---

### Fase 5 - Notificaciones

Objetivo futuro:

* Notificaciones internas.
* Alertas por documentos pendientes de lectura o implementación.
* Alertas por solicitudes documentales.
* Posible integración con correo.

---

### Fase 6 - Constancias formales

Objetivo futuro:

* `ImplementationCertificate`.
* Numeración de constancias.
* Formato formal validado por OyM.
* Evidencia imprimible o exportable si OyM lo requiere.

---

### Fase 7 - Endurecimiento y despliegue productivo

Objetivo futuro:

* Seguridad productiva.
* Variables de entorno productivas.
* Backup formal.
* Monitoreo.
* Logs.
* Revisión de permisos.
* Hardening Docker/Linux.
* Despliegue en infraestructura definida por Sistemas.

---

## 12. Estado resumido

Resumen del estado al cierre de este documento:

```text
Puntos principales de la primera fase: 25
Punto documental intercalado: 19B
Puntos completados: 01 al 22
Puntos pendientes: 23, 24 y 25
Rama activa de trabajo: develop
Rama estable: main
```

Este roadmap debe mantenerse actualizado al completar nuevos puntos de fases posteriores.
