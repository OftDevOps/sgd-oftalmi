# Modelo de Datos Preliminar - SGD-OFTALMI

## 1. Propósito del documento

Este documento define el modelo preliminar de datos para el MVP del sistema SGD-OFTALMI.

Su objetivo es servir como guía técnica para el diseño inicial del backend, evitando que se creen modelos, relaciones o reglas de negocio fuera del alcance validado por Organización y Métodos.

Este documento no representa todavía el modelo físico definitivo de base de datos. Es una referencia preliminar para análisis, diseño técnico, implementación progresiva y validación funcional.

## 2. Contexto funcional

SGD-OFTALMI es una aplicación interna para la Gestión Documental administrada por Organización y Métodos.

El sistema debe controlar:

* Usuarios.
* Roles y permisos.
* Unidades ejecutoras.
* Tipos documentales.
* Documentos.
* Versiones documentales.
* Solicitudes documentales.
* Copias controladas.
* Constancias de lectura, aceptación e implementación.
* Documentos obsoletos.
* Notificaciones.
* Auditoría.
* Reportes.

El username del sistema será el correo electrónico institucional.

## 3. Principios de modelado

El modelo de datos debe cumplir estos principios:

* Trazabilidad antes que simplicidad aparente.
* No eliminación física como operación normal.
* Control por usuario, documento y versión.
* Separación entre documento lógico y archivo digital.
* Separación entre administración funcional y administración técnica.
* Uso de estados explícitos.
* Relaciones claras con unidad ejecutora.
* Auditoría de acciones críticas.
* Soporte para reportes de OyM.
* Soporte para exportación futura a Excel.

## 4. Módulos asociados

El modelo se distribuirá preliminarmente en las siguientes apps Django:

```text
backend/apps/accounts/
backend/apps/organizational_units/
backend/apps/document_types/
backend/apps/documents/
backend/apps/document_requests/
backend/apps/controlled_copies/
backend/apps/implementation_records/
backend/apps/notifications/
backend/apps/audit/
backend/apps/reports/
```

## 5. Entidades preliminares

Entidades principales recomendadas:

```text
User
OrganizationalUnit
DocumentType
Document
DocumentVersion
DocumentFile
DocumentRequest
DocumentChecklist
DocumentCodeSequence
ControlledCopy
ImplementationRecord
ImplementationCertificate
Notification
AuditEvent
ReportExport
```

Entidades futuras o sujetas a validación:

```text
AuthorizedSigner
DocumentStatus
RequestStatus
ReportSnapshot
AuditAccessJustification
```

## 6. User

### 6.1 Propósito

Representa a los usuarios internos del sistema.

Debe implementarse como Custom User desde el inicio, usando el correo electrónico institucional como identificador principal.

### 6.2 Campos preliminares

| Campo               | Tipo sugerido       |  Requerido | Descripción                               |
| ------------------- | ------------------- | ---------: | ----------------------------------------- |
| id                  | UUID / BigAutoField |         Sí | Identificador interno.                    |
| email               | EmailField unique   |         Sí | Username del sistema.                     |
| first_name          | CharField           |         Sí | Nombre.                                   |
| last_name           | CharField           |         Sí | Apellido.                                 |
| is_active           | BooleanField        |         Sí | Indica si el usuario puede acceder.       |
| is_staff            | BooleanField        |         Sí | Acceso al admin Django.                   |
| is_superuser        | BooleanField        |         Sí | Superusuario técnico.                     |
| organizational_unit | FK                  | No inicial | Unidad ejecutora asociada.                |
| is_technical_user   | BooleanField        |         No | Indica si es usuario técnico de Sistemas. |
| date_joined         | DateTimeField       |         Sí | Fecha de creación.                        |
| updated_at          | DateTimeField       |         Sí | Última actualización.                     |

### 6.3 Reglas

* `email` debe ser único.
* `email` debe ser `USERNAME_FIELD`.
* No debe usarse `username` tradicional como identificador principal.
* Un usuario inactivo no debe poder autenticarse.
* Las acciones críticas deben asociarse al usuario autenticado.

## 7. OrganizationalUnit

### 7.1 Propósito

Representa las unidades ejecutoras internas que participan en la gestión documental.

Ejemplos:

* Organización y Métodos.
* Gerencia de Garantía de la Calidad como unidad usuaria.
* Sistemas.
* Producción.
* Recursos Humanos.
* Otras unidades definidas por OyM.

### 7.2 Campos preliminares

| Campo       | Tipo sugerido       | Requerido | Descripción                  |
| ----------- | ------------------- | --------: | ---------------------------- |
| id          | UUID / BigAutoField |        Sí | Identificador.               |
| name        | CharField           |        Sí | Nombre de la unidad.         |
| code        | CharField unique    |        No | Código interno de la unidad. |
| description | TextField           |        No | Descripción.                 |
| is_active   | BooleanField        |        Sí | Estado activo/inactivo.      |
| created_at  | DateTimeField       |        Sí | Fecha de creación.           |
| updated_at  | DateTimeField       |        Sí | Última actualización.        |

### 7.3 Reglas

* Una unidad inactiva no debe usarse para nuevas asignaciones.
* Sistemas puede ser unidad ejecutora y administrador técnico.
* Calidad puede ser unidad usuaria, pero no dueño funcional del MVP.

## 8. DocumentType

### 8.1 Propósito

Representa las tipologías documentales controladas por OyM.

### 8.2 Campos preliminares

| Campo       | Tipo sugerido       | Requerido | Descripción                 |
| ----------- | ------------------- | --------: | --------------------------- |
| id          | UUID / BigAutoField |        Sí | Identificador.              |
| code        | CharField unique    |        Sí | Código del tipo documental. |
| name        | CharField           |        Sí | Nombre del tipo documental. |
| description | TextField           |        No | Descripción.                |
| is_active   | BooleanField        |        Sí | Estado.                     |
| created_at  | DateTimeField       |        Sí | Fecha de creación.          |
| updated_at  | DateTimeField       |        Sí | Última actualización.       |

### 8.3 Reglas

* Solo OyM debe administrar tipologías documentales.
* Un tipo documental inactivo no debe usarse para nuevos documentos.
* La codificación documental debe considerar el tipo documental cuando aplique.

## 9. Document

### 9.1 Propósito

Representa el documento lógico controlado por el sistema.

El documento lógico no debe confundirse con el archivo físico o digital. Un documento puede tener múltiples versiones.

### 9.2 Campos preliminares

| Campo           | Tipo sugerido         |  Requerido | Descripción                          |
| --------------- | --------------------- | ---------: | ------------------------------------ |
| id              | UUID / BigAutoField   |         Sí | Identificador.                       |
| code            | CharField unique      |         Sí | Código documental único.             |
| title           | CharField             |         Sí | Título del documento.                |
| document_type   | FK DocumentType       |         Sí | Tipo documental.                     |
| owner_unit      | FK OrganizationalUnit |         Sí | Unidad ejecutora responsable.        |
| current_version | FK DocumentVersion    | No inicial | Versión vigente.                     |
| status          | CharField choices     |         Sí | Estado documental.                   |
| is_active       | BooleanField          |         Sí | Indica si está activo en el sistema. |
| created_by      | FK User               |         Sí | Usuario creador.                     |
| created_at      | DateTimeField         |         Sí | Fecha de creación.                   |
| updated_at      | DateTimeField         |         Sí | Última actualización.                |

### 9.3 Reglas

* Todo documento debe tener código único.
* Todo documento debe estar asociado a tipo documental y unidad responsable.
* No debe eliminarse físicamente como operación normal.
* Un documento obsoleto no debe ser visible para usuarios lectores.
* OyM puede consultar documentos obsoletos para trazabilidad.
* El código `FOR-GGHD-010` es el código correcto para Registro de Recepción de Información.
* No debe usarse `FOR-HHGD-010` para ese registro.
* `DOC-GGHD-004` debe mantenerse como una sola entrada válida.

## 10. DocumentVersion

### 10.1 Propósito

Representa una versión o revisión específica de un documento.

Es clave para controlar lectura, aceptación e implementación por versión.

### 10.2 Campos preliminares

| Campo           | Tipo sugerido       | Requerido | Descripción                          |
| --------------- | ------------------- | --------: | ------------------------------------ |
| id              | UUID / BigAutoField |        Sí | Identificador.                       |
| document        | FK Document         |        Sí | Documento asociado.                  |
| version_number  | CharField           |        Sí | Número o código de versión/revisión. |
| status          | CharField choices   |        Sí | Estado de la versión.                |
| issue_date      | DateField           |        No | Fecha de emisión.                    |
| effective_date  | DateField           |        No | Fecha de vigencia.                   |
| expiration_date | DateField           |        No | Fecha de vencimiento.                |
| approved_at     | DateTimeField       |        No | Fecha de aprobación.                 |
| published_at    | DateTimeField       |        No | Fecha de publicación.                |
| obsolete_at     | DateTimeField       |        No | Fecha de obsolescencia.              |
| created_by      | FK User             |        Sí | Usuario creador.                     |
| created_at      | DateTimeField       |        Sí | Fecha de creación.                   |

### 10.3 Reglas

* La aceptación del usuario se controla por documento y versión.
* Una nueva versión aprobada genera nueva obligación de lectura e implementación.
* Una versión obsoleta no debe mostrarse a usuarios lectores.
* Debe conservarse histórico de versiones.

## 11. DocumentFile

### 11.1 Propósito

Representa el archivo digital asociado a una versión documental.

Se separa de `DocumentVersion` para permitir trazabilidad de archivo, hash, ruta interna y metadatos técnicos.

### 11.2 Campos preliminares

| Campo             | Tipo sugerido           | Requerido | Descripción                   |
| ----------------- | ----------------------- | --------: | ----------------------------- |
| id                | UUID / BigAutoField     |        Sí | Identificador.                |
| document_version  | FK DocumentVersion      |        Sí | Versión asociada.             |
| file              | FileField               |        Sí | Archivo almacenado.           |
| original_filename | CharField               |        Sí | Nombre original del archivo.  |
| content_type      | CharField               |        No | Tipo MIME.                    |
| size_bytes        | PositiveBigIntegerField |        No | Tamaño del archivo.           |
| file_hash         | CharField               |        No | Hash para integridad.         |
| uploaded_by       | FK User                 |        Sí | Usuario que cargó el archivo. |
| uploaded_at       | DateTimeField           |        Sí | Fecha de carga.               |
| is_active         | BooleanField            |        Sí | Estado del archivo.           |

### 11.3 Reglas

* No debe exponerse la ruta directa del archivo al usuario lector.
* El acceso debe pasar por autorización backend.
* La visualización debe poder auditarse.
* El archivo debe almacenarse en volumen persistente.

## 12. DocumentRequest

### 12.1 Propósito

Representa solicitudes relacionadas con la gestión documental.

### 12.2 Tipos preliminares

```text
new_document_control
document_modification
document_decommission
document_reception
controlled_copy
implementation_record
```

### 12.3 Campos preliminares

| Campo            | Tipo sugerido         | Requerido | Descripción                  |
| ---------------- | --------------------- | --------: | ---------------------------- |
| id               | UUID / BigAutoField   |        Sí | Identificador.               |
| request_type     | CharField choices     |        Sí | Tipo de solicitud.           |
| status           | CharField choices     |        Sí | Estado de solicitud.         |
| requester        | FK User               |        Sí | Usuario solicitante.         |
| requester_unit   | FK OrganizationalUnit |        Sí | Unidad solicitante.          |
| related_document | FK Document           |        No | Documento relacionado.       |
| title            | CharField             |        Sí | Título o asunto.             |
| description      | TextField             |        No | Descripción de la solicitud. |
| observations     | TextField             |        No | Observaciones de OyM.        |
| created_at       | DateTimeField         |        Sí | Fecha de creación.           |
| updated_at       | DateTimeField         |        Sí | Última actualización.        |
| closed_at        | DateTimeField         |        No | Fecha de cierre.             |

### 12.4 Reglas

* Toda solicitud debe tener solicitante, unidad, tipo, estado y trazabilidad.
* OyM procesa solicitudes documentales.
* Una solicitud de modificación debe asociarse a un documento existente cuando aplique.
* Las observaciones deben conservarse.

## 13. DocumentChecklist

### 13.1 Propósito

Representa chequeos funcionales realizados por OyM sobre una solicitud o documento.

### 13.2 Campos preliminares

| Campo            | Tipo sugerido       | Requerido | Descripción             |
| ---------------- | ------------------- | --------: | ----------------------- |
| id               | UUID / BigAutoField |        Sí | Identificador.          |
| document_request | FK DocumentRequest  |        Sí | Solicitud asociada.     |
| checked_by       | FK User             |        Sí | Analista OyM.           |
| checklist_data   | JSONField           |        Sí | Respuestas del chequeo. |
| result           | CharField choices   |        Sí | Resultado.              |
| observations     | TextField           |        No | Observaciones.          |
| checked_at       | DateTimeField       |        Sí | Fecha de chequeo.       |

### 13.3 Reglas

* Debe conservarse evidencia del chequeo.
* No debe sobrescribirse el resultado sin trazabilidad.
* El detalle puede evolucionar según formatos validados por OyM.

## 14. DocumentCodeSequence

### 14.1 Propósito

Permite controlar correlativos o secuencias de codificación documental.

### 14.2 Campos preliminares

| Campo               | Tipo sugerido             | Requerido | Descripción               |
| ------------------- | ------------------------- | --------: | ------------------------- |
| id                  | UUID / BigAutoField       |        Sí | Identificador.            |
| document_type       | FK DocumentType           |        Sí | Tipo documental.          |
| organizational_unit | FK OrganizationalUnit     |        No | Unidad asociada.          |
| prefix              | CharField                 |        Sí | Prefijo del código.       |
| current_number      | PositiveIntegerField      |        Sí | Último correlativo usado. |
| padding             | PositiveSmallIntegerField |        Sí | Cantidad de dígitos.      |
| is_active           | BooleanField              |        Sí | Estado.                   |
| updated_at          | DateTimeField             |        Sí | Última actualización.     |

### 14.3 Reglas

* Solo OyM debe administrar o validar codificación.
* Debe evitarse duplicidad de códigos.
* La generación automática puede quedar para fase posterior si no está completamente validada.

## 15. ControlledCopy

### 15.1 Propósito

Representa copias controladas de documentos.

### 15.2 Campos preliminares

| Campo            | Tipo sugerido         | Requerido | Descripción                      |
| ---------------- | --------------------- | --------: | -------------------------------- |
| id               | UUID / BigAutoField   |        Sí | Identificador.                   |
| document_version | FK DocumentVersion    |        Sí | Versión asociada.                |
| copy_number      | CharField             |        Sí | Número o identificador de copia. |
| receiver_unit    | FK OrganizationalUnit |        Sí | Unidad receptora.                |
| receiver_user    | FK User               |        No | Responsable receptor.            |
| delivered_at     | DateTimeField         |        No | Fecha de entrega.                |
| retired_at       | DateTimeField         |        No | Fecha de retiro.                 |
| status           | CharField choices     |        Sí | Estado de copia.                 |
| observations     | TextField             |        No | Observaciones.                   |
| created_by       | FK User               |        Sí | Usuario OyM que registra.        |
| created_at       | DateTimeField         |        Sí | Fecha de creación.               |

### 15.3 Reglas

* Toda copia controlada debe estar asociada a documento y versión.
* Debe tener número de copia.
* Debe registrar entrega y retiro cuando aplique.
* OyM debe poder reportar copias activas y retiradas.

## 16. ImplementationRecord

### 16.1 Propósito

Representa la obligación y confirmación de lectura, interpretación, aceptación e implementación de una versión documental por parte de un usuario.

### 16.2 Campos preliminares

| Campo            | Tipo sugerido       | Requerido | Descripción                  |
| ---------------- | ------------------- | --------: | ---------------------------- |
| id               | UUID / BigAutoField |        Sí | Identificador.               |
| user             | FK User             |        Sí | Usuario asignado.            |
| document         | FK Document         |        Sí | Documento.                   |
| document_version | FK DocumentVersion  |        Sí | Versión.                     |
| assigned_at      | DateTimeField       |        Sí | Fecha de asignación.         |
| read_at          | DateTimeField       |        No | Fecha de lectura.            |
| interpreted_at   | DateTimeField       |        No | Fecha de interpretación.     |
| accepted_at      | DateTimeField       |        No | Fecha de aceptación.         |
| implemented_at   | DateTimeField       |        No | Fecha de implementación.     |
| status           | CharField choices   |        Sí | Estado de la implementación. |
| created_at       | DateTimeField       |        Sí | Fecha de creación.           |
| updated_at       | DateTimeField       |        Sí | Última actualización.        |

### 16.3 Estados sugeridos

```text
pending
read
interpreted
accepted
implemented
expired
cancelled
```

### 16.4 Reglas

* La aceptación se controla por usuario, documento y versión.
* No debe solicitarse aceptación repetida para la misma versión ya aceptada.
* Una nueva versión genera nueva obligación.
* Las constancias pendientes deben poder reportarse por OyM.

## 17. ImplementationCertificate

### 17.1 Propósito

Representa la constancia emitida cuando un usuario completa lectura, interpretación, aceptación e implementación.

### 17.2 Campos preliminares

| Campo                 | Tipo sugerido       | Requerido | Descripción                   |
| --------------------- | ------------------- | --------: | ----------------------------- |
| id                    | UUID / BigAutoField |        Sí | Identificador.                |
| implementation_record | OneToOneField       |        Sí | Registro asociado.            |
| certificate_number    | CharField unique    |        Sí | Número de constancia.         |
| generated_at          | DateTimeField       |        Sí | Fecha de generación.          |
| generated_by_system   | BooleanField        |        Sí | Indica generación automática. |
| metadata              | JSONField           |        No | Metadatos de evidencia.       |

### 17.3 Reglas

* Debe existir una constancia por implementación completada.
* La constancia debe estar asociada a usuario, documento y versión mediante `ImplementationRecord`.
* El formato final de constancia puede definirse en fase posterior.

## 18. Notification

### 18.1 Propósito

Representa notificaciones internas del sistema.

### 18.2 Campos preliminares

| Campo               | Tipo sugerido       | Requerido | Descripción                    |
| ------------------- | ------------------- | --------: | ------------------------------ |
| id                  | UUID / BigAutoField |        Sí | Identificador.                 |
| user                | FK User             |        Sí | Usuario destinatario.          |
| title               | CharField           |        Sí | Título.                        |
| message             | TextField           |        Sí | Mensaje.                       |
| notification_type   | CharField choices   |        Sí | Tipo.                          |
| related_object_type | CharField           |        No | Tipo de objeto relacionado.    |
| related_object_id   | CharField           |        No | ID del objeto relacionado.     |
| is_read             | BooleanField        |        Sí | Leída/no leída.                |
| sent_by_email       | BooleanField        |        Sí | Indica si se envió por correo. |
| created_at          | DateTimeField       |        Sí | Fecha de creación.             |
| read_at             | DateTimeField       |        No | Fecha de lectura.              |

### 18.3 Reglas

* Debe notificar pendientes por correo y panel interno.
* Debe notificar nuevas versiones que requieren aceptación.
* Debe permitir consultar notificaciones propias.

## 19. AuditEvent

### 19.1 Propósito

Representa eventos de auditoría del sistema.

### 19.2 Campos preliminares

| Campo       | Tipo sugerido         | Requerido | Descripción                    |
| ----------- | --------------------- | --------: | ------------------------------ |
| id          | UUID / BigAutoField   |        Sí | Identificador.                 |
| user        | FK User nullable      |        No | Usuario que ejecutó la acción. |
| action      | CharField             |        Sí | Acción realizada.              |
| module      | CharField             |        Sí | Módulo origen.                 |
| entity_type | CharField             |        No | Tipo de entidad afectada.      |
| entity_id   | CharField             |        No | ID de entidad afectada.        |
| result      | CharField             |        Sí | Resultado.                     |
| ip_address  | GenericIPAddressField |        No | Dirección IP.                  |
| user_agent  | TextField             |        No | User agent.                    |
| description | TextField             |        No | Descripción legible.           |
| before_data | JSONField             |        No | Datos previos.                 |
| after_data  | JSONField             |        No | Datos posteriores.             |
| created_at  | DateTimeField         |        Sí | Fecha del evento.              |

### 19.3 Reglas

* Debe registrar acciones críticas.
* No debe permitir modificación ordinaria de eventos.
* Debe soportar auditoría funcional y técnica.
* Debe registrar generación y exportación de reportes.

## 20. ReportExport

### 20.1 Propósito

Representa exportaciones de reportes, especialmente a Excel.

### 20.2 Campos preliminares

| Campo        | Tipo sugerido       | Requerido | Descripción                      |
| ------------ | ------------------- | --------: | -------------------------------- |
| id           | UUID / BigAutoField |        Sí | Identificador.                   |
| report_type  | CharField           |        Sí | Tipo de reporte.                 |
| generated_by | FK User             |        Sí | Usuario OyM que genera.          |
| file         | FileField           |        No | Archivo generado si se almacena. |
| format       | CharField           |        Sí | Formato, por ejemplo xlsx.       |
| parameters   | JSONField           |        No | Parámetros usados.               |
| generated_at | DateTimeField       |        Sí | Fecha de generación.             |

### 20.3 Reglas

* Los reportes son exclusivos de OyM.
* Los reportes deben exportarse a Excel.
* Toda generación de reporte debe auditarse.

## 21. Relaciones principales

Relaciones clave:

```text
User → OrganizationalUnit
Document → DocumentType
Document → OrganizationalUnit
Document → DocumentVersion
DocumentVersion → DocumentFile
DocumentRequest → User
DocumentRequest → OrganizationalUnit
DocumentRequest → Document
ControlledCopy → DocumentVersion
ImplementationRecord → User
ImplementationRecord → Document
ImplementationRecord → DocumentVersion
ImplementationCertificate → ImplementationRecord
Notification → User
AuditEvent → User
ReportExport → User
```

## 22. Decisiones para el punto 11

Durante el punto 11 solo debe implementarse una parte mínima del modelo:

Sí se puede implementar:

```text
User
CustomUserManager
AUTH_USER_MODEL
admin básico de User
migración inicial de accounts
```

Puede prepararse, sin lógica final:

```text
organizational_units
document_types
documents
document_requests
audit
reports
notifications
```

No debe implementarse todavía:

```text
Document completo
DocumentVersion completo
DocumentFile completo
DocumentRequest workflow
ControlledCopy completo
ImplementationRecord completo
ImplementationCertificate completo
Notification final
AuditEvent final
ReportExport final
```

## 23. Criterio de aceptación para el punto 11

El punto 11 se considera correcto si:

* Django levanta correctamente.
* `manage.py check` ejecuta sin errores.
* Existe `CustomUser` usando email como username.
* `AUTH_USER_MODEL` está configurado.
* `createsuperuser` solicita correo electrónico.
* La app `accounts` tiene migración inicial.
* PostgreSQL está configurado por variables de entorno.
* Las apps existentes están registradas o preparadas según decisión técnica.
* No se implementaron modelos documentales complejos fuera de alcance.

## 24. Pendientes para fases posteriores

* Definir modelo definitivo de roles y permisos.
* Validar si se usará UUID o BigAutoField.
* Definir estados finales por entidad.
* Definir formato definitivo de constancia.
* Definir estructura exacta del Libro Maestro.
* Definir exportadores Excel.
* Definir política de almacenamiento documental.
* Definir visor documental seguro.
* Definir auditoría detallada por módulo.
* Definir reglas de vencimiento y alertas.

