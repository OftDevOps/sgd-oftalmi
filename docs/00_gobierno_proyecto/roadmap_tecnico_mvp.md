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
| Punto 19B | Documentación formal del roadmap técnico MVP                           | En curso   |
| Punto 20  | Servicios/selectors base del núcleo documental                         | Completado |
| Punto 21  | Permisos finos por acción/módulo                                       | Completado |
| Punto 22  | Transiciones de estados documentales                                   | Completado |
| Punto 23  | Transiciones de estados de solicitudes documentales                    | Pendiente  |
| Punto 24  | Servicios de auditoría automática controlada                           | Pendiente  |
| Punto 25  | Carga inicial / seed de catálogos base                                 | Pendiente  |

---

## 6. Estado actual de avance

Al momento de crear este roadmap, el desarrollo técnico ha avanzado hasta el **Punto 22**.

Último avance técnico registrado:

```text
Punto 21 -> Permisos finos por acción/módulo
Punto 22 -> Transiciones de estados documentales
```

Último commit técnico conocido en `develop`:

```text
87de533 feat: add module permissions and document status transitions
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

## 8. Puntos pendientes de la primera fase

### Punto 23 - Transiciones de estados de solicitudes documentales

**Estado:** Pendiente.

**Descripción:**
Implementar una matriz explícita de transiciones permitidas para `DocumentRequestStatus`.

**Resultado esperado:**

* Crear `backend/apps/document_requests/workflows.py`.
* Agregar servicio de transición en `document_requests/services.py`.
* Validar transiciones permitidas y no permitidas.
* Agregar pruebas unitarias.
* No implementar todavía aprobaciones multinivel ni workflow operativo completo.

---

### Punto 24 - Servicios de auditoría automática controlada

**Estado:** Pendiente.

**Descripción:**
Crear servicios mínimos para registrar eventos de auditoría desde operaciones controladas del sistema.

**Resultado esperado:**

* Centralizar creación de eventos de auditoría.
* Permitir registrar actor, acción, resultado, objeto afectado, descripción y metadata.
* No implementar todavía auditoría automática global por middleware.
* No implementar reportes ni exportación.

---

### Punto 25 - Carga inicial / seed de catálogos base

**Estado:** Pendiente.

**Descripción:**
Crear mecanismo controlado para cargar datos base iniciales del MVP.

**Resultado esperado:**

* Seed de roles/grupos si aplica.
* Seed de tipos documentales básicos si OyM los valida.
* Seed de unidades organizativas si OyM/Sistemas lo valida.
* Comando reproducible o fixture controlado.
* No cargar datos productivos sensibles.
* No inventar catálogos no validados.

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

---

### Fase 3 - Visor documental y restricciones de consulta

Objetivo futuro:

* Visualización controlada de documentos.
* Restricciones de descarga.
* Restricciones de impresión.
* Restricciones de copia.
* Trazabilidad de acceso.

Debe definirse con cuidado porque algunas restricciones dependen del navegador, del formato documental y de políticas técnicas realistas.

---

### Fase 4 - Reportes y Libro Maestro

Objetivo futuro:

* Reportes Excel.
* Libro Maestro documental.
* Reporte mensual.
* Reportes de implementación.
* Reportes de copias controladas.
* Reportes de auditoría.

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

Este roadmap debe actualizarse al completar los puntos 23, 24 y 25.

