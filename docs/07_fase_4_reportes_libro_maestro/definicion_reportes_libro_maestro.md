# Definicion Tecnica y Funcional - Reportes y Libro Maestro

## 1. Proposito

Este documento inicia la Fase 4 del SGD-OFTALMI y define el alcance tecnico y funcional inicial de reportes y Libro Maestro documental.

F4-P01 es un punto documental. No implementa codigo, vistas, URLs, templates, modelos, migraciones ni exportadores.

El objetivo es establecer una base verificable para construir reportes de Organizacion y Metodos sin inventar reglas funcionales fuera del MVP.

## 2. Contexto de cierre de fases previas

La Fase 1 dejo el backend base, modelos documentales, solicitudes, copias controladas, registros de implementacion, auditoria, roles, permisos, servicios y selectors iniciales.

La Fase 2 dejo la capa de acceso web interna con Django templates, login, dashboard, vistas de consulta base, permisos por rol y pruebas integradas.

La Fase 3 dejo el visor documental controlado para PDF, entrega protegida, permisos por documento/version/archivo, auditoria `DOCUMENT_VIEWED`, reduccion de exposicion de descarga e impresion, marca de agua visual y documentacion de limitaciones reales.

La Fase 4 debe construir sobre esa base, sin modificar el alcance funcional: los reportes son de uso exclusivo de Organizacion y Metodos.

## 3. Objetivo de Fase 4

Fase 4 tiene como objetivo habilitar reportes operativos y el Libro Maestro de Control Documental para Organizacion y Metodos.

Objetivos funcionales:

* Consultar el inventario documental controlado.
* Identificar documentos vigentes, vencidos, por vencer, obsoletos y archivados.
* Consultar solicitudes documentales pendientes o cerradas.
* Consultar constancias/registros de implementacion pendientes y completados.
* Consultar copias controladas activas, entregadas, retiradas o canceladas.
* Obtener estadisticas por unidad ejecutora y tipo documental.
* Exportar informacion reportable para uso interno de OyM.

Objetivos tecnicos:

* Reutilizar modelos, servicios, selectors y permisos existentes.
* Mantener reportes como consultas de solo lectura.
* Auditar consulta o exportacion de reportes cuando aplique.
* Evitar exponer informacion a usuarios lectores, unidades ejecutoras o Sistemas sin autorizacion funcional.
* Implementar exportaciones de forma progresiva y trazable.

## 4. Alcance del Libro Maestro documental

El Libro Maestro debe representar el inventario controlado de documentos administrados por Organizacion y Metodos.

Campos base esperados:

* Codigo documental.
* Titulo del documento.
* Tipo documental.
* Unidad ejecutora responsable.
* Estado documental.
* Version vigente o version actual registrada.
* Fecha de emision cuando exista.
* Fecha de vigencia/efectividad cuando exista.
* Fecha de vencimiento cuando exista.
* Fecha de publicacion cuando exista.
* Fecha de obsolescencia cuando exista.
* Usuario creador o responsable de carga cuando aplique.
* Indicador de archivo documental activo cuando aplique.

El Libro Maestro debe generarse a partir de datos existentes en `Document`, `DocumentVersion`, `DocumentFile`, `DocumentType` y `OrganizationalUnit`.

No debe modificar datos documentales. No debe recalcular estados documentales con reglas no validadas por OyM.

## 5. Reportes incluidos en el MVP

Reportes funcionales base:

| Reporte | Proposito |
| --- | --- |
| Libro Maestro de Control Documental | Inventario principal de documentos controlados. |
| Reporte mensual de Gestion Documental | Resumen mensual de actividad documental. |
| Documentos vigentes | Documentos publicados o activos segun estado registrado. |
| Documentos vencidos | Documentos con fecha de vencimiento anterior a la fecha de corte, segun datos disponibles. |
| Documentos por vencer | Documentos con vencimiento dentro de una ventana configurable o definida por OyM. |
| Documentos obsoletos | Documentos con estado obsoleto o version obsoleta registrada. |
| Solicitudes pendientes | Solicitudes en estados no cerrados ni cancelados. |
| Constancias pendientes | Registros de implementacion no completados. |
| Copias controladas activas | Copias con estado activo o entregado, segun regla definida. |
| Copias controladas retiradas | Copias con estado retirado. |
| Estadisticas por unidad ejecutora | Conteos por unidad responsable o receptora. |
| Estadisticas por tipo documental | Conteos por tipo documental. |
| Historico de modificaciones documentales | Cambios documentales trazables desde versiones, estados y auditoria disponible. |

Los reportes pueden ampliarse solo con validacion funcional de OyM.

## 6. Filtros esperados

Filtros transversales:

* Tipo documental.
* Unidad ejecutora.
* Estado documental o estado del modulo reportado.
* Vigencia.
* Rango de fechas.
* Fecha de corte.

Filtros por modulo:

| Modulo | Filtros esperados |
| --- | --- |
| Documentos | Tipo documental, unidad responsable, estado, version, fecha de emision, fecha efectiva, fecha de vencimiento. |
| Solicitudes documentales | Tipo de solicitud, estado, unidad solicitante, solicitante, fecha de creacion, fecha de cierre. |
| Copias controladas | Documento, version, unidad receptora, usuario receptor, estado, fecha de entrega, fecha de retiro. |
| Implementacion | Usuario, unidad, documento, version, estado, fecha de asignacion, lectura, aceptacion o implementacion. |
| Auditoria | Accion, resultado, usuario, modulo, entidad y rango de fechas, si se habilita reporte de auditoria para OyM. |

Los filtros deben aplicarse en backend. No deben depender solo de ocultamiento visual en templates.

## 7. Fuentes de datos existentes

Fuentes principales ya disponibles:

| Fuente | Uso esperado |
| --- | --- |
| `Document` | Libro Maestro, documentos por estado, unidad, tipo y estado activo. |
| `DocumentVersion` | Version vigente, fechas de emision, vigencia, vencimiento, publicacion y obsolescencia. |
| `DocumentFile` | Evidencia de archivo activo, metadatos de carga y trazabilidad de archivo. |
| `DocumentType` | Filtro y agrupacion por tipo documental. |
| `OrganizationalUnit` | Filtro y agrupacion por unidad ejecutora. |
| `DocumentRequest` | Solicitudes pendientes, cerradas, observadas y estadisticas de gestion. |
| `ControlledCopy` | Copias activas, entregadas, retiradas y asignaciones por unidad/usuario. |
| `ImplementationRecord` | Registros pendientes, leidos, aceptados, implementados y vencidos. |
| `AuditEvent` | Trazabilidad de generacion/exportacion y posible historico de eventos. |
| `User` | Filtros por solicitante, responsable, receptor o usuario de implementacion. |

Limitacion actual: no existe todavia un modelo especializado `ReportExport`, `ReportSnapshot` ni tablas analiticas. F4 debe iniciar con consultas sobre modelos transaccionales existentes.

## 8. Permisos por rol

Los reportes son exclusivos de Organizacion y Metodos.

| Rol | Acceso esperado |
| --- | --- |
| OyM Administrador Funcional | Puede consultar, generar y exportar reportes. |
| Analista OyM | Puede consultar, generar y exportar reportes autorizados. |
| Unidad Ejecutora | No accede a reportes de OyM en el MVP. |
| Usuario Lector | No accede a reportes. |
| Sistemas Administrador Tecnico | No accede funcionalmente a reportes, salvo soporte tecnico autorizado y documentado. |
| Auditor | No accede por defecto a reportes de OyM; mantiene consulta de auditoria segun permisos existentes. |

El helper actual de `reports.permissions` restringe `can_view_reports`, `can_generate_reports` y `can_export_reports` a usuarios OyM. F4 debe mantener esta regla salvo validacion funcional expresa.

## 9. Exportaciones permitidas

La regla funcional del MVP exige exportacion a Excel para reportes.

Decision tecnica inicial:

* CSV puede usarse como primera exportacion simple porque no requiere dependencia adicional.
* Excel (`.xlsx`) debe implementarse como objetivo del MVP cuando se agregue una dependencia justificada, por ejemplo `openpyxl` o alternativa equivalente.
* La incorporacion de dependencia para Excel debe hacerse en un punto tecnico especifico y quedar registrada en requirements, pruebas y documentacion.

La exportacion controlada final de Fase 4 debe:

* Respetar permisos de reportes.
* Aplicar los filtros seleccionados.
* Registrar auditoria de generacion/exportacion cuando se implemente el punto especifico de auditoria de reportes.
* Evitar incluir campos sensibles no necesarios.
* Mantener encabezados claros y consistentes.

## 10. Auditoria esperada

Las consultas y exportaciones de reportes deben auditarse cuando sean relevantes para control documental.

Evento base existente:

```text
AuditAction.REPORT_GENERATED
```

Metadata minima recomendada:

* Usuario.
* Modulo `reports`.
* Nombre del reporte.
* Accion: consulta, generacion o exportacion.
* Resultado: exitoso, denegado o fallido.
* Filtros aplicados.
* Formato de salida cuando aplique.
* Fecha/hora del servidor.
* IP y user agent cuando esten disponibles.

No se debe crear un nuevo modelo de auditoria si `AuditEvent` cubre la necesidad inicial.

## 11. Riesgos y limites

Riesgos tecnicos y funcionales:

* Datos incompletos por campos opcionales de fechas en versiones documentales.
* Estados documentales mal usados o no actualizados por proceso operativo incompleto.
* Interpretar "vencido" o "por vencer" sin regla de corte validada por OyM.
* Exportar informacion sensible a roles no autorizados.
* Generar reportes pesados sin paginacion o limites.
* Duplicar logica de filtros entre vistas, selectors y exportadores.
* Agregar dependencia Excel sin pruebas ni justificacion.
* Confundir reportes operativos con auditoria completa o BI avanzado.

Limites de F4-P01:

* No implementa reportes.
* No crea endpoints, vistas, templates ni exportadores.
* No crea modelos, migraciones ni snapshots.
* No define reglas de vencimiento no validadas por OyM.

## 12. Roadmap F4-P01 a F4-P11

Puntos propuestos para Fase 4:

| Punto | Nombre | Resultado esperado |
| --- | --- | --- |
| F4-P01 | Definicion tecnica y funcional de reportes y Libro Maestro | Documento base de alcance, fuentes, permisos, filtros, auditoria y riesgos. |
| F4-P02 | Selectors base de reportes | Consultas reutilizables para Libro Maestro y reportes principales. |
| F4-P03 | Vista de Libro Maestro documental | Consulta web base y protegida del inventario documental. |
| F4-P04 | Filtros base del Libro Maestro | Filtros iniciales por tipo, unidad, estado, vigencia y fechas. |
| F4-P05 | Reporte mensual documental | Actividad documental publicada por periodo mensual. |
| F4-P06 | Reporte de copias controladas | Activas, entregadas, retiradas y agrupaciones por unidad/documento. |
| F4-P07 | Reporte de implementacion/lectura | Pendientes, leidos, aceptados, implementados y vencidos. |
| F4-P08 | Exportacion controlada CSV de reportes | Exportadores CSV para los reportes base ya implementados. |
| F4-P09 | Permisos y auditoria de reportes | Registro `REPORT_GENERATED` con metadata de consulta/exportacion, filtros y formato. |
| F4-P10 | Pruebas integradas de reportes | Cobertura de vistas, filtros, exportaciones, permisos, auditoria y seguridad documental. |
| F4-P11 | Cierre documental de Fase 4 y pendientes | Cierre tecnico, pendientes y siguiente fase. |

El orden puede ajustarse si OyM prioriza un reporte especifico, pero cualquier cambio debe documentarse.

## 13. Criterios de aceptacion de F4-P01

F4-P01 se considera cerrado cuando:

* Existe documento de definicion de reportes y Libro Maestro.
* Roadmap tecnico registra el inicio formal de Fase 4.
* Arquitectura de aplicacion referencia la estrategia de reportes.
* Queda claro que no se implemento codigo.
* Queda claro que no se crearon modelos ni migraciones.
* Quedan documentados reportes MVP, filtros, fuentes, permisos, exportaciones, auditoria, riesgos y puntos F4-P01 a F4-P11.

## 14. Selectores base de reportes

F4-P02 implementa la capa base de selectors para reportes documentales y Libro Maestro.

Selectors definidos:

* `get_master_book_queryset`
* `get_monthly_document_report_queryset`
* `get_controlled_copies_report_queryset`
* `get_implementation_records_report_queryset`

Propiedades esperadas:

* Reutilizan modelos existentes.
* Trabajan con `QuerySet` de solo lectura.
* Centralizan filtros por tipo documental, unidad organizativa, estado, vigencia, rango de fechas, código documental, responsable y versión.
* Usan `select_related` para reducir consultas adicionales cuando aplica.
* No dependen de `request` HTTP.
* No incluyen lógica de exportacion ni de presentacion.
* Sirven como base para reportes, Libro Maestro y futuras vistas de Fase 4.

F4-P02 no crea modelos ni migraciones. Cualquier selector nuevo debe documentar de forma explicita su fuente de datos y su criterio de filtro.

## 15. Vista de Libro Maestro documental

F4-P03 crea la primera vista web de solo lectura del Libro Maestro documental.

Alcance implementado:

* Ruta interna `/app/reports/master-book/`.
* Acceso protegido por login.
* Acceso funcional restringido a usuarios OyM mediante `can_view_reports`.
* Reutilizacion directa de `get_master_book_queryset`.
* Template tabular sin enlaces a archivos documentales ni exposicion de rutas `MEDIA_URL`.
* Pruebas de acceso, render y uso del selector.

Mapeo de campos visibles:

| Columna | Fuente actual |
| --- | --- |
| Codigo documental | `Document.code` |
| Titulo | `Document.title` |
| Tipo documental | `Document.document_type.code` y `Document.document_type.name` |
| Unidad responsable | `Document.owner_unit.name` |
| Estado | `Document.status` con su display Django |
| Version vigente o actual | `Document.current_version.version_number` |
| Fecha de emision/creacion | `DocumentVersion.issue_date`; si no existe, `Document.created_at` |
| Fecha de vigencia | `DocumentVersion.effective_date`; si no existe, se muestra vacio funcional `-` |

F4-P03 no implementa filtros avanzados, exportaciones, reportes analiticos, auditoria de consulta, modelos nuevos ni migraciones.

## 16. Filtros de Libro Maestro

F4-P04 agrega filtros funcionales de consulta a la vista del Libro Maestro documental.

Alcance implementado:

* Filtros GET en `/app/reports/master-book/`.
* Formulario Django `MasterBookFilterForm` para validacion simple de parametros.
* Reutilizacion de `get_master_book_queryset` como unica fuente de consulta.
* Conservacion visual de filtros seleccionados.
* Manejo tolerante de filtros invalidos sin romper la vista.
* Pruebas de filtros por tipo documental, unidad, estado, vigencia, codigo y titulo.

Filtros disponibles:

| Filtro | Fuente o criterio |
| --- | --- |
| Tipo documental | `Document.document_type` |
| Unidad responsable | `Document.owner_unit` |
| Estado documental | `Document.status` |
| Vigencia | Grupos de estado existentes en `get_master_book_queryset` |
| Codigo documental | `Document.code` exacto |
| Titulo | `Document.title__icontains` |
| Rango de fechas | `Document.created_at__date` |

Limitaciones registradas:

* La vigencia actual no recalcula vencimientos a partir de fechas; usa estados documentales disponibles.
* El rango de fechas aplica sobre fecha de creacion del documento, no sobre emision, vigencia o vencimiento.
* No se implementan filtros avanzados por fechas de version documental en este punto.
* No se implementa exportacion CSV/Excel.
* No se crean modelos ni migraciones.

## 17. Reporte mensual documental

F4-P05 implementa la primera vista del reporte mensual documental.

Alcance implementado:

* Ruta interna `/app/reports/monthly-documents/`.
* Acceso protegido por login.
* Acceso funcional restringido a usuarios OyM mediante `can_view_reports`.
* Periodo por defecto con mes y ano actuales.
* Filtros GET por mes, ano, tipo documental, unidad responsable y estado.
* Reutilizacion de `get_monthly_document_report_queryset`.
* Resumen basico con total del periodo, totales por estado y totales por tipo documental.
* Pruebas de acceso, render, filtros, parametros invalidos y llamada al selector.

Mapeo de campos visibles:

| Columna | Fuente actual |
| --- | --- |
| Codigo documental | `DocumentVersion.document.code` |
| Titulo | `DocumentVersion.document.title` |
| Tipo documental | `DocumentVersion.document.document_type` |
| Unidad responsable | `DocumentVersion.document.owner_unit` |
| Estado | `DocumentVersion.status` con su display Django |
| Version | `DocumentVersion.version_number` |
| Fecha de creacion/emision | `DocumentVersion.issue_date`; si no existe, `DocumentVersion.created_at` |
| Ultima actualizacion | `DocumentVersion.document.updated_at` |

Limitaciones registradas:

* El periodo mensual usa `DocumentVersion.published_at__date`.
* Las versiones sin fecha de publicacion no aparecen en este reporte mensual.
* No se recalculan estados, vigencias ni vencimientos.
* No se implementan exportaciones CSV/Excel en este punto.
* No se crean modelos ni migraciones.

## 18. Reporte de copias controladas

F4-P06 implementa la vista base del reporte de copias controladas.

Alcance implementado:

* Ruta interna `/app/reports/controlled-copies/`.
* Acceso protegido por login.
* Acceso funcional restringido a usuarios OyM mediante `can_view_reports`.
* Filtros GET por tipo documental, unidad responsable, unidad destinataria, usuario destinatario, estado de copia, codigo documental y rango de fecha de entrega.
* Reutilizacion de `get_controlled_copies_report_queryset`.
* Resumen basico con total de copias, totales por estado y totales por unidad destinataria.
* Pruebas de acceso, render, filtros, parametros invalidos y llamada al selector.

Mapeo de campos visibles:

| Columna | Fuente actual |
| --- | --- |
| Codigo documental | `ControlledCopy.document.code` |
| Titulo | `ControlledCopy.document.title` |
| Tipo documental | `ControlledCopy.document.document_type` |
| Unidad responsable | `ControlledCopy.document.owner_unit` |
| Version | `ControlledCopy.document_version.version_number` |
| Destinatario | `ControlledCopy.receiver_user.email`; si no existe, `-` |
| Unidad destinataria | `ControlledCopy.receiver_unit.name` |
| Estado | `ControlledCopy.status` con su display Django |
| Fecha de creacion/asignacion | `ControlledCopy.delivered_at`; si no existe, `ControlledCopy.created_at` |
| Fecha de devolucion/cierre | `ControlledCopy.retired_at`; si no existe, `-` |
| Ultima actualizacion | `ControlledCopy.updated_at` |

Limitaciones registradas:

* El rango de fechas usa `ControlledCopy.delivered_at__date`.
* Las copias sin fecha de entrega no aparecen cuando se filtra por rango de entrega.
* No se implementa workflow de entrega, retiro ni cierre.
* No se implementan exportaciones CSV/Excel en este punto.
* No se crean modelos ni migraciones.

## 19. Reporte de implementacion/lectura

F4-P07 implementa la vista base del reporte de implementacion y lectura.

Alcance implementado:

* Ruta interna `/app/reports/implementation-records/`.
* Acceso protegido por login.
* Acceso funcional restringido a usuarios OyM mediante `can_view_reports`.
* Filtros GET por tipo documental, unidad responsable, unidad destinataria del usuario, usuario destinatario, estado, codigo documental, fecha de asignacion y fecha de implementacion.
* Reutilizacion de `get_implementation_records_report_queryset`.
* Resumen basico con total de registros, implementados, no implementados, totales por estado y totales por unidad destinataria.
* Pruebas de acceso, render, filtros, parametros invalidos y llamada al selector.

Mapeo de campos visibles:

| Columna | Fuente actual |
| --- | --- |
| Codigo documental | `ImplementationRecord.document.code` |
| Titulo | `ImplementationRecord.document.title` |
| Tipo documental | `ImplementationRecord.document.document_type` |
| Unidad responsable | `ImplementationRecord.document.owner_unit` |
| Version | `ImplementationRecord.document_version.version_number` |
| Unidad destinataria | `ImplementationRecord.user.organizational_unit`; si no existe, `-` |
| Usuario destinatario | `ImplementationRecord.user.email` |
| Estado | `ImplementationRecord.status` con su display Django |
| Fecha de asignacion | `ImplementationRecord.assigned_at` |
| Fecha de confirmacion | `implemented_at`, `accepted_at`, `interpreted_at` o `read_at`, en ese orden |
| Ultima actualizacion | `ImplementationRecord.updated_at` |

Limitaciones registradas:

* `ImplementationRecord` no tiene unidad destinataria directa; se usa la unidad asociada al usuario.
* El rango de asignacion usa `ImplementationRecord.assigned_at__date`.
* El rango de confirmacion usa `ImplementationRecord.implemented_at__date` como criterio operativo.
* "Implementados" se calcula con estado `IMPLEMENTED`; los demas estados quedan agrupados como no implementados para resumen operativo.
* No se modifica el flujo funcional de lectura, aceptacion o implementacion.
* No se implementan exportaciones CSV/Excel en este punto.
* No se crean modelos ni migraciones.

## 20. Exportacion controlada CSV de reportes

F4-P08 implementa la primera salida controlada de reportes, usando CSV como formato tecnico simple.

Rutas implementadas:

| Reporte | Ruta CSV |
| --- | --- |
| Libro Maestro | `/app/reports/master-book/export.csv` |
| Reporte mensual documental | `/app/reports/monthly-documents/export.csv` |
| Reporte de copias controladas | `/app/reports/controlled-copies/export.csv` |
| Reporte de implementacion/lectura | `/app/reports/implementation-records/export.csv` |

Alcance implementado:

* Acceso protegido por login.
* Acceso funcional restringido a usuarios OyM mediante `can_view_reports`.
* Reutilizacion de los formularios GET existentes para sanitizar parametros.
* Reutilizacion de los selectors de reportes como fuente de datos.
* Enlaces `Exportar CSV` en las pantallas de reportes.
* Respuesta `text/csv; charset=utf-8` con BOM UTF-8.
* `Content-Disposition: attachment` aplicado al CSV generado.
* Nombres de archivo fechados con prefijo `sgd-oftalmi`.
* Pruebas de acceso, headers, contenido, filtros y ausencia de rutas `MEDIA_URL`.

Campos exportados:

| Reporte | Fuente |
| --- | --- |
| Libro Maestro | `Document`, `Document.current_version`, `DocumentType`, `OrganizationalUnit` |
| Reporte mensual | `DocumentVersion` y su `Document` asociado |
| Copias controladas | `ControlledCopy`, `Document`, `DocumentVersion`, destinatario y unidad receptora |
| Implementacion/lectura | `ImplementationRecord`, `Document`, `DocumentVersion`, usuario y unidad del usuario |

Controles aplicados:

* La exportacion respeta los mismos filtros de la pantalla.
* No exporta PDFs, adjuntos ni contenido documental.
* No incluye rutas fisicas, rutas `MEDIA_URL` ni enlaces de descarga.
* No expone visor documental ni entrega controlada de archivos.
* No crea snapshots ni tablas analiticas.

Limitaciones registradas:

* Excel `.xlsx` queda pendiente como objetivo MVP con dependencia justificada.
* No se agrego dependencia nueva para F4-P08.
* La auditoria especifica de consulta/exportacion se implementa en F4-P09.
* No se crean modelos ni migraciones.

## 21. Permisos y auditoria de reportes

F4-P09 refuerza permisos y registra auditoria de consulta/exportacion de los reportes base de Fase 4.

Alcance implementado:

* Permiso unico de consulta/exportacion mediante `can_view_reports`.
* Acceso mantenido para OyM Administrador Funcional y Analista OyM.
* Usuarios no autenticados mantienen redireccion al login.
* Usuarios autenticados sin permiso mantienen respuesta 403.
* Consulta HTML auditada para:
  * Libro Maestro.
  * Reporte mensual documental.
  * Reporte de copias controladas.
  * Reporte de implementacion/lectura.
* Exportacion CSV auditada para esos mismos reportes.
* Intentos denegados auditados cuando existe usuario autenticado.

Decision tecnica de auditoria:

* Se reutiliza `AuditEvent`.
* Se reutiliza `AuditAction.REPORT_GENERATED`.
* No se crean nuevos valores `REPORT_VIEWED` ni `REPORT_EXPORTED` en el enum para evitar migraciones.
* La diferencia entre consulta y exportacion se registra en `after_data.report_event`.

Metadata registrada:

| Campo | Fuente |
| --- | --- |
| Usuario | `request.user` |
| Accion base | `AuditAction.REPORT_GENERATED` |
| Modulo | `reports` |
| Entidad | `Report` |
| Identificador | Codigo interno del reporte |
| Resultado | `success` o `denied` |
| Evento de reporte | `REPORT_VIEWED` o `REPORT_EXPORTED` |
| Filtros | Parametros GET recibidos |
| Formato | `html` o `csv` |
| IP | Metadata del request si esta disponible |
| User agent | Metadata del request si esta disponible |
| Fecha/hora | `AuditEvent.created_at` |

Controles aplicados:

* La auditoria no registra contenido documental.
* La auditoria no registra PDFs, adjuntos ni rutas de archivos.
* La auditoria no incluye rutas `MEDIA_URL`.
* Cada request exitoso de vista o exportacion genera un solo evento.
* Las exportaciones siguen usando la misma fuente de datos de pantalla.

Limitaciones registradas:

* No se implementa Excel `.xlsx`.
* No se crean modelos especializados como `ReportExport` o `ReportSnapshot`.
* No se implementan reportes nuevos.
* No se modifica visor documental, documentos, copias controladas ni registros de implementacion.
* No se crean modelos ni migraciones.

## 22. Pruebas integradas de reportes

F4-P10 consolida la cobertura integrada del modulo de reportes sin crear funcionalidad nueva.

Cobertura reforzada:

* Acceso HTML a los cuatro reportes de Fase 4.
* Exportacion CSV de los cuatro reportes.
* Redireccion a login para usuarios no autenticados.
* Respuesta 403 para usuarios autenticados sin permiso.
* Acceso autorizado para roles OyM.
* Filtros GET principales por reporte.
* Parametros invalidos sin ruptura de vistas ni exportaciones.
* Headers CSV `Content-Type` y `Content-Disposition`.
* Encabezados CSV completos por reporte.
* Preservacion de UTF-8 con acentos en CSV.
* Auditoria `REPORT_VIEWED` y `REPORT_EXPORTED` mediante `AuditAction.REPORT_GENERATED`.
* Auditoria de intentos denegados con resultado `denied`.
* Ausencia de PDFs, adjuntos, rutas `MEDIA_URL`, rutas fisicas y visor documental en reportes HTML y CSV.

Resultado tecnico:

```text
apps.reports -> 69 tests OK
```

Controles confirmados:

* Los reportes no exponen archivos documentales.
* Las exportaciones contienen solo metadata reportable.
* Los filtros invalidos no interrumpen la respuesta.
* La auditoria no registra contenido documental sensible.
* Las exportaciones no implementan Excel ni descargan adjuntos.

Pendientes documentados:

* Excel `.xlsx` sigue pendiente como objetivo MVP con dependencia justificada.
* Reportes de solicitudes documentales quedan pendientes para un punto posterior si OyM los prioriza.
* Cierre documental completo de Fase 4 queda para F4-P11.

## 23. Cierre documental de Fase 4

F4-P11 cierra documentalmente la Fase 4.

Documento de cierre:

```text
docs/07_fase_4_reportes_libro_maestro/cierre_fase_4.md
```

El cierre consolida:

* Estado final de Fase 4.
* Rutas HTML y CSV.
* Componentes tecnicos implementados.
* Reportes disponibles.
* Filtros por reporte.
* Exportacion CSV controlada.
* Permisos por rol.
* Auditoria de consulta/exportacion.
* Validaciones finales.
* Limitaciones y riesgos residuales.
* Pendientes y recomendacion para preparacion piloto posterior.

F4-P11 no crea codigo funcional, modelos, migraciones, vistas, templates, URLs ni reportes nuevos. Tampoco inicia piloto tecnico.
