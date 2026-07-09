# Cierre Tecnico - Fase 4 Reportes y Libro Maestro

## 1. Estado final de Fase 4

La Fase 4 queda cerrada tecnicamente como bloque de reportes operativos y Libro Maestro documental para Organizacion y Metodos.

El cierre es documental. No crea codigo Python, modelos, migraciones, vistas, templates, URLs ni nuevas funcionalidades.

Estado final:

```text
Fase 4 -> Completada documentalmente
Rama de trabajo -> develop
Rama estable -> main sin modificar
Piloto tecnico -> No iniciado
```

## 2. Resumen ejecutivo

Fase 4 implemento la base operativa de reportes del MVP del SGD-OFTALMI.

El modulo permite a usuarios autorizados de Organizacion y Metodos consultar:

* Libro Maestro documental.
* Reporte mensual documental.
* Reporte de copias controladas.
* Reporte de implementacion/lectura.

Tambien permite exportar esos reportes a CSV de forma controlada, con permisos, trazabilidad y pruebas integradas. El sistema no exporta archivos documentales, PDFs, adjuntos ni rutas fisicas.

La exportacion Excel queda pendiente como objetivo MVP posterior, porque requiere una dependencia justificada y validaciones especificas.

## 3. Puntos cerrados F4-P01 a F4-P11

| Punto | Estado | Resultado |
| --- | --- | --- |
| F4-P01 | Completado | Definicion tecnica y funcional de reportes y Libro Maestro. |
| F4-P02 | Completado | Selectors base de reportes. |
| F4-P03 | Completado | Vista de Libro Maestro documental. |
| F4-P04 | Completado | Filtros base del Libro Maestro. |
| F4-P05 | Completado | Reporte mensual documental. |
| F4-P06 | Completado | Reporte de copias controladas. |
| F4-P07 | Completado | Reporte de implementacion/lectura. |
| F4-P08 | Completado | Exportacion controlada CSV de reportes. |
| F4-P09 | Completado | Permisos y auditoria de reportes. |
| F4-P10 | Completado | Pruebas integradas de reportes. |
| F4-P11 | Completado | Documentacion tecnica de cierre de Fase 4. |

## 4. Rutas implementadas

Rutas HTML:

| Reporte | Ruta |
| --- | --- |
| Libro Maestro documental | `/app/reports/master-book/` |
| Reporte mensual documental | `/app/reports/monthly-documents/` |
| Reporte de copias controladas | `/app/reports/controlled-copies/` |
| Reporte de implementacion/lectura | `/app/reports/implementation-records/` |

Rutas CSV:

| Reporte | Ruta |
| --- | --- |
| Libro Maestro documental | `/app/reports/master-book/export.csv` |
| Reporte mensual documental | `/app/reports/monthly-documents/export.csv` |
| Reporte de copias controladas | `/app/reports/controlled-copies/export.csv` |
| Reporte de implementacion/lectura | `/app/reports/implementation-records/export.csv` |

Todas las rutas requieren login y permiso funcional de reportes.

## 5. Componentes tecnicos

Componentes consolidados:

```text
backend/apps/reports/forms.py
backend/apps/reports/selectors.py
backend/apps/reports/views.py
backend/apps/reports/urls.py
backend/apps/reports/exporters.py
backend/apps/reports/services.py
backend/templates/reports/*.html
backend/apps/reports/tests/test_views.py
backend/apps/reports/tests/test_selectors.py
```

Responsabilidad por componente:

| Componente | Responsabilidad |
| --- | --- |
| `forms.py` | Validacion simple de filtros GET. |
| `selectors.py` | Consultas reutilizables de solo lectura. |
| `views.py` | Vistas HTML, exportaciones CSV y aplicacion de permisos. |
| `urls.py` | Rutas internas del modulo de reportes. |
| `exporters.py` | Construccion de CSV y filas exportables. |
| `services.py` | Auditoria de consulta/exportacion de reportes. |
| `templates/reports/*.html` | Presentacion tabular y enlaces de exportacion. |
| `test_views.py` | Cobertura integrada de vistas, CSV, permisos, auditoria y seguridad documental. |
| `test_selectors.py` | Cobertura de selectors y filtros base. |

## 6. Reportes implementados

### 6.1 Libro Maestro documental

Consulta el inventario documental base desde `Document` y `Document.current_version`.

Campos principales:

* Codigo documental.
* Titulo.
* Tipo documental.
* Unidad responsable.
* Estado.
* Version.
* Fecha de emision/creacion.
* Fecha de vigencia.
* Ultima actualizacion en CSV.

### 6.2 Reporte mensual documental

Consulta actividad documental por periodo mensual desde `DocumentVersion.published_at`.

Campos principales:

* Codigo documental.
* Titulo.
* Tipo documental.
* Unidad responsable.
* Estado.
* Version.
* Fecha de creacion/emision.
* Ultima actualizacion.
* Periodo reportado en CSV.

### 6.3 Reporte de copias controladas

Consulta copias controladas desde `ControlledCopy`.

Campos principales:

* Codigo documental.
* Titulo.
* Tipo documental.
* Unidad responsable.
* Version.
* Destinatario.
* Unidad destinataria.
* Estado de copia.
* Fecha de entrega/asignacion.
* Fecha de cierre/devolucion.
* Ultima actualizacion.

### 6.4 Reporte de implementacion/lectura

Consulta cumplimiento documental desde `ImplementationRecord`.

Campos principales:

* Codigo documental.
* Titulo.
* Tipo documental.
* Unidad responsable.
* Version.
* Unidad destinataria/ejecutora.
* Usuario.
* Estado de implementacion/lectura.
* Fecha de asignacion.
* Fecha de implementacion/confirmacion.
* Ultima actualizacion.

## 7. Filtros disponibles

| Reporte | Filtros disponibles |
| --- | --- |
| Libro Maestro | Tipo documental, unidad responsable, estado, vigencia, codigo, titulo, rango de fecha de creacion. |
| Reporte mensual | Mes, ano, tipo documental, unidad responsable, estado. |
| Copias controladas | Tipo documental, unidad responsable, unidad destinataria, usuario destinatario, estado, codigo, rango de fecha de entrega. |
| Implementacion/lectura | Tipo documental, unidad responsable, unidad destinataria del usuario, usuario, estado, codigo, rango de asignacion, rango de confirmacion. |

Los filtros invalidos no rompen las vistas ni las exportaciones. Cuando el formulario no valida, la vista retorna el reporte sin aplicar criterios invalidos.

## 8. Exportacion CSV

La exportacion CSV de Fase 4 queda implementada como salida controlada inicial.

Controles:

* Login obligatorio.
* Permiso `can_view_reports`.
* Misma fuente de datos que la vista HTML.
* Mismos filtros GET que la vista HTML.
* `Content-Disposition: attachment`.
* `Content-Type: text/csv; charset=utf-8`.
* BOM UTF-8 para compatibilidad basica con hojas de calculo.
* Nombres de archivo fechados.

Exclusiones confirmadas:

* No exporta PDFs.
* No exporta adjuntos.
* No incluye rutas `MEDIA_URL`.
* No incluye rutas fisicas de storage.
* No abre visor documental.
* No implementa Excel `.xlsx`.

## 9. Permisos

Reglas aplicadas:

* Todo reporte requiere usuario autenticado.
* Usuarios no autenticados redirigen al login.
* Usuarios autenticados sin permiso reciben 403.
* Consulta y exportacion usan el mismo permiso funcional.
* El helper central usado es `can_view_reports`.

Acceso funcional actual:

| Rol | Acceso a reportes |
| --- | --- |
| OyM Administrador Funcional | Permitido |
| Analista OyM | Permitido |
| Unidad Ejecutora | Denegado |
| Usuario Lector | Denegado |
| Sistemas Tecnico | Denegado |
| Auditor | Denegado para reportes OyM |

## 10. Auditoria

La auditoria de reportes reutiliza:

```text
AuditAction.REPORT_GENERATED
```

No se crearon nuevos valores de enum para evitar migraciones.

Eventos especificos registrados como metadata:

```text
after_data.report_event = REPORT_VIEWED
after_data.report_event = REPORT_EXPORTED
```

Metadata registrada:

* Usuario.
* Reporte.
* Filtros GET.
* Formato (`html` o `csv`).
* Resultado (`success` o `denied`).
* IP si esta disponible.
* User agent si esta disponible.
* Fecha/hora automatica por `AuditEvent.created_at`.

La auditoria no registra contenido documental, PDFs, adjuntos ni rutas de archivos.

## 11. Validaciones finales

Validaciones registradas para el cierre:

```text
git diff --check -> OK
python -m compileall backend -> OK
make check -> OK
makemigrations --check --dry-run -> No changes detected
apps.reports -> 69 tests OK
make test-base -> 204 tests OK
make healthcheck -> 200 {"status": "ok"}
```

## 12. Limitaciones

Limitaciones actuales:

* Excel `.xlsx` no esta implementado.
* No existe dashboard grafico ejecutivo.
* No existe envio automatico o programado de reportes.
* No existe reporte de solicitudes documentales en Fase 4.
* No existen snapshots historicos de reportes.
* No existe modelo especializado `ReportExport`.
* No se inicio piloto tecnico.

## 13. Riesgos residuales

Riesgos identificados:

* Un CSV exportado por un usuario autorizado puede redistribuirse fuera del sistema.
* Los reportes exponen metadatos documentales operativos, aunque no archivos.
* La correcta autorizacion depende de roles y permisos ya definidos.
* Datos incompletos en modelos base pueden afectar la calidad de los reportes.
* La interpretacion de vencimientos o vigencias avanzadas requiere reglas adicionales de OyM.

Controles compensatorios actuales:

* Permisos por rol.
* Login obligatorio.
* Auditoria de consulta/exportacion.
* Exportacion solo de metadata.
* Pruebas de no exposicion de archivos.
* Documentacion de limitaciones.

## 14. Pendientes

Pendientes recomendados:

* Evaluar Excel `.xlsx` con dependencia justificada.
* Evaluar reporte de solicitudes documentales si OyM lo prioriza.
* Evaluar dashboard ejecutivo de metricas si OyM lo valida.
* Evaluar snapshots o historicos de reportes si se requieren cortes auditables.
* Preparar datos demo o seed especifico para validacion funcional.
* Preparar checklist de usuarios y roles para piloto.
* Preparar guion de validacion de OyM.
* Verificar respaldo/restauracion antes de cualquier piloto.

## 15. Recomendacion para preparacion piloto posterior

Antes de iniciar una prueba tecnica piloto, se recomienda preparar un bloque separado con:

* Dataset demo controlado.
* Usuarios demo por rol.
* Checklist de permisos.
* Checklist de rutas criticas.
* Guion de validacion con OyM.
* Procedimiento de respaldo y restauracion.
* Registro de incidencias.
* Criterios de aceptacion de piloto.

La prueba piloto no se inicia en F4-P11.

## 16. Siguiente bloque recomendado

Opciones recomendadas:

1. Preparacion piloto controlada, si OyM y Sistemas deciden validar lo construido.
2. Fase 5 de notificaciones, si se prioriza continuidad funcional interna.
3. Bloque de Excel/reportes avanzados, si OyM prioriza exportacion `.xlsx`.

La recomendacion tecnica es preparar primero el paquete de piloto controlado, sin desplegarlo todavia, para validar datos, usuarios, respaldos y guion funcional.

## 17. Criterios de cierre

Fase 4 se considera cerrada cuando:

* Los cuatro reportes base estan documentados.
* Las rutas HTML y CSV estan documentadas.
* Permisos y auditoria estan documentados.
* Validaciones finales estan registradas.
* Limitaciones y riesgos residuales estan documentados.
* No se crearon modelos ni migraciones en el cierre.
* No se inicio piloto tecnico.
