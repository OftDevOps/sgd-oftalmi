# Datos Demo y Usuarios de Prueba - Piloto Controlado SGD-OFTALMI

## 1. Objetivo del set demo

Definir el set minimo de usuarios, roles, unidades, documentos, versiones, archivos PDF, copias controladas, registros de implementacion, reportes y auditoria requerido para ejecutar un piloto tecnico controlado del SGD-OFTALMI.

Este documento no crea usuarios, no carga datos, no crea fixtures y no inicia el piloto. Solo define los datos ficticios que deberan prepararse en un punto posterior autorizado.

## 2. Principios

El set demo debe cumplir estos principios:

* Datos ficticios: nombres, codigos, correos, documentos y archivos deben ser de prueba.
* Sin informacion productiva: no se deben cargar documentos reales, respaldos reales ni informacion sensible.
* Trazabilidad verificable: cada escenario debe permitir verificar auditoria, permisos, filtros y resultados.
* Cobertura por rol: cada rol relevante debe tener al menos un escenario permitido y uno denegado cuando aplique.
* Cobertura por flujo documental: el set debe cubrir visor, solicitudes, copias controladas, registros de implementacion, reportes y exportacion CSV.
* Reversibilidad: los datos deben poder eliminarse o restaurarse desde respaldo del ambiente piloto.

## 3. Usuarios demo requeridos

Los usuarios se definen con correos de dominio `.test` para evitar uso accidental de cuentas reales.

| Codigo demo | Email demo | Rol real esperado | Unidad demo | Estado | Proposito |
| --- | --- | --- | --- | --- | --- |
| `USR-OYM-ADM` | `oym.admin.demo@oftalmi.test` | `oym_admin` | `OYM` | Activo | Validar administracion funcional, reportes, auditoria funcional y acceso documental OyM. |
| `USR-OYM-ANA` | `oym.analista.demo@oftalmi.test` | `oym_analyst` | `OYM` | Activo | Validar gestion operativa OyM, reportes, Libro Maestro y solicitudes. |
| `USR-UE-PROD` | `unidad.produccion.demo@oftalmi.test` | `executing_unit` | `PROD` | Activo | Validar creacion de solicitudes y consulta por unidad ejecutora. |
| `USR-LECT-PROD` | `lector.produccion.demo@oftalmi.test` | `reader` | `PROD` | Activo | Validar consulta controlada por copia o registro de implementacion. |
| `USR-AUD` | `auditor.demo@oftalmi.test` | `auditor` | `OYM` | Activo | Validar acceso restringido a auditoria, sin acceso a reportes ni visor documental. |
| `USR-SIS` | `sistemas.demo@oftalmi.test` | `systems_tech_admin` | `SIS` | Activo | Validar soporte tecnico, usuarios, auditoria tecnica y restricciones funcionales. |
| `USR-SIN-PERM` | `sin.permiso.demo@oftalmi.test` | `reader` | `ADMIN` | Activo | Validar denegacion por ausencia de relacion documental, reportes y auditoria. |

Notas:

* `USR-SIN-PERM` no debe tener copia controlada, registro de implementacion ni relacion documental con los documentos demo.
* No se deben crear superusuarios reales para el piloto salvo autorizacion tecnica separada.
* La contrasena demo queda fuera de este documento y debe gestionarse fuera del repositorio.

## 4. Unidades demo

| Codigo | Nombre demo | Uso |
| --- | --- | --- |
| `OYM` | Organizacion y Metodos Demo | Dueño funcional del piloto, reportes y administracion documental. |
| `PROD` | Produccion Demo | Unidad ejecutora principal para copias e implementacion. |
| `RRHH` | Recursos Humanos Demo | Unidad secundaria para validar filtros por unidad. |
| `SIS` | Sistemas Demo | Unidad tecnica sin propiedad funcional sobre reglas OyM. |
| `ADMIN` | Administracion Demo | Unidad para usuario sin relacion documental. |

Todas las unidades deben estar activas. No se deben usar unidades reales con informacion productiva.

## 5. Tipos documentales demo

| Codigo | Nombre demo | Uso |
| --- | --- | --- |
| `PROC` | Procedimiento Demo | Documentos normativos de proceso. |
| `INST` | Instructivo Demo | Documentos de instrucciones operativas. |
| `FORM` | Formato Demo | Formatos controlados. |
| `MAN` | Manual Demo | Manuales internos. |

Todos los tipos documentales deben estar activos. La codificacion es demo y no reemplaza codigos aprobados por Organizacion y Metodos.

## 6. Documentos demo

| Codigo documental | Titulo demo | Tipo | Unidad responsable | Estado | Proposito |
| --- | --- | --- | --- | --- | --- |
| `PROC-OYM-DEMO-001` | Procedimiento demo de gestion documental | `PROC` | `OYM` | `active` | Documento principal para visor, Libro Maestro y reportes. |
| `INST-PROD-DEMO-001` | Instructivo demo de produccion | `INST` | `PROD` | `published` | Validar unidad ejecutora, copia controlada activa y reporte mensual. |
| `FORM-RRHH-DEMO-001` | Formato demo de induccion | `FORM` | `RRHH` | `under_review` | Validar filtros por estado y unidad sin visor final. |
| `MAN-OYM-DEMO-001` | Manual demo obsoleto | `MAN` | `OYM` | `obsolete` | Validar filtros de obsolescencia y no consulta por usuario lector. |
| `PROC-PROD-DEMO-002` | Procedimiento demo sin relacion lector | `PROC` | `PROD` | `active` | Validar 403 para `USR-SIN-PERM` en visor documental. |

## 7. Versiones demo

| Documento | Version | Estado version | Fechas esperadas | Proposito |
| --- | --- | --- | --- | --- |
| `PROC-OYM-DEMO-001` | `1.0` | `active` | `issue_date`, `effective_date`, `published_at` dentro del periodo piloto | Version vigente con PDF activo. |
| `INST-PROD-DEMO-001` | `1.0` | `published` | `published_at` dentro del mes piloto | Reporte mensual y copia controlada entregada. |
| `FORM-RRHH-DEMO-001` | `0.1` | `under_review` | `issue_date` opcional, sin `published_at` | Filtro por estado en Libro Maestro. |
| `MAN-OYM-DEMO-001` | `1.0` | `obsolete` | `obsolete_at` informado | Validar documento obsoleto y copia retirada. |
| `PROC-PROD-DEMO-002` | `1.0` | `active` | `effective_date` informada | Validar denegacion a usuario sin relacion. |

El campo `current_version` del documento debe apuntar a la version demo vigente o actual definida para cada caso.

## 8. Archivos PDF demo requeridos

| Codigo archivo | Documento/version | Nombre sugerido | Content type | Estado | Proposito |
| --- | --- | --- | --- | --- | --- |
| `PDF-OYM-001` | `PROC-OYM-DEMO-001` v`1.0` | `proc-oym-demo-001-v1.pdf` | `application/pdf` | Activo | Visor permitido para OyM y lector asignado. |
| `PDF-PROD-001` | `INST-PROD-DEMO-001` v`1.0` | `inst-prod-demo-001-v1.pdf` | `application/pdf` | Activo | Copia controlada y reporte mensual. |
| `PDF-RRHH-001` | `FORM-RRHH-DEMO-001` v`0.1` | `form-rrhh-demo-001-v01.pdf` | `application/pdf` | Inactivo | Validar archivo no disponible o no visible. |
| `PDF-OBS-001` | `MAN-OYM-DEMO-001` v`1.0` | `man-oym-demo-001-v1.pdf` | `application/pdf` | Activo | Validar obsolescencia bajo roles OyM. |
| `PDF-PROD-002` | `PROC-PROD-DEMO-002` v`1.0` | `proc-prod-demo-002-v1.pdf` | `application/pdf` | Activo | Validar acceso denegado para usuario sin relacion. |

Los archivos deben ser PDFs ficticios sin contenido productivo. No se deben versionar en el repositorio si contienen documentos generados para prueba.

## 9. Copias controladas demo

| Copia | Documento/version | Numero | Unidad destinataria | Usuario destinatario | Estado | Fechas | Proposito |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CC-001` | `PROC-OYM-DEMO-001` v`1.0` | `C-001` | `PROD` | `USR-LECT-PROD` | `active` | `delivered_at` dentro del piloto | Permitir visor al lector por relacion de copia. |
| `CC-002` | `INST-PROD-DEMO-001` v`1.0` | `C-002` | `PROD` | `USR-UE-PROD` | `delivered` | `delivered_at` dentro del mes piloto | Validar reporte de copias por unidad y estado. |
| `CC-003` | `MAN-OYM-DEMO-001` v`1.0` | `C-003` | `RRHH` | Sin usuario directo | `retired` | `delivered_at` y `retired_at` informados | Validar copias retiradas. |
| `CC-004` | `PROC-PROD-DEMO-002` v`1.0` | `C-004` | `RRHH` | Sin usuario directo | `registered` | Sin `delivered_at` | Validar copia registrada sin habilitar al usuario sin permiso. |

## 10. Registros de implementacion/lectura demo

| Registro | Usuario | Documento/version | Estado | Fechas esperadas | Proposito |
| --- | --- | --- | --- | --- | --- |
| `IR-001` | `USR-LECT-PROD` | `PROC-OYM-DEMO-001` v`1.0` | `pending` | `assigned_at` informado | Pendiente de lectura/implementacion. |
| `IR-002` | `USR-UE-PROD` | `INST-PROD-DEMO-001` v`1.0` | `implemented` | `assigned_at`, `read_at`, `interpreted_at`, `accepted_at`, `implemented_at` | Validar cumplido. |
| `IR-003` | `USR-LECT-PROD` | `INST-PROD-DEMO-001` v`1.0` | `accepted` | `assigned_at`, `read_at`, `interpreted_at`, `accepted_at` | Validar aceptado sin implementacion final. |
| `IR-004` | `USR-SIN-PERM` | Sin registro | No aplica | No aplica | Confirmar que no tiene relacion documental. |

## 11. Escenarios de visor documental

| Escenario | Usuario | Documento/archivo | Resultado esperado |
| --- | --- | --- | --- |
| Visor permitido OyM | `USR-OYM-ADM` | `PDF-OYM-001` | Acceso 200, marca de agua, auditoria `DOCUMENT_VIEWED` success. |
| Visor permitido por copia | `USR-LECT-PROD` | `PDF-OYM-001` | Acceso 200 por copia o implementacion, sin ruta fisica. |
| Visor denegado sin relacion | `USR-SIN-PERM` | `PDF-PROD-002` | 403 y auditoria denied si aplica. |
| Visor denegado Auditor | `USR-AUD` | `PDF-OYM-001` | 403; auditor revisa eventos, no contenido documental. |
| Archivo inactivo | `USR-OYM-ADM` | `PDF-RRHH-001` | 404 o mensaje controlado de archivo no disponible. |
| Documento obsoleto | `USR-LECT-PROD` | `PDF-OBS-001` | Sin acceso lector general; OyM puede consultar segun permisos. |

## 12. Escenarios de reportes

### 12.1 Libro Maestro

Debe mostrar todos los documentos demo para OyM y permitir filtros por:

* Tipo documental.
* Unidad responsable.
* Estado.
* Vigencia basada en estados.
* Codigo documental.
* Titulo.

### 12.2 Reporte mensual

Debe incluir documentos/versiones con `published_at` dentro del mes piloto:

* `PROC-OYM-DEMO-001` v`1.0`.
* `INST-PROD-DEMO-001` v`1.0`.

Los documentos sin `published_at` no deben aparecer en el reporte mensual.

### 12.3 Reporte de copias controladas

Debe permitir validar:

* Total por estado: `active`, `delivered`, `retired`, `registered`.
* Filtro por unidad destinataria `PROD` y `RRHH`.
* Filtro por usuario destinatario `USR-LECT-PROD` o `USR-UE-PROD`.
* Filtro por codigo documental.

### 12.4 Reporte de implementacion/lectura

Debe permitir validar:

* Total por estado: `pending`, `accepted`, `implemented`.
* Filtro por usuario.
* Filtro por unidad del usuario.
* Filtro por documento y codigo.
* Cumplidos vs pendientes segun estados existentes.

### 12.5 Exportacion CSV

Cada reporte debe poder exportarse a CSV para usuario OyM autorizado:

* CSV con `Content-Disposition: attachment`.
* CSV UTF-8/BOM.
* CSV sin PDFs.
* CSV sin adjuntos.
* CSV sin rutas fisicas.
* CSV sin `MEDIA_URL`.

## 13. Escenarios de auditoria

| Evento esperado | Accion | Usuario | Resultado |
| --- | --- | --- | --- |
| `DOCUMENT_VIEWED` | Visor permitido | `USR-LECT-PROD` | `success` |
| `DOCUMENT_VIEWED` | Visor denegado | `USR-SIN-PERM` | `denied` |
| `DOCUMENT_VIEWED` | Archivo inactivo/no disponible | `USR-OYM-ADM` | `failure` o resultado equivalente existente |
| `REPORT_GENERATED` | Consulta Libro Maestro | `USR-OYM-ADM` | `REPORT_VIEWED`, `success` |
| `REPORT_GENERATED` | Exportacion CSV | `USR-OYM-ANA` | `REPORT_EXPORTED`, `success` |
| `REPORT_GENERATED` | Intento reporte sin permiso | `USR-LECT-PROD` | `denied` si el patron actual lo registra |

La auditoria no debe guardar contenido documental, PDFs ni rutas de archivos.

## 14. Matriz de permisos esperados

| Usuario demo | Rol | Unidad | Documentos | Visor PDF | Solicitudes | Copias | Implementacion | Auditoria | Reportes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `USR-OYM-ADM` | `oym_admin` | `OYM` | Acceso funcional OyM | Permitido | Ver y crear | Ver todas | Ver/reportar | Ver funcional | Ver/exportar |
| `USR-OYM-ANA` | `oym_analyst` | `OYM` | Acceso funcional OyM | Permitido | Ver y crear | Ver todas | Ver/reportar | Ver funcional | Ver/exportar |
| `USR-UE-PROD` | `executing_unit` | `PROD` | Modulo documentos segun reglas visibles | Solo si hay relacion | Crear propias | Ver aplicables | Ver propias | Denegado | Denegado |
| `USR-LECT-PROD` | `reader` | `PROD` | Modulo documentos segun reglas visibles | Solo por copia o implementacion | Denegado | Ver aplicables | Ver propias | Denegado | Denegado |
| `USR-AUD` | `auditor` | `OYM` | Denegado por modulo | Denegado | Denegado | Denegado | Denegado salvo regla futura | Ver auditoria | Denegado |
| `USR-SIS` | `systems_tech_admin` | `SIS` | Denegado por modulo documental | Denegado | Crear segun helper actual | Denegado | Ver modulo si activo, sin rol funcional OyM | Ver auditoria tecnica | Denegado |
| `USR-SIN-PERM` | `reader` | `ADMIN` | Modulo documentos sin relacion aplicable | Denegado para documentos demo | Denegado | Sin copias | Solo propias inexistentes | Denegado | Denegado |

Esta matriz se basa en los helpers existentes. Si Organizacion y Metodos requiere una matriz formal `documento <-> usuario/unidad autorizada`, debe validarse funcionalmente antes de modelarla.

## 15. Criterios de aceptacion

PILOTO-P02 queda aceptado si:

* El set demo cubre todos los roles requeridos.
* Existe al menos un usuario sin permiso para escenarios negativos.
* Las unidades demo permiten validar filtros y permisos por unidad.
* Los tipos documentales demo permiten validar filtros por tipo.
* Los documentos demo cubren estados `active`, `published`, `under_review` y `obsolete`.
* Las versiones demo cubren `published_at`, vigencia y obsolescencia.
* Los archivos PDF demo cubren archivo activo, inactivo y denegado por permiso.
* Las copias controladas demo cubren estados relevantes.
* Los registros de implementacion cubren pendiente, aceptado e implementado.
* Los reportes demo cubren HTML, filtros y CSV.
* La auditoria esperada queda definida.
* No se crearon usuarios, datos, fixtures, seeders, modelos ni migraciones.

## 16. Criterios de bloqueo

El avance a PILOTO-P03 debe bloquearse si:

* Se requiere usar informacion productiva para cubrir un escenario.
* No existe usuario demo para algun rol critico.
* No existe escenario negativo de permisos.
* No se puede cubrir visor, reportes o auditoria con datos ficticios.
* OyM no valida la pertinencia funcional de documentos demo.
* Sistemas no valida que los datos puedan respaldarse y restaurarse.
* Se intenta crear datos reales antes de autorizacion.

## 17. Que debe quedar listo para PILOTO-P03

Para PILOTO-P03 debe quedar listo:

* Documento de datos demo aprobado como referencia.
* Lista cerrada de usuarios demo a crear.
* Lista cerrada de unidades y tipos documentales demo.
* Lista cerrada de documentos, versiones y PDFs demo.
* Escenarios de copias controladas e implementacion definidos.
* Matriz de permisos esperados.
* Criterios de auditoria esperada.
* Decision sobre si PILOTO-P03 sera fixture, comando seed controlado o carga manual guiada.
* Confirmacion de que no se usaran datos productivos.

## 18. Implementacion tecnica PILOTO-P03

PILOTO-P03 implementa el set demo mediante un comando de management Django:

```bash
cd backend
python manage.py seed_pilot_demo_data
```

Con Docker:

```bash
docker compose exec backend python manage.py seed_pilot_demo_data
```

Precondicion obligatoria:

```bash
cd backend
python manage.py seed_base_catalogs
```

Con Docker:

```bash
docker compose exec backend python manage.py seed_base_catalogs
```

El comando falla de forma controlada si faltan los grupos base de roles creados por `seed_base_catalogs`.

Modo de revision sin escritura:

```bash
cd backend
python manage.py seed_pilot_demo_data --dry-run
```

El comando es idempotente: ejecutarlo varias veces no debe duplicar usuarios, documentos, versiones, archivos, copias controladas ni registros de implementacion.

La contrasena por defecto para usuarios demo nuevos es:

```text
DemoPilot2026!
```

Esta contrasena es solo para ambiente local o piloto controlado. No debe usarse en produccion ni con usuarios reales.

El comando crea archivos PDF ficticios en el almacenamiento configurado por `MEDIA_ROOT`. Esos archivos no contienen informacion productiva y no deben versionarse en el repositorio.

PILOTO-P03 no inicia el piloto. Solo deja disponible el mecanismo repetible para cargar datos demo cuando exista autorizacion.
