# Validaciones OyM - Levantamiento de Información SGD-OFTALMI

## 1. Propósito del documento

Este documento registra las validaciones funcionales emitidas por el Departamento de Organización y Métodos en respuesta a las observaciones realizadas sobre el levantamiento de información del proyecto SGD-OFTALMI.

Su objetivo es dejar trazabilidad sobre las decisiones funcionales confirmadas antes de avanzar con la configuración técnica inicial del backend y el diseño detallado del MVP.

## 2. Contexto

Luego de revisar la matriz de levantamiento de información suministrada por Organización y Métodos, se identificaron puntos que requerían confirmación funcional.

Las validaciones recibidas permiten consolidar el alcance inicial del MVP y establecer reglas de negocio base para el sistema.

Los documentos base derivados del levantamiento son:

* Alcance funcional MVP validado.
* Backlog inicial de requerimientos.
* Modelo preliminar de datos y permisos.

Organización y Métodos indicó que estos documentos serán revisados y devueltos con observaciones cuando culmine su validación interna.

## 3. Confirmación del alcance del MVP

Organización y Métodos confirmó que el alcance inicial del sistema estará centrado en los siguientes procesos:

* Codificación documental.
* Solicitudes documentales.
* Recepción, control y archivo.
* Modificación documental.
* Difusión e implementación.
* Desincorporación u obsolescencia documental.
* Copias controladas.
* Constancias de implementación.
* Libro Maestro de Control Documental.
* Reporte mensual de Gestión Documental.
* Auditoría y trazabilidad.

## 4. Alcance para usuarios de Unidades Ejecutoras

Organización y Métodos precisó que, a nivel de usuarios de las diferentes Unidades Ejecutoras, el sistema será principalmente de consulta y confirmación de implementación y lectura.

Los usuarios de las Unidades Ejecutoras:

* Podrán visualizar documentos asignados o aplicables.
* No podrán copiar documentos.
* No podrán imprimir documentos.
* No podrán descargar documentos.
* Deberán confirmar lectura, aceptación e implementación de los documentos que les correspondan.
* Recibirán documentos asignados al momento del control documental.

## 5. Gerencia de Garantía de la Calidad

Organización y Métodos confirmó que la Gerencia de Garantía de la Calidad no será dueña funcional del sistema.

La Gerencia de Garantía de la Calidad será tratada como una unidad usuaria, al igual que el resto de las Unidades Ejecutoras de Laboratorios L.O. Oftalmi, C.A., siempre que presente documentos para ser controlados bajo las premisas metodológicas del Sistema de Gestión Documental administrado por Organización y Métodos.

Las metodologías de elaboración, control y difusión de información documentada utilizadas por la Gerencia de Garantía de la Calidad son diferentes a las planteadas por Organización y Métodos, por lo tanto no aplican para este sistema.

El administrador responsable del sistema será el personal de Organización y Métodos, encargado de los registros y carga de documentos en el sistema.

## 6. Validación de codificación documental

Se identificó una posible inconsistencia en el código:

```text
FOR-HHGD-010 - Registro de Recepción de Información
```

Organización y Métodos confirmó que el código correcto es:

```text
FOR-GGHD-010
```

Por tanto, debe evitarse el uso de:

```text
FOR-HHGD-010
```

## 7. Validación de documento duplicado

Se observó que el documento `DOC-GGHD-004` aparecía duplicado o con descripciones similares dentro de la información suministrada.

Organización y Métodos confirmó que la duplicidad corresponde a un error involuntario.

Criterio validado:

* Mantener una sola entrada válida para `DOC-GGHD-004`.
* Eliminar o ignorar el registro duplicado.
* No tratarlo como dos documentos distintos.

## 8. Validación del rol Sistemas

Organización y Métodos confirmó que la unidad de Soporte y Desarrollo Tecnológico, Sistemas, tendrá una doble naturaleza dentro del proyecto:

1. Unidad usuaria.
2. Responsable técnico de plataforma.

Como responsable técnico, Sistemas administrará:

* Plataforma técnica.
* Infraestructura.
* Despliegue.
* Soporte.
* Operación.

Sistemas deberá aplicar las reglas funcionales establecidas por Organización y Métodos.

Criterio funcional:

* Sistemas puede administrar técnicamente la plataforma.
* Sistemas puede ser unidad usuaria cuando corresponda.
* Sistemas no es dueño funcional de las reglas de Gestión Documental de OyM.
* Sistemas no debe modificar catálogos o reglas funcionales de OyM sin autorización formal.

## 9. Validación sobre documentos obsoletos

Organización y Métodos confirmó el siguiente comportamiento:

* Los documentos obsoletos dejarán de visualizarse a los usuarios del sistema.
* Cuando se coloque una nueva versión del documento, esta será visible nuevamente a los usuarios asignados.
* Los documentos obsoletos saldrán del sistema únicamente cuando el personal de Organización y Métodos los desincorpore.

Criterio funcional consolidado:

| Rol                         | Acceso a documentos obsoletos                                |
| --------------------------- | ------------------------------------------------------------ |
| Usuarios lectores generales | No                                                           |
| Unidades Ejecutoras         | No, salvo criterio definido por OyM                          |
| Organización y Métodos      | Sí, para control, auditoría y trazabilidad                   |
| Sistemas                    | No al contenido documental, salvo soporte técnico autorizado |
| Auditoría                   | Solo si se define rol auditor                                |

## 10. Validación de lectura e implementación por versión

Organización y Métodos confirmó que la regla de lectura e implementación por versión es correcta.

Regla validada:

* El usuario lector debe aceptar lectura, interpretación, aceptación e implementación de un documento una sola vez por versión.
* Si el usuario ya aceptó la versión vigente, el sistema no debe volver a solicitar aceptación para esa misma versión.
* Si se publica una nueva versión, el sistema debe generar nuevamente la obligación de lectura, interpretación, aceptación e implementación.

Organización y Métodos también precisó que la validación debe aparecer siempre que el usuario no haya leído, interpretado, validado e implementado el documento.

El sistema deberá emitir una constancia de implementación al usuario correspondiente luego de completar el proceso.

## 11. Alertas y notificaciones

Organización y Métodos confirmó que los usuarios deberán recibir alertas sobre documentos pendientes por lectura, aceptación e implementación.

Canales requeridos:

* Correo electrónico institucional.
* Panel interno de notificaciones.

Eventos mínimos asociados:

* Documento pendiente de lectura.
* Documento pendiente de aceptación.
* Documento pendiente de implementación.
* Nueva versión que requiere nueva aceptación.
* Recordatorio de documentos pendientes.

## 12. Validación de reportes mínimos

Organización y Métodos validó los reportes mínimos del MVP:

* Libro Maestro de Control Documental.
* Reporte mensual de Gestión Documental.
* Documentos vigentes.
* Documentos vencidos.
* Documentos por vencer.
* Documentos obsoletos.
* Solicitudes pendientes.
* Constancias pendientes.
* Copias controladas activas.
* Copias controladas retiradas.
* Estadísticas por unidad ejecutora.
* Estadísticas por tipo documental.
* Histórico de modificaciones documentales.

Además, Organización y Métodos confirmó que:

* Los reportes deberán poder exportarse a formato Excel.
* Los reportes serán para uso del personal de Organización y Métodos.
* Los usuarios no tendrán acceso a reportes.

## 13. Validación de identidad de usuario

Organización y Métodos confirmó que el usuario de acceso será el correo electrónico institucional.

Regla validada:

```text
El username del sistema será el correo electrónico institucional del usuario.
```

Esta regla será la premisa de registro y acceso al sistema.

Los perfiles de usuarios serán definidos en conjunto con el personal técnico de Sistemas.

## 14. Reglas consolidadas derivadas de la validación

A partir de la respuesta de Organización y Métodos, se consolidan las siguientes reglas funcionales:

| ID          | Regla                                                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| RN-OYM-001  | Organización y Métodos es el dueño funcional del MVP.                                                                                  |
| RN-OYM-002  | Calidad podrá participar como unidad usuaria, pero no define el flujo funcional del sistema.                                           |
| RN-USR-001  | Los usuarios lectores solo podrán visualizar documentos asignados o aplicables.                                                        |
| RN-USR-002  | Los usuarios lectores no podrán copiar, imprimir ni descargar documentos desde la aplicación.                                          |
| RN-USR-003  | Los usuarios lectores deberán confirmar lectura, interpretación, aceptación e implementación.                                          |
| RN-AUTH-001 | El username será el correo electrónico institucional.                                                                                  |
| RN-DOC-001  | El código correcto para Registro de Recepción de Información es FOR-GGHD-010.                                                          |
| RN-DOC-002  | DOC-GGHD-004 debe mantenerse como única entrada, eliminando duplicados.                                                                |
| RN-ROL-001  | Sistemas podrá administrar técnicamente la plataforma y actuar como unidad usuaria, pero no será dueño funcional de las reglas de OyM. |
| RN-OBS-001  | Los documentos obsoletos no serán visibles para usuarios lectores.                                                                     |
| RN-OBS-002  | Los documentos obsoletos permanecerán en el sistema hasta desincorporación formal por OyM.                                             |
| RN-IMP-001  | La aceptación se controla por usuario, documento y versión.                                                                            |
| RN-IMP-002  | Una nueva versión genera nueva obligación de lectura, aceptación e implementación.                                                     |
| RN-NOT-001  | El sistema notificará pendientes por correo institucional y panel interno.                                                             |
| RN-REP-001  | Los reportes serán exclusivos de OyM.                                                                                                  |
| RN-REP-002  | Los reportes deberán exportarse a Excel.                                                                                               |

## 15. Impacto en el diseño técnico

Estas validaciones impactan directamente:

* Modelo de usuario.
* Custom User con email como username.
* Modelo de roles y permisos.
* Modelo de documentos.
* Modelo de versiones documentales.
* Modelo de constancias de implementación.
* Modelo de notificaciones.
* Modelo de reportes.
* Exportadores Excel.
* Auditoría.
* Restricciones del visor documental.
* Control de documentos obsoletos.
* Separación entre administrador funcional OyM y administrador técnico Sistemas.

## 16. Criterio de avance

Con estas validaciones se puede avanzar al punto 11, limitado a configuración técnica inicial.

El punto 11 puede incluir:

* Configuración Django base.
* Settings por ambiente.
* PostgreSQL por variables de entorno.
* Registro de apps existentes.
* URLs principales.
* Dockerfile backend mínimo.
* Custom User usando correo institucional como username.
* Admin básico para usuario.
* Validación de ejecución de `manage.py`.

El punto 11 no debe incluir todavía:

* Workflows documentales completos.
* Modelos complejos de documentos y versiones.
* Reportes finales.
* Automatizaciones avanzadas.
* Reglas funcionales no validadas.

