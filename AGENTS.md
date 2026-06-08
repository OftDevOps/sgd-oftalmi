# AGENTS.md - SGD-OFTALMI

## Contexto del proyecto

SGD-OFTALMI es una aplicacion interna para la Gestion Documental administrada por el Departamento de Organizacion y Metodos de Laboratorios Oftalmi.

El MVP excluye al Departamento de Calidad como dueno funcional. Calidad puede aparecer como unidad usuaria o consultora, pero no define el flujo central del sistema en esta fase.

El sistema debe controlar informacion documentada bajo responsabilidad de OyM: solicitudes documentales, codificacion, recepcion, archivo, modificacion, difusion, implementacion, copias controladas, obsolescencia, registros, Libro Maestro y reportes de gestion.

## Principios de trabajo

- Separar ingenieria de software e ingenieria DevOps.
- Priorizar mantenibilidad, trazabilidad, seguridad y operacion interna.
- No implementar reglas de negocio sin referencia documental o requerimiento aprobado.
- No asumir que el prototipo HTML inicial representa la arquitectura final.
- No mezclar procesos propios de Calidad con procesos de OyM salvo que el alcance lo apruebe explicitamente.

## Stack recomendado

Backend:
- Python
- Django
- Django REST Framework si se expone API
- PostgreSQL

Frontend:
- React con Vite o Django Templates segun decision del MVP

Infraestructura:
- Linux
- Docker
- Docker Compose
- Nginx
- Gunicorn
- PostgreSQL
- Backups automatizados

## Modulos backend recomendados

- accounts: usuarios, autenticacion, roles y permisos.
- organizational_units: unidades ejecutoras.
- document_types: tipologias documentales.
- documents: catalogo documental, archivos, versiones, estados y vigencias.
- document_requests: solicitudes de control, modificacion y desincorporacion.
- controlled_copies: entrega, retiro y control de copias controladas.
- implementation_records: constancias de implementacion.
- audit: trazabilidad y eventos del sistema.
- reports: Libro Maestro, reportes mensuales, estadisticas y exportaciones.
- notifications: avisos internos o correo.

## Reglas de diseno backend

- Mantener modelos simples y explicitos.
- Usar services.py para operaciones con efectos.
- Usar selectors.py para consultas reutilizables.
- No poner reglas de negocio complejas directamente en vistas.
- Registrar eventos relevantes en auditoria.
- Evitar eliminacion fisica de documentos; preferir eliminacion logica o cambio de estado.
- Todo documento debe tener estado, version, tipo documental y unidad responsable.
- Todo archivo documental debe preservar trazabilidad basica: usuario, fecha, hash y version.

## Estados documentales base

Usar estos estados como referencia inicial:

- draft
- received
- under_review
- observed
- approved
- published
- active
- expired
- obsolete
- archived

No agregar nuevos estados sin justificarlo en reglas de negocio.

## Reglas para solicitudes documentales

El modulo document_requests debe soportar inicialmente:

- Solicitud de control de nueva informacion documentada.
- Solicitud de modificacion de informacion documentada.
- Solicitud de desincorporacion de informacion documentada obsoleta.
- Registro de recepcion de informacion.
- Solicitud o registro de copias controladas.
- Constancia de implementacion.

## Auditoria

Registrar como minimo:

- Usuario.
- Accion.
- Fecha/hora del servidor.
- Entidad afectada.
- Identificador del registro.
- Direccion IP si esta disponible.
- Resultado de la operacion.
- Datos relevantes antes/despues cuando aplique.

## Reportes minimos

- Libro Maestro de Control Documental.
- Reporte mensual de gestion documental.
- Documentos vigentes.
- Documentos vencidos.
- Documentos por vencer.
- Documentos obsoletos.
- Solicitudes pendientes.
- Constancias pendientes.
- Copias controladas activas.
- Estadisticas por unidad ejecutora.

## DevOps

- Usar variables de entorno; no colocar secretos en codigo.
- Mantener .env.example actualizado.
- Toda dependencia debe estar declarada.
- El entorno local debe poder levantarse con Docker Compose.
- Incluir comandos reproducibles en Makefile.
- Definir scripts para backup y restore.
- Nginx debe servir como reverse proxy.
- PostgreSQL debe tener volumen persistente.
- Los archivos documentales deben estar fuera del contenedor de aplicacion mediante volumen persistente.

## Testing

- Agregar pruebas para modelos criticos.
- Agregar pruebas para reglas de negocio.
- Agregar pruebas para permisos.
- Agregar pruebas para workflows documentales.
- No considerar cerrada una funcionalidad critica sin prueba minima.

## Convenciones

- Usar nombres claros en ingles para carpetas y codigo.
- Documentacion funcional puede estar en espanol.
- Commits claros y pequenos.
- No crear abstracciones innecesarias.
- Priorizar trazabilidad sobre velocidad.
