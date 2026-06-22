# Roles y Permisos - SGD-OFTALMI

## 1. Propósito del documento

Este documento define los roles iniciales, responsabilidades y permisos funcionales del MVP del sistema SGD-OFTALMI.

Su objetivo es establecer una base clara para el diseño de seguridad, autorización, vistas, acciones permitidas y restricciones de acceso dentro del sistema.

Este documento debe ser utilizado como referencia para:

* Diseño funcional.
* Diseño técnico.
* Configuración de grupos y permisos.
* Desarrollo backend.
* Desarrollo frontend.
* Pruebas de seguridad.
* Auditoría.

## 2. Contexto funcional

SGD-OFTALMI será administrado funcionalmente por Organización y Métodos.

El sistema permitirá controlar información documentada, solicitudes, documentos, versiones, copias controladas, constancias de implementación, documentos obsoletos, notificaciones, auditoría y reportes.

La Gerencia de Garantía de la Calidad no será dueña funcional del MVP. Podrá actuar como unidad usuaria, consultora o destinataria de documentos cuando sus documentos se gestionen bajo la metodología de Organización y Métodos.

Sistemas será responsable de la plataforma técnica, infraestructura, despliegue, soporte, operación, respaldos y monitoreo. Sistemas también podrá actuar como unidad usuaria cuando corresponda, pero no será dueño funcional de las reglas de gestión documental.

## 3. Principios de autorización

Los permisos deben diseñarse bajo los siguientes principios:

* Mínimo privilegio.
* Separación entre administración funcional y administración técnica.
* Acceso según rol, unidad ejecutora, asignación documental o permiso explícito.
* Trazabilidad de acciones críticas.
* Restricción de acceso directo a archivos documentales.
* Reportes exclusivos para Organización y Métodos.
* Documentos obsoletos ocultos para usuarios lectores generales.
* Usuarios lectores solo con consulta controlada y confirmación de implementación.

## 4. Roles iniciales del MVP

Los roles iniciales del MVP son:

| Rol                            | Tipo                | Descripción                                                                    |
| ------------------------------ | ------------------- | ------------------------------------------------------------------------------ |
| OyM Administrador Funcional    | Funcional           | Responsable principal de la administración documental del sistema.             |
| Analista OyM                   | Funcional           | Procesa solicitudes, controla documentos y realiza seguimiento operativo.      |
| Unidad Ejecutora               | Funcional           | Solicita control, modificación o desincorporación documental.                  |
| Usuario Lector                 | Funcional           | Consulta documentos asignados y confirma lectura, aceptación e implementación. |
| Sistemas Administrador Técnico | Técnico             | Administra plataforma, despliegue, soporte, operación y configuración técnica. |
| Auditor                        | Funcional / Control | Rol opcional para consulta controlada de trazabilidad y eventos.               |

Nota: el rol Auditor puede quedar como rol futuro si no forma parte del MVP inicial.

## 5. OyM Administrador Funcional

### 5.1 Responsabilidad

El rol OyM Administrador Funcional representa al personal de Organización y Métodos con responsabilidad principal sobre la gestión documental.

### 5.2 Puede realizar

* Administrar catálogos funcionales.
* Registrar documentos controlados.
* Cargar archivos documentales.
* Validar codificación documental.
* Procesar solicitudes documentales.
* Aprobar u observar solicitudes.
* Registrar o gestionar modificaciones documentales.
* Publicar documentos.
* Gestionar obsolescencia.
* Ejecutar desincorporación formal.
* Gestionar copias controladas.
* Gestionar constancias de implementación.
* Consultar documentos obsoletos.
* Generar reportes.
* Exportar reportes a Excel.
* Consultar auditoría funcional.
* Definir usuarios o asignaciones funcionales según alcance aprobado.

### 5.3 No debe realizar

* Modificar configuración técnica de infraestructura.
* Administrar secretos, contenedores, base de datos o servidores.
* Ejecutar despliegues.
* Modificar código fuente.
* Acceder a funciones técnicas no funcionales.

## 6. Analista OyM

### 6.1 Responsabilidad

El rol Analista OyM representa al personal operativo de Organización y Métodos que gestiona el flujo diario de documentación.

### 6.2 Puede realizar

* Registrar solicitudes recibidas.
* Revisar documentos presentados por Unidades Ejecutoras.
* Registrar observaciones.
* Validar datos documentales.
* Actualizar estados bajo permisos aprobados.
* Registrar difusión documental.
* Registrar seguimiento de implementación.
* Consultar documentos vigentes.
* Consultar documentos obsoletos para control interno.
* Gestionar constancias pendientes.
* Consultar reportes autorizados.
* Exportar reportes autorizados a Excel.

### 6.3 No debe realizar

* Modificar parámetros críticos sin autorización de administrador funcional.
* Modificar usuarios técnicos.
* Cambiar configuración de infraestructura.
* Ejecutar tareas DevOps.
* Acceder a acciones reservadas al administrador funcional si no tiene permiso explícito.

## 7. Unidad Ejecutora

### 7.1 Responsabilidad

La Unidad Ejecutora representa a áreas internas de Laboratorios Oftalmi que generan, solicitan o reciben información documentada.

Ejemplos:

* Organización y Métodos.
* Gerencia de Garantía de la Calidad como unidad usuaria.
* Producción.
* Sistemas.
* Recursos Humanos.
* Administración.
* Otras áreas definidas por OyM.

### 7.2 Puede realizar

* Solicitar control de nueva información documentada.
* Solicitar modificación documental.
* Solicitar desincorporación documental cuando aplique.
* Consultar estado de sus solicitudes.
* Recibir observaciones de OyM.
* Consultar documentos asignados a su unidad.
* Ver documentos vigentes aplicables.
* Confirmar implementación cuando aplique.

### 7.3 No debe realizar

* Aprobar documentos como OyM si no tiene rol funcional.
* Modificar catálogos de OyM.
* Publicar documentos.
* Desincorporar documentos directamente.
* Ver reportes de OyM.
* Consultar documentos obsoletos salvo autorización expresa.
* Acceder a documentos de otras unidades sin asignación o permiso.

## 8. Usuario Lector

### 8.1 Responsabilidad

El Usuario Lector es el usuario interno que recibe documentos asignados para consulta, lectura, interpretación, aceptación e implementación.

### 8.2 Puede realizar

* Iniciar sesión usando correo institucional.
* Visualizar documentos asignados o aplicables.
* Consultar documentos vigentes asignados.
* Confirmar lectura.
* Confirmar interpretación.
* Confirmar aceptación.
* Confirmar implementación.
* Recibir constancia de implementación.
* Consultar sus documentos pendientes.
* Consultar sus notificaciones.
* Recibir alertas por correo institucional.

### 8.3 No debe realizar

* Descargar documentos.
* Imprimir documentos.
* Copiar documentos desde la aplicación.
* Acceder a reportes.
* Acceder a documentos no asignados.
* Acceder a documentos obsoletos.
* Modificar documentos.
* Cargar documentos.
* Aprobar solicitudes.
* Cambiar estados documentales.
* Ver auditoría.
* Modificar catálogos.
* Administrar usuarios.

### 8.4 Restricción técnica importante

Las restricciones de copiar, imprimir y descargar deben implementarse con controles razonables, incluyendo:

* Visor documental controlado.
* No exposición directa del archivo.
* Permisos backend.
* Registro de visualización.
* Marca de agua cuando aplique.
* Bloqueo de botones de descarga e impresión en la interfaz.

Estas restricciones no deben documentarse como protección absoluta frente a capturas de pantalla u otros mecanismos externos.

## 9. Sistemas Administrador Técnico

### 9.1 Responsabilidad

Sistemas administra la plataforma técnica del sistema.

Sus responsabilidades incluyen:

* Infraestructura.
* Servidores.
* Docker.
* Docker Compose.
* Nginx.
* Gunicorn.
* PostgreSQL.
* Variables de entorno.
* Respaldos.
* Restauración.
* Monitoreo.
* Despliegue.
* Soporte técnico.
* Logs.
* Health checks.

### 9.2 Puede realizar

* Administrar configuración técnica.
* Gestionar despliegues.
* Monitorear servicios.
* Revisar logs técnicos.
* Ejecutar backups y restores.
* Administrar variables de entorno.
* Configurar contenedores.
* Reiniciar servicios.
* Gestionar incidencias técnicas.
* Crear o desactivar usuarios técnicos según procedimiento aprobado.
* Actuar como unidad usuaria cuando corresponda.

### 9.3 No debe realizar

* Modificar reglas funcionales de OyM.
* Modificar catálogos documentales de OyM sin autorización.
* Aprobar documentos como OyM.
* Procesar solicitudes documentales como OyM.
* Desincorporar documentos funcionalmente.
* Acceder al contenido documental salvo soporte autorizado o necesidad técnica justificada.
* Generar reportes funcionales de OyM salvo autorización.
* Alterar evidencias funcionales o auditoría.

## 10. Auditor

### 10.1 Estado del rol

El rol Auditor queda como rol opcional o futuro, salvo que OyM lo confirme dentro del MVP.

### 10.2 Puede realizar si se activa

* Consultar auditoría del sistema.
* Consultar trazabilidad documental.
* Consultar historial de modificaciones.
* Consultar reportes de control autorizados.
* Consultar documentos obsoletos si el alcance lo permite.
* Exportar evidencias si OyM lo autoriza.

### 10.3 No debe realizar

* Modificar documentos.
* Procesar solicitudes.
* Cambiar estados.
* Administrar catálogos.
* Administrar plataforma técnica.
* Modificar usuarios.
* Alterar eventos de auditoría.

## 11. Matriz preliminar de permisos

| Acción / Módulo                    |   OyM Admin |            Analista OyM |         Unidad Ejecutora | Usuario Lector |            Sistemas Técnico |            Auditor |
| ---------------------------------- | ----------: | ----------------------: | -----------------------: | -------------: | --------------------------: | -----------------: |
| Iniciar sesión                     |          Sí |                      Sí |                       Sí |             Sí |                          Sí |                 Sí |
| Administrar usuarios funcionales   |          Sí |            No / Parcial |                       No |             No |           Técnico / Parcial |                 No |
| Administrar infraestructura        |          No |                      No |                       No |             No |                          Sí |                 No |
| Administrar catálogos documentales |          Sí |                 Parcial |                       No |             No |                          No |                 No |
| Registrar documento                |          Sí |                      Sí |            No / Solicita |             No |                          No |                 No |
| Cargar archivo documental          |          Sí |                      Sí |            No / Solicita |             No |                          No |                 No |
| Solicitar control documental       |          Sí |                      Sí |                       Sí |             No |         Como unidad usuaria |                 No |
| Solicitar modificación documental  |          Sí |                      Sí |                       Sí |             No |         Como unidad usuaria |                 No |
| Procesar solicitudes               |          Sí |                      Sí |                       No |             No |                          No |                 No |
| Publicar documento                 |          Sí | Parcial / Según permiso |                       No |             No |                          No |                 No |
| Visualizar documento asignado      |          Sí |                      Sí |                       Sí |             Sí |       Como usuario asignado |      Según permiso |
| Descargar documento                | Restringido |             Restringido |                       No |             No |                          No | Según autorización |
| Imprimir documento                 | Restringido |             Restringido |                       No |             No |                          No | Según autorización |
| Copiar documento                   |          No |                      No |                       No |             No |                          No |                 No |
| Confirmar lectura                  |          Sí |                      Sí |                       Sí |             Sí |       Como usuario asignado |                 No |
| Confirmar implementación           |          Sí |                      Sí |                       Sí |             Sí |       Como usuario asignado |                 No |
| Emitir constancia                  |          Sí |                      Sí |                  Sistema |        Sistema |                          No |                 No |
| Consultar constancias              |          Sí |                      Sí | Solo propias o de unidad |   Solo propias |                          No |      Según permiso |
| Gestionar copias controladas       |          Sí |                      Sí |            No / Solicita |             No |                          No |                 No |
| Consultar documentos obsoletos     |          Sí |                      Sí |                       No |             No | No salvo soporte autorizado |      Según permiso |
| Desincorporar documento            |          Sí |      No / Según permiso |                       No |             No |                          No |                 No |
| Generar reportes                   |          Sí |                      Sí |                       No |             No |       No salvo autorización |      Según permiso |
| Exportar reportes a Excel          |          Sí |                      Sí |                       No |             No |       No salvo autorización |      Según permiso |
| Consultar auditoría                |          Sí |                 Parcial |                       No |             No |          Técnica / Limitada |                 Sí |
| Modificar reglas funcionales       |          Sí |      No / Según permiso |                       No |             No |                          No |                 No |

## 12. Permisos mínimos por módulo

### 12.1 accounts

| Permiso            | Roles                                                                      |
| ------------------ | -------------------------------------------------------------------------- |
| Crear usuario      | OyM Admin / Sistemas Técnico según procedimiento                           |
| Editar usuario     | OyM Admin / Sistemas Técnico según procedimiento                           |
| Desactivar usuario | OyM Admin / Sistemas Técnico según procedimiento                           |
| Cambiar roles      | OyM Admin con control funcional / Sistemas solo soporte técnico autorizado |
| Ver usuarios       | OyM Admin / Sistemas Técnico                                               |

### 12.2 organizational_units

| Permiso                     | Roles                                       |
| --------------------------- | ------------------------------------------- |
| Crear unidad ejecutora      | OyM Admin                                   |
| Editar unidad ejecutora     | OyM Admin                                   |
| Desactivar unidad ejecutora | OyM Admin                                   |
| Ver unidades                | OyM Admin / Analista OyM / Sistemas Técnico |

### 12.3 document_types

| Permiso                    | Roles                                                       |
| -------------------------- | ----------------------------------------------------------- |
| Crear tipo documental      | OyM Admin                                                   |
| Editar tipo documental     | OyM Admin                                                   |
| Desactivar tipo documental | OyM Admin                                                   |
| Ver tipos documentales     | OyM Admin / Analista OyM / Unidad Ejecutora según necesidad |

### 12.4 documents

| Permiso                        | Roles                               |
| ------------------------------ | ----------------------------------- |
| Crear documento                | OyM Admin / Analista OyM            |
| Editar metadatos               | OyM Admin / Analista OyM autorizado |
| Cargar archivo                 | OyM Admin / Analista OyM            |
| Publicar documento             | OyM Admin                           |
| Ver documento vigente asignado | Usuario asignado                    |
| Ver documento obsoleto         | OyM Admin / Analista OyM autorizado |
| Desincorporar documento        | OyM Admin                           |

### 12.5 document_requests

| Permiso                   | Roles                                                 |
| ------------------------- | ----------------------------------------------------- |
| Crear solicitud           | Unidad Ejecutora / OyM / Sistemas como unidad usuaria |
| Ver solicitud propia      | Unidad Ejecutora solicitante                          |
| Ver todas las solicitudes | OyM Admin / Analista OyM                              |
| Procesar solicitud        | OyM Admin / Analista OyM                              |
| Observar solicitud        | OyM Admin / Analista OyM                              |
| Cerrar solicitud          | OyM Admin / Analista OyM autorizado                   |

### 12.6 implementation_records

| Permiso                         | Roles                    |
| ------------------------------- | ------------------------ |
| Ver pendiente propio            | Usuario asignado         |
| Confirmar lectura               | Usuario asignado         |
| Confirmar interpretación        | Usuario asignado         |
| Confirmar aceptación            | Usuario asignado         |
| Confirmar implementación        | Usuario asignado         |
| Ver constancias propias         | Usuario asignado         |
| Ver constancias por documento   | OyM Admin / Analista OyM |
| Reportar constancias pendientes | OyM Admin / Analista OyM |

### 12.7 controlled_copies

| Permiso                           | Roles                    |
| --------------------------------- | ------------------------ |
| Registrar copia controlada        | OyM Admin / Analista OyM |
| Registrar entrega                 | OyM Admin / Analista OyM |
| Registrar retiro                  | OyM Admin / Analista OyM |
| Ver copias controladas            | OyM Admin / Analista OyM |
| Reportar copias activas/retiradas | OyM Admin / Analista OyM |

### 12.8 reports

| Permiso                     | Roles                    |
| --------------------------- | ------------------------ |
| Generar reportes            | OyM Admin / Analista OyM |
| Exportar reportes a Excel   | OyM Admin / Analista OyM |
| Ver reportes                | OyM Admin / Analista OyM |
| Acceso de usuarios lectores | No permitido             |

### 12.9 audit

| Permiso                 | Roles                                        |
| ----------------------- | -------------------------------------------- |
| Ver auditoría funcional | OyM Admin / Auditor autorizado               |
| Ver auditoría técnica   | Sistemas Técnico                             |
| Exportar auditoría      | OyM Admin / Auditor autorizado según alcance |
| Modificar auditoría     | No permitido                                 |

### 12.10 notifications

| Permiso                                   | Roles                           |
| ----------------------------------------- | ------------------------------- |
| Ver notificaciones propias                | Todos los usuarios autenticados |
| Gestionar notificaciones funcionales      | OyM Admin / Analista OyM        |
| Gestionar configuración técnica de correo | Sistemas Técnico                |
| Enviar recordatorios                      | Sistema / OyM según flujo       |

## 13. Reglas especiales de acceso documental

* Todo acceso a documentos debe pasar por autorización backend.
* No debe exponerse directamente la ruta física del archivo.
* No debe permitirse descarga directa a usuarios lectores.
* La visualización debe ser auditable.
* El acceso debe considerar documento, versión, usuario, unidad y estado.
* Los documentos obsoletos no deben mostrarse a usuarios lectores.
* OyM puede consultar obsoletos para control y trazabilidad.
* Sistemas no debe consultar contenido salvo necesidad técnica autorizada.

## 14. Relación con grupos de Django

Recomendación técnica inicial:

Usar grupos de Django para mapear roles generales:

```text
OYM_ADMIN
OYM_ANALYST
EXECUTING_UNIT
READER
SYSTEMS_TECH_ADMIN
AUDITOR
```

Permisos específicos pueden implementarse mediante:

* Permisos nativos de Django.
* Permisos personalizados por modelo.
* Validaciones en `permissions.py`.
* Servicios de autorización cuando las reglas dependan de documento, unidad, versión o asignación.

## 15. Relación con auditoría

Deben auditarse especialmente las acciones de:

* Inicio de sesión.
* Visualización documental.
* Cambio de permisos.
* Creación de usuario.
* Desactivación de usuario.
* Cambio de rol.
* Creación o modificación de documento.
* Publicación documental.
* Desincorporación documental.
* Confirmación de implementación.
* Generación de reportes.
* Exportación a Excel.
* Entrega o retiro de copias controladas.

## 16. Restricciones para el punto 11

Durante el punto 11 no debe implementarse toda la matriz de permisos completa.

Sí puede prepararse:

* Custom User.
* Admin básico.
* Grupos base si Codex lo considera necesario.
* Estructura inicial de permisos.
* Preparación de `permissions.py`.
* Configuración para autenticación por email.

No debe implementarse todavía:

* Autorización documental completa.
* Permisos por documento y versión.
* Workflows completos.
* Visor documental final.
* Reportes finales.
* Auditoría completa.
* Notificaciones finales.

## 17. Pendientes de validación futura

* Definir si existirá rol Auditor dentro del MVP o posterior.
* Definir si los responsables de Unidad Ejecutora tendrán permisos diferenciados frente a usuarios lectores comunes.
* Definir si OyM tendrá subniveles adicionales de aprobación.
* Definir si Sistemas podrá crear usuarios o solo administrar soporte técnico.
* Definir si la consulta de obsoletos requerirá justificación obligatoria.
* Definir si las constancias serán descargables por usuarios o solo consultables.

