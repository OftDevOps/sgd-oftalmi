# Reglas de Negocio - SGD-OFTALMI

## 1. Propósito del documento

Este documento consolida las reglas de negocio iniciales del MVP del sistema SGD-OFTALMI, derivadas del levantamiento de información y de las validaciones emitidas por el Departamento de Organización y Métodos.

Las reglas aquí definidas deben ser usadas como referencia obligatoria para análisis, diseño, desarrollo, pruebas y validación funcional.

Ninguna funcionalidad debe implementarse si contradice estas reglas, salvo que exista una nueva validación formal de Organización y Métodos.

## 2. Contexto funcional

SGD-OFTALMI será una aplicación interna para la Gestión Documental administrada por Organización y Métodos.

El sistema controlará información documentada bajo responsabilidad de OyM, incluyendo:

* Codificación documental.
* Solicitudes documentales.
* Recepción, control y archivo.
* Modificación documental.
* Difusión e implementación.
* Desincorporación u obsolescencia documental.
* Copias controladas.
* Constancias de implementación.
* Libro Maestro de Control Documental.
* Reportes.
* Auditoría y trazabilidad.
* Notificaciones.

## 3. Reglas sobre gobierno funcional

| ID         | Regla                                                                                                                                                                |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-GOB-001 | Organización y Métodos es el dueño funcional del MVP.                                                                                                                |
| RN-GOB-002 | Organización y Métodos define reglas funcionales, catálogos documentales, criterios de control documental y reportes.                                                |
| RN-GOB-003 | Sistemas administra la plataforma técnica, infraestructura, despliegue, soporte y operación.                                                                         |
| RN-GOB-004 | Sistemas puede actuar como unidad usuaria cuando corresponda.                                                                                                        |
| RN-GOB-005 | Sistemas no debe modificar reglas funcionales, catálogos documentales ni decisiones de negocio propias de OyM sin autorización formal.                               |
| RN-GOB-006 | Calidad no es dueño funcional del flujo documental del MVP.                                                                                                          |
| RN-GOB-007 | La Gerencia de Garantía de la Calidad puede participar como unidad usuaria, consultora o destinataria cuando sus documentos se gestionen bajo la metodología de OyM. |
| RN-GOB-008 | No deben implementarse procesos documentales propios de Calidad dentro del MVP, salvo validación formal de OyM.                                                      |

## 4. Reglas sobre usuarios e identidad

| ID          | Regla                                                                                 |
| ----------- | ------------------------------------------------------------------------------------- |
| RN-AUTH-001 | El username del sistema será el correo electrónico institucional del usuario.         |
| RN-AUTH-002 | El correo electrónico debe ser único por usuario.                                     |
| RN-AUTH-003 | El sistema debe usar un modelo de usuario personalizado desde el inicio del proyecto. |
| RN-AUTH-004 | No debe usarse el campo username tradicional de Django como identificador principal.  |
| RN-AUTH-005 | Todo usuario debe estar asociado a una unidad ejecutora cuando aplique.               |
| RN-AUTH-006 | Los perfiles de usuario serán definidos en conjunto entre OyM y Sistemas.             |
| RN-AUTH-007 | Un usuario inactivo no debe poder acceder al sistema.                                 |
| RN-AUTH-008 | Las acciones críticas deben quedar asociadas al usuario autenticado que las ejecutó.  |

## 5. Reglas sobre roles y permisos

| ID         | Regla                                                                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-ROL-001 | Deben existir permisos diferenciados para OyM, Sistemas, Unidades Ejecutoras y Usuarios Lectores.                                               |
| RN-ROL-002 | OyM tendrá permisos funcionales para administrar documentos, solicitudes, catálogos, obsolescencia, copias controladas, constancias y reportes. |
| RN-ROL-003 | Sistemas tendrá permisos técnicos para operación de plataforma, soporte, despliegue y administración técnica.                                   |
| RN-ROL-004 | Sistemas no debe tener acceso funcional irrestricto al contenido documental salvo autorización o soporte justificado.                           |
| RN-ROL-005 | Los usuarios lectores solo podrán consultar documentos asignados o aplicables.                                                                  |
| RN-ROL-006 | Los usuarios lectores no tendrán acceso a reportes.                                                                                             |
| RN-ROL-007 | Las Unidades Ejecutoras podrán solicitar control, modificación o desincorporación documental según permisos aprobados.                          |
| RN-ROL-008 | Todo acceso a documentos debe estar condicionado por rol, unidad, asignación o permiso explícito.                                               |

## 6. Reglas sobre documentos

| ID         | Regla                                                                                                          |
| ---------- | -------------------------------------------------------------------------------------------------------------- |
| RN-DOC-001 | Todo documento controlado debe tener código documental único.                                                  |
| RN-DOC-002 | Todo documento controlado debe tener título o nombre.                                                          |
| RN-DOC-003 | Todo documento controlado debe estar asociado a un tipo documental.                                            |
| RN-DOC-004 | Todo documento controlado debe estar asociado a una unidad ejecutora responsable.                              |
| RN-DOC-005 | Todo documento controlado debe tener versión o revisión.                                                       |
| RN-DOC-006 | Todo documento controlado debe tener estado documental.                                                        |
| RN-DOC-007 | Todo archivo documental debe preservar trazabilidad básica: usuario, fecha, versión y metadatos de carga.      |
| RN-DOC-008 | No debe eliminarse físicamente un documento controlado como operación normal del sistema.                      |
| RN-DOC-009 | El documento debe cambiar de estado cuando se modifique, publique, venza, quede obsoleto o sea desincorporado. |
| RN-DOC-010 | El código correcto para Registro de Recepción de Información es FOR-GGHD-010.                                  |
| RN-DOC-011 | El código FOR-HHGD-010 no debe usarse para Registro de Recepción de Información.                               |
| RN-DOC-012 | El documento DOC-GGHD-004 debe mantenerse como una sola entrada válida, eliminando duplicados.                 |

## 7. Reglas sobre estados documentales

Estados documentales base:

* `draft`
* `received`
* `under_review`
* `observed`
* `approved`
* `published`
* `active`
* `expired`
* `obsolete`
* `archived`

| ID         | Regla                                                                                                          |
| ---------- | -------------------------------------------------------------------------------------------------------------- |
| RN-EST-001 | Todo documento debe tener un estado documental vigente en el sistema.                                          |
| RN-EST-002 | No deben agregarse nuevos estados sin justificación funcional documentada.                                     |
| RN-EST-003 | Un documento publicado o activo puede ser visible para los usuarios asignados.                                 |
| RN-EST-004 | Un documento obsoleto no debe ser visible para usuarios lectores generales.                                    |
| RN-EST-005 | Un documento archivado o desincorporado debe conservar trazabilidad histórica.                                 |
| RN-EST-006 | Una nueva versión aprobada puede generar la obsolescencia de la versión anterior según regla definida por OyM. |

## 8. Reglas sobre solicitudes documentales

| ID         | Regla                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------- |
| RN-SOL-001 | El sistema debe soportar solicitudes de control de nueva información documentada.             |
| RN-SOL-002 | El sistema debe soportar solicitudes de modificación de información documentada.              |
| RN-SOL-003 | El sistema debe soportar solicitudes de desincorporación de información documentada obsoleta. |
| RN-SOL-004 | El sistema debe soportar registro de recepción de información.                                |
| RN-SOL-005 | El sistema debe soportar solicitud o registro de copias controladas.                          |
| RN-SOL-006 | Toda solicitud debe tener solicitante, unidad ejecutora, tipo, fecha, estado y trazabilidad.  |
| RN-SOL-007 | Una solicitud de modificación debe estar asociada a un documento existente cuando aplique.    |
| RN-SOL-008 | Una solicitud observada o devuelta debe conservar la observación emitida por OyM.             |
| RN-SOL-009 | OyM será responsable de procesar y validar solicitudes documentales.                          |

## 9. Reglas sobre modificación documental

| ID         | Regla                                                                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-MOD-001 | Toda modificación documental debe quedar asociada al documento original.                                                                      |
| RN-MOD-002 | Toda modificación debe generar trazabilidad de versión o revisión.                                                                            |
| RN-MOD-003 | Una nueva versión aprobada debe sustituir la versión anterior según regla funcional aplicable.                                                |
| RN-MOD-004 | Una nueva versión aprobada debe generar nueva obligación de lectura, interpretación, aceptación e implementación para los usuarios asignados. |
| RN-MOD-005 | El histórico de modificaciones debe poder consultarse o reportarse por OyM.                                                                   |

## 10. Reglas sobre consulta documental

| ID         | Regla                                                                                                                                                                       |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RN-CON-001 | Los usuarios lectores solo podrán visualizar documentos asignados o aplicables.                                                                                             |
| RN-CON-002 | Los usuarios lectores no podrán copiar documentos desde la aplicación.                                                                                                      |
| RN-CON-003 | Los usuarios lectores no podrán imprimir documentos desde la aplicación.                                                                                                    |
| RN-CON-004 | Los usuarios lectores no podrán descargar documentos desde la aplicación.                                                                                                   |
| RN-CON-005 | La aplicación debe evitar exponer directamente la ruta física o URL pública del archivo documental.                                                                         |
| RN-CON-006 | La visualización debe registrarse en auditoría cuando aplique.                                                                                                              |
| RN-CON-007 | Las restricciones de copiar, imprimir y descargar son controles razonables de aplicación, no protección absoluta frente a capturas de pantalla u otros mecanismos externos. |

## 11. Reglas sobre lectura, aceptación e implementación

| ID         | Regla                                                                                                                                  |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| RN-IMP-001 | La aceptación se controla por usuario, documento y versión.                                                                            |
| RN-IMP-002 | Si el usuario ya aceptó una versión vigente, el sistema no debe volver a solicitar aceptación para esa misma versión.                  |
| RN-IMP-003 | Si se publica una nueva versión, el sistema debe generar una nueva obligación de lectura, interpretación, aceptación e implementación. |
| RN-IMP-004 | El usuario debe confirmar lectura, interpretación, aceptación e implementación del documento asignado.                                 |
| RN-IMP-005 | La validación debe aparecer siempre que el usuario no haya completado el proceso para un documento asignado.                           |
| RN-IMP-006 | El sistema debe emitir una constancia de implementación luego de completar el proceso.                                                 |
| RN-IMP-007 | La constancia debe estar asociada al usuario, documento y versión.                                                                     |
| RN-IMP-008 | Las constancias pendientes deben poder reportarse por OyM.                                                                             |

## 12. Reglas sobre documentos obsoletos

| ID         | Regla                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------ |
| RN-OBS-001 | Los documentos obsoletos no serán visibles para usuarios lectores generales.                                       |
| RN-OBS-002 | Los documentos obsoletos permanecerán en el sistema hasta que OyM ejecute su desincorporación formal.              |
| RN-OBS-003 | OyM podrá consultar documentos obsoletos para control, auditoría y trazabilidad.                                   |
| RN-OBS-004 | Sistemas no debe consultar contenido documental obsoleto salvo soporte autorizado o necesidad técnica justificada. |
| RN-OBS-005 | Cuando se publique una nueva versión, esta será visible para los usuarios asignados según permisos.                |

## 13. Reglas sobre copias controladas

| ID         | Regla                                                                      |
| ---------- | -------------------------------------------------------------------------- |
| RN-COP-001 | Toda copia controlada debe estar asociada a un documento.                  |
| RN-COP-002 | Toda copia controlada debe tener número o identificador de copia.          |
| RN-COP-003 | Toda copia controlada debe tener unidad receptora o responsable receptor.  |
| RN-COP-004 | Toda copia controlada debe registrar fecha de entrega.                     |
| RN-COP-005 | Toda copia controlada debe registrar fecha de retiro cuando aplique.       |
| RN-COP-006 | Toda copia controlada debe tener estado.                                   |
| RN-COP-007 | La entrega y retiro de copias controladas debe conservar trazabilidad.     |
| RN-COP-008 | Las copias controladas activas y retiradas deben poder reportarse por OyM. |

## 14. Reglas sobre reportes

| ID         | Regla                                                              |
| ---------- | ------------------------------------------------------------------ |
| RN-REP-001 | Los reportes serán de uso exclusivo de Organización y Métodos.     |
| RN-REP-002 | Los usuarios lectores no tendrán acceso a reportes.                |
| RN-REP-003 | Los reportes deben poder exportarse a formato Excel.               |
| RN-REP-004 | El sistema debe generar el Libro Maestro de Control Documental.    |
| RN-REP-005 | El sistema debe generar el Reporte mensual de Gestión Documental.  |
| RN-REP-006 | El sistema debe reportar documentos vigentes.                      |
| RN-REP-007 | El sistema debe reportar documentos vencidos.                      |
| RN-REP-008 | El sistema debe reportar documentos por vencer.                    |
| RN-REP-009 | El sistema debe reportar documentos obsoletos.                     |
| RN-REP-010 | El sistema debe reportar solicitudes pendientes.                   |
| RN-REP-011 | El sistema debe reportar constancias pendientes.                   |
| RN-REP-012 | El sistema debe reportar copias controladas activas.               |
| RN-REP-013 | El sistema debe reportar copias controladas retiradas.             |
| RN-REP-014 | El sistema debe generar estadísticas por unidad ejecutora.         |
| RN-REP-015 | El sistema debe generar estadísticas por tipo documental.          |
| RN-REP-016 | El sistema debe reportar histórico de modificaciones documentales. |

## 15. Reglas sobre notificaciones

| ID         | Regla                                                                                                                 |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| RN-NOT-001 | El sistema debe notificar documentos pendientes por correo institucional y panel interno.                             |
| RN-NOT-002 | El sistema debe notificar cuando un documento sea asignado para lectura, interpretación, aceptación e implementación. |
| RN-NOT-003 | El sistema debe notificar recordatorios de documentos pendientes.                                                     |
| RN-NOT-004 | El sistema debe notificar cuando se publique una nueva versión que requiera nueva aceptación.                         |
| RN-NOT-005 | El sistema debe notificar solicitudes documentales observadas o devueltas cuando aplique.                             |
| RN-NOT-006 | El sistema debe notificar documentos próximos a vencer cuando aplique.                                                |

## 16. Reglas sobre auditoría

| ID         | Regla                                                                                                 |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| RN-AUD-001 | El sistema debe registrar eventos relevantes del proceso documental.                                  |
| RN-AUD-002 | Todo evento de auditoría debe registrar usuario, acción, fecha y hora del servidor.                   |
| RN-AUD-003 | Todo evento de auditoría debe registrar entidad afectada e identificador del registro cuando aplique. |
| RN-AUD-004 | Todo evento de auditoría debe registrar resultado de la operación.                                    |
| RN-AUD-005 | Debe registrarse inicio y cierre de sesión.                                                           |
| RN-AUD-006 | Debe registrarse creación y modificación de documentos.                                               |
| RN-AUD-007 | Debe registrarse cambio de estado documental.                                                         |
| RN-AUD-008 | Debe registrarse carga de archivos.                                                                   |
| RN-AUD-009 | Debe registrarse visualización de documentos cuando aplique.                                          |
| RN-AUD-010 | Debe registrarse generación de reportes.                                                              |
| RN-AUD-011 | Debe registrarse cambios de permisos, usuario, rol o unidad.                                          |
| RN-AUD-012 | Debe registrarse entrega o retiro de copias controladas.                                              |
| RN-AUD-013 | Debe registrarse emisión de constancias de implementación.                                            |

## 17. Reglas sobre seguridad y operación

| ID         | Regla                                                                                               |
| ---------- | --------------------------------------------------------------------------------------------------- |
| RN-SEG-001 | No deben almacenarse secretos en el repositorio.                                                    |
| RN-SEG-002 | La configuración debe manejarse mediante variables de entorno.                                      |
| RN-SEG-003 | Los documentos deben almacenarse en ubicación persistente y controlada.                             |
| RN-SEG-004 | La base de datos debe tener respaldo y restauración documentados.                                   |
| RN-SEG-005 | El sistema debe separar configuración de desarrollo, pruebas y producción.                          |
| RN-SEG-006 | Los archivos documentales no deben depender del ciclo de vida efímero del contenedor de aplicación. |
| RN-SEG-007 | El acceso a contenido documental debe pasar por controles de autorización.                          |

## 18. Reglas no implementables en el punto 11

Durante el punto 11 solo se debe configurar la base técnica inicial.

No deben implementarse todavía:

* Workflows documentales completos.
* Modelos complejos de documentos y versiones.
* Reglas completas de obsolescencia.
* Reportes finales.
* Exportadores Excel finales.
* Notificaciones finales.
* Visor documental final.
* Automatizaciones avanzadas.
* Lógica completa de copias controladas.
* Lógica completa de constancias de implementación.

Sí puede implementarse en el punto 11:

* Backend Django base.
* Settings por ambiente.
* PostgreSQL por variables de entorno.
* Registro de apps.
* URLs principales.
* Requirements base.
* Dockerfile backend mínimo.
* Custom User con email como username.
* Admin básico de usuario.

