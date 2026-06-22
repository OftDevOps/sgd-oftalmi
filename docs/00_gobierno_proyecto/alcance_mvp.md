# Alcance MVP - SGD-OFTALMI

## 1. Propósito del documento

Este documento define el alcance funcional inicial del MVP del sistema SGD-OFTALMI.

Su objetivo es establecer qué procesos serán cubiertos en la primera versión del sistema, qué áreas participan, qué límites funcionales deben respetarse y qué reglas generales deben guiar el desarrollo inicial.

Este documento debe ser usado como referencia por el equipo técnico, Codex y cualquier persona que participe en el diseño, desarrollo, pruebas o despliegue del sistema.

## 2. Contexto del sistema

SGD-OFTALMI es una aplicación interna para la Gestión Documental administrada por el Departamento de Organización y Métodos de Laboratorios Oftalmi.

El sistema busca digitalizar y controlar el proceso de gestión documental bajo responsabilidad de Organización y Métodos, manteniendo trazabilidad, control de usuarios, control de versiones, consulta documental, constancias de implementación, reportes y auditoría.

El sistema no reemplaza las metodologías documentales propias del Departamento de Calidad. La Gerencia de Garantía de la Calidad podrá participar como unidad usuaria, consultora o destinataria de documentos cuando aplique, siempre que dichos documentos sean gestionados bajo las premisas metodológicas de Organización y Métodos.

## 3. Dueño funcional del MVP

El dueño funcional del MVP es el Departamento de Organización y Métodos.

Organización y Métodos será responsable de:

* Definir reglas funcionales.
* Validar catálogos documentales.
* Administrar la gestión documental.
* Controlar la carga y registro de documentos.
* Gestionar solicitudes documentales.
* Validar codificación documental.
* Controlar obsolescencia y desincorporación.
* Generar reportes.
* Validar criterios de implementación documental.

Sistemas será responsable de:

* Plataforma técnica.
* Infraestructura.
* Configuración.
* Despliegue.
* Soporte.
* Operación.
* Respaldo y restauración.
* Monitoreo.
* Seguridad técnica.

Sistemas también podrá actuar como unidad usuaria cuando corresponda, pero no será dueño de las reglas funcionales de gestión documental.

## 4. Alcance funcional del MVP

El MVP estará centrado en los siguientes procesos:

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
* Notificaciones internas y por correo institucional.
* Consulta documental controlada para usuarios asignados.

## 5. Funcionalidades incluidas

### 5.1 Gestión de usuarios y acceso

El sistema debe permitir la gestión de usuarios internos.

El identificador principal del usuario será el correo electrónico institucional.

El username del sistema será el correo electrónico.

El sistema debe contemplar roles y permisos diferenciados para:

* Organización y Métodos.
* Sistemas.
* Unidad Ejecutora.
* Usuario lector.
* Otros roles que sean aprobados formalmente.

### 5.2 Gestión de unidades ejecutoras

El sistema debe permitir registrar y administrar unidades ejecutoras.

Las unidades ejecutoras podrán:

* Solicitar control documental.
* Solicitar modificación documental.
* Solicitar desincorporación cuando aplique.
* Consultar documentos asignados.
* Confirmar lectura, interpretación, aceptación e implementación.
* Recibir notificaciones.

### 5.3 Catálogo documental

El sistema debe permitir registrar información documentada con, al menos:

* Código documental.
* Nombre o título del documento.
* Tipo documental.
* Unidad ejecutora responsable.
* Versión o revisión.
* Estado documental.
* Fecha de emisión.
* Fecha de vigencia.
* Fecha de vencimiento si aplica.
* Archivo digital.
* Responsable.
* Observaciones.
* Trazabilidad básica.

### 5.4 Codificación documental

El sistema debe permitir registrar, validar o asistir la codificación documental según las reglas aprobadas por Organización y Métodos.

La codificación correcta confirmada para Registro de Recepción de Información es:

```text
FOR-GGHD-010
```

Debe evitarse el uso incorrecto del código:

```text
FOR-HHGD-010
```

### 5.5 Solicitudes documentales

El MVP debe contemplar inicialmente:

* Solicitud de control de nueva información documentada.
* Solicitud de modificación de información documentada.
* Solicitud de desincorporación de información documentada obsoleta.
* Registro de recepción de información.
* Solicitud o registro de copias controladas.
* Registro de constancias de implementación.

### 5.6 Modificación documental

El sistema debe permitir registrar solicitudes de modificación documental y asociarlas a documentos existentes.

Una nueva versión aprobada debe generar una nueva obligación de lectura, interpretación, aceptación e implementación para los usuarios asignados.

### 5.7 Difusión e implementación

El sistema debe permitir asignar documentos a usuarios o unidades ejecutoras para consulta e implementación.

Los usuarios asignados deberán confirmar:

* Lectura.
* Interpretación.
* Aceptación.
* Implementación.

El sistema debe generar una constancia de implementación una vez completado el proceso.

### 5.8 Consulta documental controlada

Los usuarios lectores solo podrán visualizar documentos asignados o aplicables.

Los usuarios lectores no podrán:

* Copiar documentos desde la aplicación.
* Imprimir documentos desde la aplicación.
* Descargar documentos desde la aplicación.

Estas restricciones deben implementarse mediante controles razonables de aplicación, permisos backend, visor documental, no exposición directa del archivo, marcas de agua y auditoría.

No deben presentarse como una protección absoluta frente a capturas de pantalla u otros mecanismos externos.

### 5.9 Obsolescencia y desincorporación

Los documentos obsoletos no deben ser visibles para usuarios lectores generales.

Los documentos obsoletos deben permanecer en el sistema para control interno hasta que Organización y Métodos ejecute su desincorporación formal.

Organización y Métodos podrá consultar documentos obsoletos para fines de control, auditoría y trazabilidad.

### 5.10 Copias controladas

El sistema debe contemplar el control de copias controladas, incluyendo como mínimo:

* Documento asociado.
* Número de copia.
* Unidad receptora.
* Responsable receptor.
* Fecha de entrega.
* Fecha de retiro cuando aplique.
* Estado de la copia.
* Observaciones.
* Evidencia o registro asociado.

### 5.11 Libro Maestro de Control Documental

El sistema debe permitir generar o consultar el Libro Maestro de Control Documental.

El Libro Maestro debe reflejar la información documental vigente, controlada, obsoleta y trazable según las reglas de Organización y Métodos.

### 5.12 Reportes

Los reportes serán de uso exclusivo de Organización y Métodos.

Los usuarios lectores no tendrán acceso a reportes.

Los reportes deben poder exportarse a formato Excel.

Reportes mínimos del MVP:

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

### 5.13 Auditoría y trazabilidad

El sistema debe registrar eventos relevantes del proceso documental.

Como mínimo debe auditar:

* Inicio de sesión.
* Cierre de sesión.
* Creación de documento.
* Modificación de documento.
* Cambio de estado documental.
* Carga de archivo.
* Visualización de documento.
* Registro de solicitud.
* Aprobación o rechazo de solicitud.
* Registro de constancia de implementación.
* Entrega o retiro de copia controlada.
* Generación de reportes.
* Cambios de permisos.
* Cambios de usuario, rol o unidad.

### 5.14 Notificaciones

El sistema debe contemplar notificaciones internas y por correo electrónico institucional.

Eventos mínimos para notificar:

* Documento asignado para lectura, interpretación, aceptación e implementación.
* Recordatorio de documento pendiente de aceptación.
* Nueva versión publicada que requiere nueva aceptación.
* Solicitud documental observada o devuelta.
* Solicitud documental procesada.
* Documento próximo a vencer, cuando aplique.

## 6. Fuera del alcance inicial

Queda fuera del MVP:

* Procesos propios del Departamento de Calidad que no estén bajo metodología de Organización y Métodos.
* Firma electrónica avanzada o certificada.
* Integración con Active Directory o LDAP, salvo decisión técnica posterior.
* Gestión documental externa fuera del alcance de OyM.
* Automatizaciones complejas de workflow no validadas.
* Reportería avanzada no solicitada por OyM.
* Edición colaborativa de documentos en línea.
* Control absoluto contra capturas de pantalla.
* Inteligencia artificial para clasificación documental.
* Integraciones con ERP u otros sistemas corporativos.
* Gestión documental de clientes o proveedores externos, salvo requerimiento posterior.

## 7. Reglas funcionales generales

* Organización y Métodos es el administrador funcional del sistema.
* Sistemas es administrador técnico de plataforma y puede ser unidad usuaria.
* Calidad no es dueño funcional del flujo del MVP.
* Los usuarios lectores solo pueden consultar documentos asignados.
* Los usuarios lectores no tendrán acceso a reportes.
* Los usuarios lectores no podrán descargar, imprimir ni copiar documentos desde la aplicación.
* Toda aceptación de lectura e implementación se controla por usuario, documento y versión.
* Una nueva versión publicada genera nueva obligación de aceptación.
* Los documentos obsoletos no son visibles para usuarios lectores.
* Los documentos obsoletos permanecen en el sistema hasta desincorporación formal por OyM.
* Los reportes son exclusivos de OyM y exportables a Excel.
* El usuario de acceso será el correo electrónico institucional.
* No deben implementarse reglas de negocio no validadas por OyM.

## 8. Criterio de avance al punto 11

Con este alcance validado, se puede avanzar a la configuración técnica inicial del backend Django.

El punto 11 debe limitarse a:

* Configurar Django base.
* Configurar settings `base`, `dev`, `test` y `prod`.
* Configurar PostgreSQL por variables de entorno.
* Registrar apps existentes.
* Configurar URLs principales.
* Preparar requirements.
* Preparar Dockerfile backend mínimo.
* Configurar `CustomUser` usando correo electrónico institucional como `USERNAME_FIELD`.
* Preparar admin básico de usuario.
* Validar que `manage.py` funcione.

El punto 11 no debe incluir todavía:

* Workflows documentales completos.
* Modelos documentales complejos.
* Reportes finales.
* Automatizaciones complejas.
* Reglas funcionales no validadas.

