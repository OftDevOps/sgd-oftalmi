# Definicion Tecnica - Visor Documental

## 1. Proposito del visor documental

El visor documental del SGD-OFTALMI debe permitir la consulta controlada de documentos gestionados por Organizacion y Metodos, evitando exponer archivos documentales mediante rutas publicas directas y manteniendo trazabilidad de acceso por usuario, documento y version.

El visor busca reducir el riesgo de descarga, impresion, copia no autorizada y acceso fuera del sistema. Estos controles son mecanismos razonables de aplicacion y operacion, pero no constituyen una proteccion absoluta contra capturas de pantalla, fotografias externas u otros mecanismos fuera del control del navegador.

## 2. Alcance de F3-P01

Este punto define documentalmente la arquitectura tecnica inicial del visor documental.

Incluye:

* Arquitectura propuesta del visor.
* Estrategia de entrega controlada de archivos.
* Formatos soportados inicialmente.
* Restricciones viables y no viables.
* Trazabilidad minima requerida.
* Riesgos tecnicos reales.
* Controles compensatorios recomendados.
* Pendientes para F3-P02.

No incluye implementacion de codigo, modelos, migraciones, vistas, templates, URLs, APIs, librerias externas ni visor PDF real.

## 3. Decision tecnica recomendada

Se recomienda iniciar Fase 3 con un visor documental controlado para PDF, construido sobre la capa web existente de Django templates y protegido por servicios/selectors/permisos del backend.

La entrega de archivos no debe usar enlaces directos a `MEDIA_URL` ni rutas publicas servidas sin validacion de permisos. El archivo debe pasar por una vista o servicio controlado que:

1. Identifique al usuario autenticado.
2. Valide permisos por rol, documento, version y unidad cuando aplique.
3. Registre trazabilidad minima del intento de acceso.
4. Entregue una respuesta de visualizacion controlada solo si la validacion es exitosa.

La API DRF no queda descartada, pero no debe ser el primer mecanismo salvo que el visor requiera interaccion asincrona, componentes especializados o integraciones internas documentadas.

## 4. Arquitectura propuesta del visor

Arquitectura logica inicial:

```text
Usuario autenticado
-> vista Django del documento
-> accion "ver documento"
-> vista/servicio controlado de visor
-> selector de documento/version/archivo
-> helper de permisos por rol/documento/version/unidad
-> servicio de auditoria
-> respuesta de visualizacion controlada
```

Componentes esperados en fases posteriores:

* Vista Django protegida por login para renderizar el contenedor del visor.
* Servicio de consulta que resuelva documento, version vigente y archivo permitido.
* Helper de permisos que confirme si el usuario puede consultar esa version.
* Servicio de auditoria para registrar intentos exitosos y denegados.
* Entrega de archivo sin exponer ruta fisica ni URL publica estable.
* Template de visor con controles de interfaz limitados.
* Marcas de agua visibles cuando aplique.

El almacenamiento de archivos debe seguir fuera del contenedor de aplicacion mediante volumen persistente. El servidor web no debe publicar archivos documentales controlados como contenido estatico abierto.

## 5. Flujo de consulta documental controlada

Flujo recomendado:

1. El usuario inicia sesion con correo institucional.
2. El usuario accede al listado o detalle documental permitido.
3. El sistema muestra solo documentos y versiones consultables para el usuario.
4. El usuario solicita visualizar una version documental.
5. El backend valida que el documento, version y archivo existan.
6. El backend valida permisos de consulta.
7. El backend registra evento de auditoria con resultado exitoso o denegado.
8. El backend entrega el contenido al visor si el acceso esta autorizado.
9. El visor presenta el documento sin exponer descarga directa.

El acceso denegado debe responder con `403` o `404` segun convenga para no revelar informacion sensible de documentos no autorizados.

## 6. Estrategia de entrega controlada de archivos

La restriccion principal de descarga debe basarse en no exponer rutas directas al archivo.

Estrategia recomendada:

* No publicar archivos documentales controlados mediante enlaces directos a `MEDIA_URL`.
* No mostrar rutas fisicas ni nombres internos de almacenamiento al usuario final.
* Entregar el archivo a traves de una vista/servicio backend protegido.
* Validar permisos en cada solicitud de visualizacion.
* Usar respuestas con encabezados orientados a visualizacion en navegador y no a descarga.
* Evitar URLs permanentes o predecibles cuando se implemente el visor.
* Registrar auditoria para accesos exitosos, denegados y errores.
* Evaluar controles de cache para reducir persistencia local no deseada.

Si en una fase posterior se decide delegar entrega a Nginx mediante mecanismos internos, esa decision debe documentarse y mantener validacion previa en Django.

## 7. Formatos soportados inicialmente

Formato inicial recomendado:

| Formato | Estado inicial | Criterio |
| --- | --- | --- |
| PDF | Soportado inicialmente | Formato prioritario para visualizacion controlada en navegador. |
| Imagenes | Evaluable posteriormente | Solo si OyM define documentos visuales controlados no PDF. |
| Word / Excel / PowerPoint | No soportado directamente al inicio | Evaluar conversion previa a PDF o visualizacion controlada posterior. |
| Otros formatos | Fuera de alcance inicial | Requieren decision tecnica especifica. |

El visor debe priorizar PDF porque permite una experiencia de consulta mas estable y reduce la necesidad de exponer archivos editables. Los archivos Office deben evaluarse para conversion previa a PDF o una estrategia controlada futura.

## 8. Restricciones viables y no viables

### 8.1 Descarga

Viable:

* No exponer ruta directa del archivo.
* No ofrecer boton de descarga a usuarios lectores.
* Validar permisos en cada solicitud de visualizacion.
* Usar encabezados de respuesta orientados a visualizacion.
* Registrar auditoria de accesos.

No garantizable:

* Impedir completamente que el navegador o herramientas externas conserven copias temporales.
* Impedir descargas si el archivo se expone accidentalmente por una URL publica.

### 8.2 Impresion

Viable:

* No ofrecer boton de impresion en la interfaz.
* Usar controles de visor y estilos orientados a desalentar impresion.
* Registrar visualizaciones y acciones de acceso.

No garantizable:

* Bloquear al 100% la impresion desde funciones del navegador, sistema operativo o herramientas externas.

### 8.3 Copia

Viable:

* No exponer texto en vistas HTML cuando no sea necesario.
* Usar visor controlado para el archivo.
* Aplicar controles de interfaz que reduzcan seleccion/copia en el navegador.
* Agregar marcas de agua visibles.

No garantizable:

* Impedir al 100% OCR, extraccion desde herramientas externas o copia a partir de capturas.

### 8.4 Captura de pantalla

Viable:

* Marcas de agua con usuario, fecha/hora y datos del documento.
* Auditoria de visualizacion.
* Politicas operativas de uso aceptable.

No garantizable:

* Impedir capturas de pantalla desde sistema operativo, dispositivos externos o herramientas de terceros.

### 8.5 Fotografia externa

Viable:

* Marcas de agua visibles.
* Trazabilidad de acceso.
* Sensibilizacion y controles operativos.

No garantizable:

* Impedir fotografias tomadas con telefonos u otros dispositivos externos.

### 8.6 Acceso directo al archivo

Viable:

* No servir archivos controlados como estaticos publicos.
* Mantener archivos fuera de rutas publicas.
* Exigir vista/servicio controlado para cada acceso.
* Validar permisos antes de entregar contenido.

No garantizable:

* Proteger archivos si se configura incorrectamente Nginx, `MEDIA_URL`, storage o permisos del sistema operativo.

## 9. Trazabilidad minima requerida

Cada intento de visualizacion debe registrar, como minimo:

* Usuario autenticado.
* Documento.
* Version documental.
* Archivo documental cuando aplique.
* Fecha y hora del servidor.
* Accion solicitada, por ejemplo `document_viewed`.
* Resultado: exitoso, denegado o error.
* Modulo de origen.
* Direccion IP si esta disponible.
* User agent si esta disponible.
* Descripcion legible del evento.

La trazabilidad debe aplicarse tanto a accesos autorizados como a intentos denegados, porque ambos son relevantes para control documental.

## 9.1 Reglas de acceso fino implementadas

F3-P03 fortalece la validacion de acceso por usuario, unidad, documento, version y archivo, sin crear modelos nuevos.

Reglas actuales:

| Rol | Acceso a archivo documental controlado |
| --- | --- |
| OyM Administrador Funcional | Puede visualizar archivos PDF documentales, incluyendo versiones no visibles para usuarios generales, por su rol funcional. |
| Analista OyM | Puede visualizar archivos PDF documentales, incluyendo versiones no visibles para usuarios generales, por su rol funcional. |
| Sistemas Tecnico | No accede al contenido documental por esta ruta; recibe `403` si intenta visualizar archivo. |
| Auditor | No accede al contenido documental por esta ruta; recibe `403` si intenta visualizar archivo. |
| Unidad Ejecutora | Puede visualizar PDF vigente si pertenece a la unidad responsable del documento o tiene relacion por copia controlada de su unidad. |
| Usuario Lector | Puede visualizar PDF vigente si tiene relacion directa por registro de implementacion, copia controlada asignada o copia controlada aplicable a su unidad. |

Condiciones obligatorias:

* El archivo debe estar activo.
* El archivo debe ser PDF por `content_type` o nombre de archivo.
* Para usuarios no OyM, documento y version deben estar en estado visible (`published` o `active`).
* Las relaciones directas se validan con registros de implementacion y copias controladas existentes.
* Las relaciones por unidad se validan con unidad responsable del documento o copias controladas asignadas a la unidad.
* Documento, version y archivo inexistentes mantienen respuesta `404`.
* Usuario autenticado sin permiso mantiene respuesta `403` y auditoria de acceso denegado.

### 9.2 Limitacion actual de autorizacion documental

La autorizacion documental de F3-P03 utiliza relaciones existentes del modelo actual:

* Rol del usuario.
* Unidad organizativa del usuario.
* Copia controlada por usuario o unidad.
* Registro de implementacion por usuario.
* Documento.
* Version documental.
* Archivo activo.

Actualmente no existe una matriz formal independiente `documento <-> usuario autorizado` o `documento <-> unidad autorizada`. Esa relacion no debe inventarse tecnicamente sin validacion funcional de Organizacion y Metodos, porque podria modificar el alcance real de consulta documental.

Queda como pendiente futuro evaluar una matriz formal de autorizacion documental si el proceso de OyM lo requiere. Esa evaluacion debe definir alcance funcional, datos requeridos, reglas de mantenimiento, auditoria, impacto en reportes y necesidad de modelos o migraciones.

### 9.3 Vista base de consulta controlada

F3-P04 implementa la primera experiencia funcional del visor documental.

La vista base:

* Renderiza una pagina protegida por login.
* Muestra metadatos basicos de documento, version y archivo.
* Valida permisos usando las reglas de F3-P03.
* Integra la entrega controlada de PDF de F3-P02 mediante `iframe`.
* No expone la ruta fisica ni URL directa del archivo en storage.
* Muestra mensaje controlado para acceso denegado o archivo no disponible.
* Agrega enlace desde el detalle documental solo cuando el usuario puede consultar el archivo.

F3-P04 no implementa bloqueo avanzado de descarga, bloqueo avanzado de impresion, marcas de agua, visor PDF.js custom, conversion Office, APIs, modelos nuevos ni migraciones.

### 9.4 Registro de acceso a documentos

F3-P05 formaliza la trazabilidad documental del visor usando la auditoria base existente.

No se crea un modelo especializado `DocumentAccessLog` en esta etapa porque `AuditEvent` cubre la evidencia minima requerida:

* Usuario.
* Documento.
* Version documental.
* Archivo documental.
* Fecha y hora del servidor.
* Accion `document_viewed`.
* Resultado `success`, `denied` o `failure`.
* Direccion IP cuando esta disponible.
* User agent cuando esta disponible.
* Descripcion normalizada del evento.

Las descripciones normalizadas son:

| Resultado | Descripcion |
| --- | --- |
| `success` | `Document viewer access granted.` |
| `denied` | `Document viewer access denied.` |
| `failure` | `Document viewer access failed because the file is unavailable.` |

La metadata documental se registra en `after_data` con identificadores y datos basicos de documento, version y archivo. Un modelo especializado de acceso documental solo debe evaluarse si OyM requiere reportes analiticos de lectura/consulta, alto volumen de eventos, reglas especificas de retencion o consultas operativas que no convenga resolver sobre `AuditEvent`.

## 10. Riesgos tecnicos reales

| Riesgo | Descripcion |
| --- | --- |
| Exposicion directa de archivos | Publicar `MEDIA_URL` o rutas de storage sin permisos anula el control del visor. |
| Falsa sensacion de seguridad | El visor reduce riesgos, pero no elimina capturas o fotografias externas. |
| Cache del navegador | El navegador puede conservar datos temporales si no se controlan encabezados y flujo. |
| Permisos incompletos | Validar solo rol y no documento/version/unidad puede exponer informacion indebida. |
| Archivos Office editables | Visualizarlos directamente puede facilitar descarga, edicion o copia. |
| Rendimiento | PDFs grandes pueden afectar memoria, ancho de banda y experiencia de usuario. |
| Auditoria excesiva o insuficiente | Registrar demasiado puede generar ruido; registrar poco debilita trazabilidad. |
| Configuracion de infraestructura | Nginx, volumenes y permisos del sistema deben alinearse con la estrategia del visor. |

## 11. Controles compensatorios recomendados

* Permisos backend obligatorios por documento, version, usuario y unidad.
* Auditoria de accesos exitosos y denegados.
* Marcas de agua visibles con usuario, fecha/hora y documento.
* No exposicion directa de archivos en rutas publicas.
* Encabezados de respuesta orientados a visualizacion y control de cache.
* Politicas internas de uso aceptable.
* Revision de configuracion Nginx/storage antes de produccion.
* Pruebas especificas de acceso autorizado, acceso denegado y ausencia de enlaces directos.
* Monitoreo de errores de acceso y patrones anormales de consulta.

## 12. Exclusiones de F3-P01

F3-P01 no implementa:

* Codigo nuevo.
* Modelos.
* Migraciones.
* Vistas.
* Templates.
* URLs.
* APIs.
* Cambios de permisos funcionales.
* Cambios de Docker, Nginx, settings o storage.
* Librerias externas de visor.
* Visor PDF real.
* Conversion de documentos Office.
* Marcas de agua reales.
* Auditoria adicional en codigo.

## 13. Pendientes para F3-P02

F3-P02 debe implementar el primer servicio de entrega controlada de archivos, manteniendo el alcance limitado a PDF y sin crear modelos ni migraciones.

Al cierre de F3-P02 queda implementado:

* Definir rutas internas del visor sin exponer archivo directo.
* Implementar vista Django protegida para entregar PDF.
* Implementar selector de documento/version/archivo consultable y activo.
* Implementar helper de permiso por usuario, documento, version y archivo.
* Registrar auditoria minima de acceso permitido y denegado.
* Agregar pruebas de acceso permitido y denegado.
* Verificar que usuarios lectores no reciban URLs directas de archivos.

Queda pendiente para puntos posteriores:

* Agregar template base del visor PDF.
* Evitar boton de descarga desde la interfaz del visor.
* Definir marcas de agua visibles.
* Fortalecer reglas por asignacion especifica de documento cuando exista ese modelo o servicio.
* Mantener fuera de alcance la conversion Office hasta decision posterior.

## 14. Criterios de aceptacion

F3-P01 se considera aceptado cuando:

* La definicion tecnica del visor queda versionada.
* La arquitectura propuesta no expone archivos por rutas directas.
* PDF queda definido como formato inicial prioritario.
* Office queda pendiente de conversion previa a PDF o evaluacion posterior.
* Las restricciones viables y no garantizables quedan documentadas.
* La trazabilidad minima queda definida.
* Los riesgos tecnicos reales quedan registrados.
* Los pendientes para F3-P02 quedan claros.
* No se implementa codigo, modelos, migraciones, APIs ni frontend avanzado.
* Las validaciones tecnicas del backend siguen pasando.
