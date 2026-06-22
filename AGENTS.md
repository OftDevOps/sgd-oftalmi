# AGENTS.md - SGD-OFTALMI

## Contexto del proyecto

SGD-OFTALMI es una aplicación interna para la Gestión Documental administrada por el Departamento de Organización y Métodos de Laboratorios Oftalmi.

El MVP excluye al Departamento de Calidad como dueño funcional. La Gerencia de Garantía de la Calidad puede participar como unidad usuaria, consultora o destinataria de información cuando aplique, siempre que los documentos ingresen al sistema bajo las premisas metodológicas de Organización y Métodos.

El sistema debe controlar información documentada bajo responsabilidad de Organización y Métodos: solicitudes documentales, codificación, recepción, archivo, modificación, difusión, implementación, copias controladas, obsolescencia, registros, Libro Maestro y reportes de gestión.

El administrador funcional del sistema será Organización y Métodos. Sistemas será responsable de la plataforma técnica, infraestructura, despliegue, soporte y operación, y también podrá actuar como unidad usuaria cuando corresponda.

## Objetivo del MVP

Construir una base funcional y técnica para digitalizar el proceso de Gestión Documental de Organización y Métodos, manteniendo trazabilidad, control documental, seguridad por roles, consulta controlada, reportes y operación interna sobre infraestructura administrada por Sistemas.

El MVP debe permitir avanzar de forma controlada desde la gestión documental manual hacia una plataforma interna con base de datos, control de usuarios, trazabilidad, documentos controlados, constancias de implementación, reportes y operación reproducible.

## Límites del alcance inicial

No implementar procesos propios del Departamento de Calidad salvo que sean definidos explícitamente como requerimiento aprobado por Organización y Métodos.

No asumir que el prototipo HTML inicial representa la arquitectura final del sistema.

No implementar reglas de negocio sin referencia en documentos de Organización y Métodos, matriz de levantamiento, requerimiento aprobado o decisión registrada.

No construir funcionalidades fuera del MVP sin documentar la justificación.

No permitir que Sistemas modifique reglas funcionales, catálogos documentales o decisiones de negocio propias de Organización y Métodos, salvo autorización formal.

## Principios de trabajo

* Separar Ingeniería de Software e Ingeniería DevOps.
* Priorizar mantenibilidad, trazabilidad, seguridad y operación interna.
* Mantener el código modular, explícito y fácil de auditar.
* Preferir decisiones simples antes que abstracciones innecesarias.
* Registrar decisiones técnicas relevantes en la documentación del proyecto.
* Mantener consistencia entre código, documentación y estructura del repositorio.
* No guardar secretos, credenciales ni archivos sensibles en el repositorio.
* No mezclar procesos propios de Calidad con procesos de Organización y Métodos salvo que el alcance lo apruebe explícitamente.

## Metodología de trabajo: Ingeniería de Software + Ingeniería DevOps

El desarrollo del SGD-OFTALMI debe abordarse mediante dos líneas de trabajo obligatorias y coordinadas: Ingeniería de Software e Ingeniería DevOps.

Estas dos líneas no deben trabajarse de forma aislada. Cada funcionalidad desarrollada debe considerar análisis funcional, diseño técnico, implementación, pruebas, despliegue, operación, monitoreo y mantenimiento.

### Línea de Ingeniería de Software

La Ingeniería de Software gobierna el ciclo de construcción de la aplicación.

Debe asegurar que cada funcionalidad esté respaldada por:

* Alcance aprobado.
* Requerimiento funcional o no funcional documentado.
* Regla de negocio identificada.
* Diseño funcional.
* Diseño técnico.
* Modelo de datos cuando aplique.
* Pruebas mínimas.
* Trazabilidad hacia documentos o matrices de Organización y Métodos.
* Documentación actualizada.

El flujo recomendado para cualquier funcionalidad es:

```text
Documento normativo / levantamiento OyM
→ requerimiento
→ regla de negocio
→ diseño funcional
→ diseño técnico
→ implementación
→ prueba
→ revisión
→ documentación
→ entrega
```

No debe implementarse una funcionalidad si no está claro:

* Qué problema resuelve.
* Qué usuario o rol la utilizará.
* Qué proceso de Organización y Métodos soporta.
* Qué datos captura o modifica.
* Qué reglas de negocio aplica.
* Qué eventos deben auditarse.
* Qué impacto tiene en reportes o trazabilidad.

### Línea de Ingeniería DevOps

La Ingeniería DevOps gobierna la plataforma, despliegue, operación, seguridad operativa y continuidad del sistema.

Debe asegurar que cada componente desarrollado pueda ejecutarse, desplegarse, monitorearse y respaldarse de forma controlada.

Todo cambio técnico debe considerar:

* Configuración por variables de entorno.
* Compatibilidad con Docker Compose.
* Persistencia de base de datos y archivos.
* Separación entre entorno local, pruebas y producción.
* Logs útiles para diagnóstico.
* Scripts reproducibles.
* Backups y restauración.
* Seguridad de secretos.
* Health checks.
* Monitoreo básico.
* Procedimiento de rollback cuando aplique.

El flujo recomendado para operación e implementación es:

```text
Código versionado
→ pruebas locales
→ build de contenedores
→ migraciones controladas
→ despliegue en ambiente de prueba
→ validación funcional
→ respaldo previo
→ despliegue en producción
→ verificación post-deploy
→ monitoreo
→ registro de cambios
```

No debe considerarse terminada una funcionalidad si no puede:

* Ejecutarse en ambiente local.
* Desplegarse de forma reproducible.
* Registrar errores relevantes.
* Conservar datos persistentes.
* Ser respaldada o restaurada si afecta información crítica.
* Ser monitoreada mínimamente.

### Coordinación entre ambas líneas

Cada cambio debe evaluarse desde ambas perspectivas:

| Pregunta                                        | Línea responsable      |
| ----------------------------------------------- | ---------------------- |
| ¿Qué proceso de Organización y Métodos soporta? | Ingeniería de Software |
| ¿Qué regla de negocio aplica?                   | Ingeniería de Software |
| ¿Qué modelos, servicios o endpoints requiere?   | Ingeniería de Software |
| ¿Qué pruebas validan el cambio?                 | Ingeniería de Software |
| ¿Cómo se configura?                             | DevOps                 |
| ¿Cómo se despliega?                             | DevOps                 |
| ¿Cómo se respalda la información afectada?      | DevOps                 |
| ¿Cómo se monitorea?                             | DevOps                 |
| ¿Cómo se revierte si falla?                     | DevOps                 |

### Criterio de cierre de una funcionalidad

Una funcionalidad solo se considera cerrada cuando cumple estos criterios mínimos:

* Está vinculada a un requerimiento o regla de negocio.
* Tiene implementación en el módulo correspondiente.
* Tiene validaciones y permisos definidos.
* Registra auditoría si modifica o consulta información crítica.
* Tiene pruebas mínimas.
* No rompe la estructura modular del proyecto.
* No introduce secretos ni dependencias no justificadas.
* Puede ejecutarse en el entorno local.
* Puede desplegarse mediante el flujo definido.
* Tiene documentación actualizada cuando aplica.

## Stack recomendado

Backend:

* Python
* Django
* Django REST Framework si se expone API
* PostgreSQL

Frontend:

* React con Vite o Django Templates, según decisión técnica del MVP

Infraestructura:

* Linux
* Docker
* Docker Compose
* Nginx
* Gunicorn
* PostgreSQL
* Volúmenes persistentes
* Backups automatizados

## Estructura práctica inicial

```text
sgd-oftalmi/
├── AGENTS.md
├── README.md
├── CHANGELOG.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docker-compose.override.yml
├── Makefile
│
├── docs/
│   ├── 00_gobierno_proyecto/
│   ├── 01_levantamiento_oym/
│   ├── 02_requerimientos/
│   ├── 03_diseno_funcional/
│   ├── 04_diseno_tecnico/
│   └── 05_operacion/
│
├── backend/
│   ├── config/
│   ├── apps/
│   ├── requirements/
│   ├── static/
│   ├── media/
│   ├── templates/
│   └── locale/
│
├── frontend/
│   └── src/
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   ├── postgres/
│   ├── scripts/
│   └── systemd/
│
├── storage/
├── backups/
├── tests/
└── ci_cd/
```

## Módulos backend recomendados

* `accounts`: usuarios, autenticación, roles y permisos.
* `organizational_units`: unidades ejecutoras.
* `document_types`: tipologías documentales.
* `documents`: catálogo documental, archivos, versiones, estados y vigencias.
* `document_requests`: solicitudes de control, modificación y desincorporación.
* `controlled_copies`: entrega, retiro y control de copias controladas.
* `implementation_records`: constancias de implementación.
* `audit`: trazabilidad y eventos del sistema.
* `reports`: Libro Maestro, reportes mensuales, estadísticas y exportaciones.
* `notifications`: avisos internos o correo.

## Reglas de identidad y autenticación

El username del sistema será el correo electrónico institucional del usuario.

Se debe implementar un `CustomUser` desde el inicio del proyecto Django.

El campo `email` debe ser único y debe utilizarse como `USERNAME_FIELD`.

No usar el modelo de usuario por defecto de Django si implica mantener `username` tradicional como identificador principal.

El módulo `accounts` debe contemplar:

* Usuario con correo único.
* Nombre.
* Apellido.
* Unidad ejecutora.
* Estado activo/inactivo.
* Rol o grupo de permisos.
* Indicador de usuario técnico cuando aplique.
* Auditoría de creación y modificación cuando aplique.

## Reglas de diseño backend

* Mantener modelos simples y explícitos.
* Usar `services.py` para operaciones con efectos de negocio.
* Usar `selectors.py` para consultas reutilizables.
* Usar `permissions.py` para reglas de acceso.
* No colocar reglas de negocio complejas directamente en vistas.
* No colocar consultas complejas repetidas en múltiples vistas.
* Registrar eventos relevantes en auditoría.
* Evitar eliminación física de documentos; preferir eliminación lógica o cambio de estado.
* Todo documento debe tener estado, versión, tipo documental y unidad responsable.
* Todo archivo documental debe preservar trazabilidad básica: usuario, fecha, hash y versión.
* Todo cambio crítico debe quedar asociado al usuario que lo ejecutó.

## Estados documentales base

Usar estos estados como referencia inicial:

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

No agregar nuevos estados sin justificarlo en reglas de negocio o documentación funcional.

## Reglas para solicitudes documentales

El módulo `document_requests` debe soportar inicialmente:

* Solicitud de control de nueva información documentada.
* Solicitud de modificación de información documentada.
* Solicitud de desincorporación de información documentada obsoleta.
* Registro de recepción de información.
* Solicitud o registro de copias controladas.
* Constancia de implementación.

Las solicitudes deben tener estado, solicitante, unidad ejecutora, fecha, tipo de solicitud, documento relacionado cuando aplique, observaciones, evidencias y trazabilidad.

## Reglas para usuarios lectores

Los usuarios lectores de las diferentes Unidades Ejecutoras tendrán uso principalmente de consulta e implementación.

Los usuarios lectores:

* Solo podrán visualizar documentos asignados o aplicables.
* No podrán copiar documentos desde la aplicación.
* No podrán imprimir documentos desde la aplicación.
* No podrán descargar documentos desde la aplicación.
* Deberán confirmar lectura, interpretación, aceptación e implementación de los documentos asignados.
* Recibirán alertas por correo o por panel de notificaciones sobre documentos pendientes.
* Recibirán constancia de implementación una vez completada la aceptación correspondiente.

Nota técnica: las restricciones de copiar, imprimir y descargar deben implementarse mediante controles razonables de aplicación, permisos backend, visor documental, no exposición directa del archivo, marcas de agua y auditoría. No deben presentarse como protección absoluta frente a capturas de pantalla u otros mecanismos externos.

## Reglas para lectura e implementación por versión

La constancia de lectura, interpretación, aceptación e implementación se controla por usuario, documento y versión.

Si el usuario ya aceptó una versión vigente, el sistema no debe volver a solicitar aceptación para esa misma versión.

Si se publica una nueva versión, el sistema debe generar nuevamente la obligación de lectura, interpretación, aceptación e implementación para los usuarios asignados.

El modelo de constancia debe contemplar, como mínimo:

* Usuario.
* Documento.
* Versión del documento.
* Fecha de asignación.
* Fecha de lectura.
* Fecha de aceptación.
* Fecha de implementación.
* Estado.
* Número o identificador de constancia.
* Fecha de generación de constancia.
* Metadatos de evidencia.

## Reglas para documentos obsoletos

Un documento obsoleto no debe ser visible para usuarios lectores generales.

Los documentos obsoletos deben permanecer en el sistema para control interno hasta que Organización y Métodos ejecute su desincorporación formal.

Organización y Métodos podrá consultar documentos obsoletos para fines de control, auditoría y trazabilidad.

Sistemas no debe consultar contenido documental obsoleto salvo soporte autorizado o necesidad técnica justificada.

## Auditoría

Registrar como mínimo:

* Usuario.
* Acción.
* Fecha y hora del servidor.
* Entidad afectada.
* Identificador del registro.
* Dirección IP si está disponible.
* Resultado de la operación.
* Datos relevantes antes y después cuando aplique.
* Módulo de origen.
* Descripción legible del evento.

Eventos mínimos a auditar:

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

## Reportes mínimos

Los reportes serán de uso exclusivo de Organización y Métodos. Los usuarios lectores no tendrán acceso a reportes.

Los reportes deben poder exportarse a formato Excel.

Reportes mínimos:

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

## Notificaciones

El sistema debe contemplar notificaciones internas y por correo electrónico institucional.

Eventos mínimos para notificar:

* Documento asignado para lectura, interpretación, aceptación e implementación.
* Recordatorio de documento pendiente de aceptación.
* Nueva versión publicada que requiere nueva aceptación.
* Solicitud documental observada o devuelta.
* Solicitud documental procesada.
* Documento próximo a vencer, cuando aplique.
* Reportes o tareas pendientes para Organización y Métodos, cuando aplique.

## DevOps

* Usar variables de entorno; no colocar secretos en código.
* Mantener `.env.example` actualizado.
* Toda dependencia debe estar declarada.
* El entorno local debe poder levantarse con Docker Compose.
* Incluir comandos reproducibles en `Makefile`.
* Definir scripts para backup y restore.
* Nginx debe servir como reverse proxy.
* PostgreSQL debe tener volumen persistente.
* Los archivos documentales deben estar fuera del contenedor de aplicación mediante volumen persistente.
* No versionar `.env`, respaldos reales, archivos cargados por usuarios ni documentos sensibles.
* Separar configuración de desarrollo, pruebas y producción.
* Mantener logs suficientes para diagnóstico.
* Incluir health checks cuando aplique.
* Documentar pasos de despliegue, rollback, backup y restore.

## Testing

* Agregar pruebas para modelos críticos.
* Agregar pruebas para reglas de negocio.
* Agregar pruebas para permisos.
* Agregar pruebas para workflows documentales.
* Agregar pruebas para auditoría.
* No considerar cerrada una funcionalidad crítica sin prueba mínima.
* Evitar pruebas dependientes de datos locales no versionados.

## Documentación

La documentación funcional puede estar en español.

Mantener actualizados estos documentos cuando se tomen decisiones relevantes:

* `docs/00_gobierno_proyecto/alcance_mvp.md`
* `docs/00_gobierno_proyecto/decisiones_arquitectura.md`
* `docs/01_levantamiento_oym/validaciones_oym.md`
* `docs/02_requerimientos/requerimientos_funcionales.md`
* `docs/02_requerimientos/requerimientos_no_funcionales.md`
* `docs/02_requerimientos/reglas_negocio.md`
* `docs/02_requerimientos/backlog_mvp.md`
* `docs/03_diseno_funcional/roles_permisos.md`
* `docs/04_diseno_tecnico/arquitectura_aplicacion.md`
* `docs/04_diseno_tecnico/modelo_datos.md`
* `docs/04_diseno_tecnico/seguridad.md`
* `docs/04_diseno_tecnico/auditoria.md`
* `docs/04_diseno_tecnico/custom_user_email.md`
* `docs/05_operacion/despliegue.md`
* `docs/05_operacion/backup_restore.md`
* `docs/05_operacion/monitoreo.md`

## Convenciones

* Usar nombres claros en inglés para carpetas, módulos y código.
* Usar español para documentación funcional y decisiones de negocio.
* Usar commits claros, pequeños y descriptivos.
* No crear abstracciones innecesarias.
* Priorizar trazabilidad sobre velocidad.
* No introducir dependencias sin justificación.
* No modificar estructura base sin mantener consistencia con este archivo.
* No usar force push sin autorización explícita.
* No subir datos reales sensibles al repositorio.

## Reglas para Codex

Antes de modificar el código:

1. Revisar este `AGENTS.md`.
2. Revisar `README.md`.
3. Revisar la estructura actual del repositorio.
4. Revisar la documentación funcional relevante.
5. Identificar el módulo afectado.
6. Evitar cambios fuera del alcance solicitado.
7. Explicar brevemente los archivos modificados.
8. No inventar reglas de negocio.
9. No sobrescribir documentación funcional sin indicarlo.
10. No usar secretos ni credenciales reales.
11. No hacer force push ni operaciones destructivas sin autorización.

Codex debe respetar el ciclo completo de desarrollo e implementación:

```text
analizar → diseñar → implementar → probar → documentar → desplegar → monitorear
```

No debe limitarse a escribir código. Cuando una tarea impacte la plataforma, debe considerar también configuración, contenedores, variables de entorno, scripts, persistencia, logs, backup, despliegue y monitoreo.

Para cada cambio relevante, Codex debe responder indicando:

* Qué se modificó.
* Por qué se modificó.
* Cómo se prueba.
* Cómo se ejecuta.
* Si requiere migraciones.
* Si requiere variables de entorno.
* Si impacta Docker, Nginx, PostgreSQL, storage, backups o despliegue.
* Qué queda pendiente.

## Primer objetivo técnico recomendado

Configurar el backend Django inicial sin implementar reglas de negocio documentales completas todavía.

Debe incluir:

* `manage.py` funcional.
* Settings `base`, `dev`, `test` y `prod`.
* Dependencias base.
* Configuración PostgreSQL por variables de entorno.
* Apps instaladas.
* URLs principales.
* Dockerfile backend mínimo.
* Docker Compose funcional para backend y base de datos.
* `CustomUser` usando correo electrónico institucional como `USERNAME_FIELD`.
* Admin básico para usuario.
* Migración inicial del usuario personalizado si aplica.

No debe incluir todavía:

* Workflows documentales completos.
* Modelos complejos de documentos, versiones, copias o constancias.
* Reglas funcionales no validadas.
* Reportes finales.
* Automatizaciones de producción no documentadas.

