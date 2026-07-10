# Plan Tecnico de Piloto Controlado - SGD-OFTALMI

## 1. Objetivo del piloto

Preparar un piloto tecnico controlado del SGD-OFTALMI para validar, con Organizacion y Metodos, la operacion interna del MVP construido hasta Fase 4.

Este documento no inicia el piloto. Define las condiciones tecnicas, funcionales y operativas que deben cumplirse antes de ejecutar una prueba piloto.

## 2. Alcance del piloto

El piloto debe validar un flujo controlado con datos demo:

* Autenticacion por correo institucional.
* Acceso por rol.
* Consulta de catalogos.
* Consulta documental.
* Visor documental controlado para PDF.
* Solicitudes documentales base.
* Copias controladas base.
* Registros de implementacion/lectura base.
* Auditoria de acciones relevantes.
* Libro Maestro documental.
* Reportes de Fase 4 y exportacion CSV.

El piloto debe ejecutarse en un ambiente controlado, con usuarios de prueba, datos no productivos y respaldo previo.

## 3. Lo que no se va a probar

Quedan fuera del piloto controlado inicial:

* Datos productivos reales.
* Usuarios reales activos en operacion diaria.
* Despliegue productivo definitivo.
* Integracion LDAP, Active Directory o Microsoft 365.
* Notificaciones por correo.
* Workflows completos de aprobacion multinivel.
* Firma electronica avanzada.
* Constancias formales con numeracion final.
* Exportacion Excel `.xlsx`.
* Conversion de Office a PDF.
* Visor PDF.js custom.
* Bloqueo absoluto de descarga, impresion, copia, captura de pantalla o fotografia externa.
* Integracion con SIEM, Wazuh u otras herramientas externas.

## 4. Roles participantes

Los roles del piloto deben representar el modelo funcional aprobado:

| Rol | Responsabilidad en piloto |
| --- | --- |
| Organizacion y Metodos Administrador | Validar reglas funcionales, reportes, Libro Maestro, solicitudes, copias y trazabilidad. |
| Analista OyM | Ejecutar escenarios operativos de gestion documental. |
| Unidad Ejecutora | Crear y consultar solicitudes documentales aplicables. |
| Usuario Lector | Consultar documentos asignados y validar restricciones del visor. |
| Sistemas Tecnico | Validar plataforma, Docker, PostgreSQL, respaldos, restauracion, healthcheck y soporte tecnico. |
| Auditor | Consultar auditoria segun permisos definidos y validar trazabilidad disponible. |

Sistemas no debe modificar reglas funcionales de Organizacion y Metodos durante el piloto.

## 5. Usuarios de prueba requeridos

Antes de iniciar el piloto se deben crear usuarios demo, no usuarios productivos:

| Usuario demo sugerido | Rol esperado | Uso |
| --- | --- | --- |
| `oym.admin.demo@oftalmi.test` | OyM Administrador | Administracion funcional y reportes. |
| `oym.analista.demo@oftalmi.test` | Analista OyM | Gestion operativa documental. |
| `unidad.demo@oftalmi.test` | Unidad Ejecutora | Solicitudes y consulta segun unidad. |
| `lector.demo@oftalmi.test` | Usuario Lector | Consulta controlada e implementacion. |
| `sistemas.demo@oftalmi.test` | Sistemas Tecnico | Validacion tecnica y soporte. |
| `auditor.demo@oftalmi.test` | Auditor | Revision de eventos de auditoria. |
| `sin.permiso.demo@oftalmi.test` | Usuario sin permiso documental | Validacion de accesos denegados por ausencia de relacion documental. |

Estos usuarios no se crean en este punto. La creacion debe realizarse solo cuando se autorice formalmente el inicio del piloto.

## 6. Datos documentales demo requeridos

El piloto debe contar con datos demo suficientes para cubrir escenarios reales sin exponer informacion sensible:

* Unidades organizativas base.
* Tipos documentales base.
* Documentos demo con codigo documental.
* Versiones documentales demo.
* Archivos PDF demo no sensibles.
* Documentos en diferentes estados cuando aplique.
* Solicitudes documentales demo.
* Copias controladas demo.
* Registros de implementacion/lectura demo.
* Eventos de auditoria generados por interacciones reales del piloto.

No se deben cargar documentos productivos, respaldos reales ni archivos sensibles.

La definicion detallada del set minimo de usuarios, roles, unidades, documentos, versiones, archivos PDF, copias controladas, registros de implementacion, reportes y auditoria se registra en:

```text
docs/08_piloto_controlado/datos_demo_y_usuarios_prueba.md
```

Ese documento corresponde a PILOTO-P02 y no crea datos, fixtures, seeders ni usuarios.

PILOTO-P03 implementa el mecanismo tecnico controlado para cargar ese set demo mediante el comando:

```bash
python manage.py seed_pilot_demo_data
```

El comando debe ejecutarse solo en ambiente local o piloto controlado, despues de `seed_base_catalogs`, y no inicia por si mismo la prueba piloto.

## 7. Checklist tecnico previo

Antes de iniciar el piloto deben validarse, como minimo:

* Rama de trabajo autorizada.
* Ambiente tecnico definido.
* Variables de entorno no productivas.
* Contenedores `db` y `backend` operativos.
* Migraciones aplicadas y sin pendientes.
* Suite de pruebas base aprobada.
* Healthcheck `200`.
* Almacenamiento de medios configurado para datos demo.
* Usuario administrador tecnico definido para soporte.
* Respaldo inicial de base de datos y archivos demo.
* Procedimiento de restauracion probado en ambiente aislado.

## 8. Checklist funcional OyM

Organizacion y Metodos debe validar:

* Roles funcionales participantes.
* Usuarios demo requeridos.
* Unidades demo.
* Tipos documentales demo.
* Documentos demo.
* Escenarios de solicitud documental.
* Escenarios de copias controladas.
* Escenarios de lectura o implementacion.
* Reportes que se revisaran.
* Criterios de aprobacion o rechazo del piloto.

## 9. Validaciones de seguridad

El piloto debe validar:

* Login obligatorio.
* Redireccion a login para usuarios anonimos.
* Respuesta 403 para usuarios autenticados sin permiso.
* Acceso restringido por rol.
* Ausencia de rutas directas a archivos documentales.
* Ausencia de enlaces `MEDIA_URL` en reportes y visor.
* Entrega controlada de PDF.
* Auditoria de accesos permitidos, denegados y fallidos cuando aplique.
* Exportaciones CSV solo para roles autorizados de OyM.

## 10. Validaciones de visor documental

El visor debe probarse con PDF demo:

* Acceso permitido para usuario autorizado.
* Acceso denegado para usuario sin relacion documental.
* Documento, version, archivo o archivo fisico inexistente con respuesta controlada.
* Entrega inline del PDF mediante ruta protegida.
* `Cache-Control: no-store`.
* Ausencia de ruta fisica del archivo.
* Ausencia de botones de descarga o impresion en la interfaz.
* Mensaje de restriccion de impresion.
* Marca de agua visual con usuario, documento, version y fecha/hora.

El visor reduce exposicion, pero no garantiza bloqueo absoluto contra captura, fotografia externa, OCR, herramientas avanzadas o funciones nativas del navegador.

## 11. Validaciones de reportes

Los reportes de Fase 4 deben validarse con datos demo:

* Libro Maestro documental.
* Reporte mensual documental.
* Reporte de copias controladas.
* Reporte de implementacion/lectura.
* Filtros por tipo documental, unidad, estado, fechas, codigo y usuario cuando aplique.
* Exportacion CSV controlada.
* CSV sin PDFs, adjuntos, rutas fisicas ni `MEDIA_URL`.
* Auditoria `REPORT_VIEWED` y `REPORT_EXPORTED` mediante `AuditAction.REPORT_GENERATED`.

Excel queda pendiente hasta que se apruebe una dependencia y punto tecnico especifico.

## 12. Validaciones de auditoria

La auditoria debe evidenciar:

* Usuario.
* Accion.
* Resultado.
* Fecha/hora del servidor.
* Modulo de origen.
* Entidad afectada cuando aplique.
* IP cuando este disponible.
* User agent cuando este disponible.
* Metadata de documento, version, archivo, reporte o filtros cuando aplique.

Eventos clave a revisar:

* Visualizacion documental.
* Acceso denegado a documento o archivo.
* Consulta de reporte.
* Exportacion de reporte.
* Creacion de solicitud.
* Registro de implementacion.

## 13. Procedimiento de respaldo/restauracion

Antes de iniciar el piloto:

1. Registrar fecha, ambiente, rama, commit y responsable tecnico.
2. Crear respaldo de PostgreSQL del ambiente de piloto.
3. Crear respaldo del almacenamiento de archivos demo.
4. Verificar que el respaldo no contenga datos productivos.
5. Ejecutar restauracion de prueba en ambiente aislado o base temporal.
6. Documentar resultado de restauracion.
7. Mantener el respaldo hasta cerrar el piloto.

Si una validacion critica falla, Sistemas debe restaurar el estado previo o detener el piloto segun el criterio de bloqueo definido.

## 14. Criterios de aceptacion

El piloto puede considerarse aceptado si:

* OyM valida que las pantallas base representan el flujo minimo esperado.
* Los roles acceden solo a lo autorizado.
* El visor documental no expone rutas directas de archivos.
* Los reportes muestran informacion demo coherente.
* La exportacion CSV respeta permisos y no incluye archivos.
* La auditoria permite reconstruir acciones relevantes.
* No existen migraciones pendientes.
* El healthcheck responde correctamente.
* Las pruebas base siguen aprobadas.
* No se cargaron datos productivos.
* No se modifico `main` sin autorizacion.

## 15. Criterios de rechazo o bloqueo

El piloto debe detenerse o no iniciarse si:

* Se requiere usar datos productivos sin aprobacion formal.
* Hay migraciones pendientes no revisadas.
* Falla el healthcheck.
* Falla una prueba critica de permisos.
* Usuarios sin permiso acceden a documentos, reportes o auditoria.
* Se exponen rutas directas de archivos o `MEDIA_URL`.
* No existe respaldo previo verificable.
* No se puede restaurar el ambiente.
* OyM identifica una regla funcional incorrecta o no validada.
* Sistemas necesita modificar reglas funcionales para continuar.

## 16. Riesgos

Riesgos principales:

* Datos demo insuficientes para representar escenarios reales.
* Expectativa de bloqueo absoluto de descarga o impresion.
* Redistribucion externa de CSV por usuarios autorizados.
* Configuracion incorrecta de almacenamiento o Nginx que exponga archivos.
* Diferencias entre piloto y futura infraestructura productiva.
* Reglas funcionales pendientes de validacion por OyM.
* Confusion entre piloto tecnico y despliegue productivo.

## 17. Plan de cierre del piloto

Al finalizar el piloto se debe documentar:

* Fecha de inicio y cierre.
* Participantes.
* Commit y ambiente probado.
* Escenarios ejecutados.
* Evidencias recolectadas.
* Incidencias.
* Riesgos nuevos.
* Decisiones funcionales de OyM.
* Decisiones tecnicas de Sistemas.
* Resultado: aprobado, aprobado con observaciones o rechazado.
* Acciones requeridas antes de despliegue interno.

## 18. Recomendacion para pasar de piloto a despliegue interno

Solo se recomienda pasar a despliegue interno si:

* OyM aprueba el resultado funcional.
* Sistemas valida operacion, respaldo, restauracion y monitoreo minimo.
* No quedan bloqueos criticos de permisos, auditoria, visor o reportes.
* Se define plan de carga inicial controlada.
* Se define procedimiento de soporte.
* Se actualiza documentacion de despliegue, backup, restauracion y monitoreo.
* Se mantiene `main` como version estable aprobada hasta autorizacion explicita de promocion.
