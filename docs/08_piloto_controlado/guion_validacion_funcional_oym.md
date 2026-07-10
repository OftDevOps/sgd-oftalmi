# Guion de Validacion Funcional OyM - PILOTO-P05

## 1. Objetivo del guion

Definir el guion funcional que Organizacion y Metodos usara para validar el MVP del SGD-OFTALMI sobre datos demo controlados, sin iniciar todavia el piloto real.

El objetivo es evitar una revision subjetiva. Cada caso debe tener rol, pasos, resultado esperado, evidencia requerida y criterio de aprobado, observado o bloqueado.

## 2. Alcance de validacion

El guion cubre:

* Login y dashboard.
* Catalogos.
* Documentos.
* Solicitudes documentales.
* Visor documental.
* Copias controladas.
* Implementacion/lectura.
* Auditoria.
* Libro Maestro.
* Reporte mensual documental.
* Reporte de copias controladas.
* Reporte de implementacion/lectura.
* Exportacion CSV.

Quedan fuera:

* Datos productivos.
* Usuarios reales.
* Reglas funcionales nuevas no validadas.
* Workflows completos de aprobacion.
* Notificaciones.
* Excel `.xlsx`.
* Firma electronica.
* Visor PDF.js custom.
* Despliegue productivo.

## 3. Roles participantes

| Rol | Usuario demo | Responsabilidad |
| --- | --- | --- |
| OyM Administrador | `oym.admin.demo@oftalmi.test` | Validar administracion funcional, reportes, Libro Maestro, auditoria funcional y control documental. |
| Analista OyM | `oym.analista.demo@oftalmi.test` | Validar operacion funcional diaria de OyM. |
| Unidad Ejecutora | `unidad.produccion.demo@oftalmi.test` | Validar creacion de solicitudes y consulta segun unidad. |
| Usuario Lector | `lector.produccion.demo@oftalmi.test` | Validar consulta controlada e implementacion/lectura. |
| Auditor | `auditor.demo@oftalmi.test` | Validar acceso restringido a auditoria. |
| Sistemas Tecnico | `sistemas.demo@oftalmi.test` | Acompanamiento tecnico sin definir reglas funcionales. |
| Usuario sin permiso | `sin.permiso.demo@oftalmi.test` | Validar denegaciones. |

## 4. Precondiciones tecnicas

Antes de ejecutar este guion en una sesion funcional real:

* Ambiente local o piloto controlado disponible.
* Rama y commit autorizados registrados.
* `make check` aprobado.
* `makemigrations --check --dry-run` sin cambios.
* `make test-base` aprobado.
* `make healthcheck` con respuesta `200`.
* `seed_base_catalogs` ejecutado.
* `seed_pilot_demo_data` ejecutado.
* Segunda ejecucion de `seed_pilot_demo_data` sin duplicados.
* Datos demo validados segun `evidencia_seed_demo_local.md`.
* Navegador de prueba disponible.
* OyM conoce que los datos son ficticios.

## 5. Usuarios demo a utilizar

| Usuario | Uso principal |
| --- | --- |
| `oym.admin.demo@oftalmi.test` | Reportes, Libro Maestro, documentos, auditoria funcional. |
| `oym.analista.demo@oftalmi.test` | Operacion OyM y reportes. |
| `unidad.produccion.demo@oftalmi.test` | Solicitudes y consulta por unidad. |
| `lector.produccion.demo@oftalmi.test` | Visor e implementacion/lectura. |
| `auditor.demo@oftalmi.test` | Auditoria. |
| `sistemas.demo@oftalmi.test` | Soporte tecnico y restricciones funcionales. |
| `sin.permiso.demo@oftalmi.test` | Escenarios de acceso denegado. |

Las credenciales demo deben comunicarse fuera del repositorio y solo a participantes autorizados.

## 6. Datos demo a utilizar

Documentos principales:

| Codigo | Uso |
| --- | --- |
| `PROC-OYM-DEMO-001` | Documento principal para visor, Libro Maestro y lectura. |
| `INST-PROD-DEMO-001` | Reporte mensual, copia controlada e implementacion. |
| `FORM-RRHH-DEMO-001` | Filtros por estado `under_review`. |
| `MAN-OYM-DEMO-001` | Filtros por estado `obsolete`. |
| `PROC-PROD-DEMO-002` | Acceso denegado para usuario sin relacion. |

Registros demo:

* Copias controladas `C-001`, `C-002`, `C-003`, `C-004`.
* Registros de implementacion `pending`, `accepted`, `implemented`.
* PDFs demo ficticios generados por el seed.

## 7. Reglas de ejecucion del guion

* Cada caso debe marcarse como `Aprobado`, `Observado`, `Bloqueado` o `No aplica`.
* Toda observacion debe indicar rol, pantalla, pasos, resultado obtenido y evidencia.
* No se deben cargar archivos reales.
* No se deben crear usuarios reales.
* No se deben modificar reglas funcionales durante la sesion.
* Sistemas solo registra soporte tecnico; OyM decide aceptacion funcional.
* Si un caso bloqueante falla, se detiene el guion y se registra la causa.

## 8. Escenarios por modulo

### 8.1 Login y dashboard

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| LOGIN-01 | OyM Administrador | Ingresar con `oym.admin.demo@oftalmi.test`. | Login exitoso y dashboard con accesos funcionales OyM. | Captura dashboard. |
| LOGIN-02 | Usuario Lector | Ingresar con `lector.produccion.demo@oftalmi.test`. | Login exitoso y accesos limitados a modulos permitidos. | Captura dashboard lector. |
| LOGIN-03 | Usuario sin permiso | Ingresar con `sin.permiso.demo@oftalmi.test`. | Login exitoso, pero sin acceso a reportes ni auditoria. | Captura navegacion visible. |

### 8.2 Catalogos

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| CAT-01 | OyM Administrador | Abrir catalogo de unidades. | Lista unidades demo sin error. | Captura listado. |
| CAT-02 | OyM Administrador | Abrir catalogo de tipos documentales. | Lista `PROC`, `INST`, `FORM`, `MAN` y tipos base. | Captura listado. |
| CAT-03 | Usuario Lector | Intentar acceder a unidades organizativas si el menu no lo permite. | Sin acceso o 403 segun helper actual. | Captura o codigo observado. |

### 8.3 Documentos

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| DOC-01 | OyM Administrador | Abrir listado documental. | Documentos demo visibles. | Captura listado. |
| DOC-02 | OyM Administrador | Abrir detalle de `PROC-OYM-DEMO-001`. | Metadatos, version y archivo demo visibles. | Captura detalle. |
| DOC-03 | Usuario Lector | Abrir listado documental. | Solo consulta segun permisos; sin acciones de administracion. | Captura listado. |

### 8.4 Solicitudes documentales

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| SOL-01 | Unidad Ejecutora | Abrir listado de solicitudes. | Acceso permitido al modulo. | Captura listado. |
| SOL-02 | Unidad Ejecutora | Crear solicitud demo con tipo `create`, titulo ficticio y unidad `PROD`. | Solicitud creada en ambiente demo, sin workflow completo. | Captura formulario y detalle. |
| SOL-03 | Usuario Lector | Intentar crear solicitud. | Acceso denegado o accion no disponible. | Captura denegacion. |

La solicitud creada durante la validacion debe usar texto ficticio y quedar identificada como demo.

### 8.5 Visor documental

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| VIS-01 | Usuario Lector | Abrir visor de `PROC-OYM-DEMO-001`. | Visor 200, PDF inline, marca de agua visual. | Captura visor. |
| VIS-02 | Usuario Lector | Revisar que no existan botones propios de descarga o impresion. | No hay controles de descarga/impresion desde la interfaz. | Captura visor. |
| VIS-03 | Usuario sin permiso | Intentar abrir `PROC-PROD-DEMO-002`. | 403 o mensaje controlado. | Captura denegacion. |
| VIS-04 | Auditor | Intentar abrir contenido documental. | Acceso denegado; auditor no consulta contenido documental. | Captura denegacion. |

Nota: el visor reduce exposicion, pero no impide al 100% capturas, fotografia externa ni controles nativos del navegador.

### 8.6 Copias controladas

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| CC-01 | OyM Administrador | Abrir listado de copias controladas. | Visualiza copias demo `C-001` a `C-004`. | Captura listado. |
| CC-02 | Usuario Lector | Abrir copias controladas aplicables. | Visualiza copias relacionadas a su usuario/unidad. | Captura listado. |
| CC-03 | Usuario sin permiso | Abrir copias controladas. | Sin copias aplicables o acceso limitado segun helper. | Captura resultado. |

### 8.7 Implementacion/lectura

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| IMP-01 | Usuario Lector | Abrir registros propios de implementacion. | Visualiza registros demo pendientes/aceptados aplicables. | Captura listado. |
| IMP-02 | OyM Administrador | Abrir reporte o listado de implementacion. | Visualiza registros demo por documento/usuario. | Captura listado. |
| IMP-03 | Usuario sin permiso | Abrir registros propios. | No visualiza registros demo ajenos. | Captura resultado. |

### 8.8 Auditoria

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| AUD-01 | Auditor | Abrir listado de auditoria. | Acceso permitido. | Captura listado. |
| AUD-02 | Auditor | Buscar eventos de visor o reportes generados durante validacion. | Eventos visibles con usuario, accion y resultado. | Captura detalle. |
| AUD-03 | Usuario Lector | Intentar abrir auditoria. | 403 o acceso no disponible. | Captura denegacion. |

### 8.9 Libro Maestro

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| LM-01 | OyM Administrador | Abrir `/app/reports/master-book/`. | Lista documentos demo. | Captura reporte. |
| LM-02 | OyM Administrador | Filtrar por tipo `PROC`. | Muestra documentos demo de tipo procedimiento. | Captura filtro. |
| LM-03 | Usuario Lector | Intentar acceder al Libro Maestro. | Acceso denegado. | Captura 403. |

### 8.10 Reporte mensual

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| RM-01 | OyM Administrador | Abrir reporte mensual. | Muestra versiones publicadas del periodo demo. | Captura reporte. |
| RM-02 | OyM Administrador | Cambiar filtros de mes/ano o tipo. | Filtros no rompen la vista. | Captura filtros. |

### 8.11 Reporte de copias controladas

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| RCC-01 | OyM Administrador | Abrir reporte de copias controladas. | Muestra `C-001` a `C-004`. | Captura reporte. |
| RCC-02 | OyM Administrador | Filtrar por estado `active` o `retired`. | Muestra resultados acordes al estado. | Captura filtro. |

### 8.12 Reporte de implementacion/lectura

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| RIM-01 | OyM Administrador | Abrir reporte de implementacion/lectura. | Muestra registros `pending`, `accepted`, `implemented`. | Captura reporte. |
| RIM-02 | OyM Administrador | Filtrar por usuario `lector.produccion.demo@oftalmi.test`. | Muestra registros asociados al usuario. | Captura filtro. |

### 8.13 Exportacion CSV

| Caso | Rol | Pasos | Resultado esperado | Evidencia |
| --- | --- | --- | --- | --- |
| CSV-01 | OyM Administrador | Exportar Libro Maestro. | Descarga CSV, no PDF, no rutas `/media/`. | Archivo CSV demo. |
| CSV-02 | OyM Administrador | Exportar reporte mensual. | Descarga CSV con datos demo. | Archivo CSV demo. |
| CSV-03 | OyM Administrador | Exportar copias controladas. | Descarga CSV con copias demo. | Archivo CSV demo. |
| CSV-04 | OyM Administrador | Exportar implementacion/lectura. | Descarga CSV con registros demo. | Archivo CSV demo. |
| CSV-05 | Usuario Lector | Intentar exportar CSV. | 403 o acceso no disponible. | Captura denegacion. |

## 9. Resultado esperado general

El MVP queda funcionalmente aprobado para continuar preparacion de piloto si:

* OyM puede navegar las pantallas base sin errores criticos.
* Los roles ven solo lo que corresponde.
* Los documentos demo se consultan con control.
* Los reportes muestran datos demo coherentes.
* Las exportaciones CSV no exponen archivos ni rutas.
* La auditoria permite verificar consultas relevantes.
* Las observaciones no bloquean seguridad, trazabilidad ni acceso por rol.

## 10. Evidencia requerida

Cada escenario debe recolectar:

* Fecha y hora.
* Usuario demo usado.
* Pantalla o ruta.
* Resultado obtenido.
* Captura de pantalla o archivo CSV cuando aplique.
* Observacion si difiere del resultado esperado.
* Clasificacion: `Aprobado`, `Observado`, `Bloqueado`, `No aplica`.

Las evidencias no deben contener datos reales.

## 11. Criterios de aceptacion

El guion puede cerrarse como aceptado si:

* Todos los casos criticos de login, permisos, visor, reportes y auditoria estan aprobados.
* Las observaciones no bloqueantes tienen responsable y accion definida.
* OyM confirma que el flujo demo representa el MVP esperado.
* Sistemas confirma estabilidad tecnica del ambiente.
* No se identifican exposiciones de archivos documentales.
* No se requiere modificar reglas funcionales durante la sesion.

## 12. Criterios de rechazo o bloqueo

El guion debe marcarse como bloqueado si ocurre cualquiera de estos eventos:

* Usuario sin permiso accede a reportes, auditoria o documento no autorizado.
* Se expone ruta fisica de archivo o `MEDIA_URL`.
* CSV exporta archivos, rutas o contenido documental no reportable.
* El visor permite acceso no autorizado.
* Falla login de roles criticos.
* No se puede consultar Libro Maestro o reportes base.
* La auditoria no registra eventos relevantes.
* OyM identifica una regla funcional incorrecta.
* El ambiente no puede restaurarse o estabilizarse.

## 13. Matriz de trazabilidad

| Caso | Modulo | Rol principal | Resultado esperado |
| --- | --- | --- | --- |
| LOGIN-01 | Autenticacion | OyM Administrador | Login y dashboard correctos. |
| LOGIN-02 | Autenticacion | Usuario Lector | Acceso limitado por rol. |
| LOGIN-03 | Autenticacion | Usuario sin permiso | Sin reportes ni auditoria. |
| CAT-01 | Catalogos | OyM Administrador | Unidades visibles. |
| CAT-02 | Catalogos | OyM Administrador | Tipos documentales visibles. |
| DOC-01 | Documentos | OyM Administrador | Documentos demo visibles. |
| DOC-02 | Documentos | OyM Administrador | Detalle documental correcto. |
| SOL-01 | Solicitudes | Unidad Ejecutora | Modulo accesible. |
| SOL-02 | Solicitudes | Unidad Ejecutora | Solicitud demo creada. |
| VIS-01 | Visor | Usuario Lector | PDF controlado visible. |
| VIS-03 | Visor | Usuario sin permiso | Acceso denegado. |
| CC-01 | Copias controladas | OyM Administrador | Copias demo visibles. |
| IMP-01 | Implementacion | Usuario Lector | Registros propios visibles. |
| AUD-01 | Auditoria | Auditor | Auditoria visible. |
| LM-01 | Libro Maestro | OyM Administrador | Reporte carga con datos demo. |
| RM-01 | Reporte mensual | OyM Administrador | Reporte carga con periodo demo. |
| RCC-01 | Reporte copias | OyM Administrador | Copias demo visibles. |
| RIM-01 | Reporte implementacion | OyM Administrador | Registros demo visibles. |
| CSV-01 | Exportacion | OyM Administrador | CSV seguro. |
| CSV-05 | Exportacion | Usuario Lector | Acceso denegado. |

## 14. Formato de observaciones

Cada observacion debe registrarse asi:

```text
ID del caso:
Usuario demo:
Modulo:
Resultado esperado:
Resultado obtenido:
Evidencia:
Severidad: critica / mayor / menor / mejora
Responsable: OyM / Sistemas / mixto
Decision: aprobar / observar / bloquear / no aplica
Accion requerida:
Fecha objetivo:
```

## 15. Reglas de cierre del piloto funcional

Al cerrar la validacion funcional:

1. OyM debe emitir resultado: aprobado, aprobado con observaciones o rechazado.
2. Sistemas debe emitir resultado tecnico: estable, estable con observaciones o bloqueado.
3. Las observaciones deben clasificarse.
4. Los bloqueos deben resolverse antes de pasar a despliegue interno.
5. No se debe promover `develop` a `main` sin aprobacion explicita.
6. No se deben mezclar datos demo con datos productivos.
7. El cierre debe quedar documentado en un acta o documento de evidencia posterior.

## 16. Pendiente posterior

El siguiente punto recomendado es:

```text
PILOTO-P06 -> Ejecucion controlada de validacion funcional OyM
```

Ese punto solo debe ejecutarse cuando OyM y Sistemas autoricen formalmente la sesion de validacion. PILOTO-P05 solo deja preparado el guion.
