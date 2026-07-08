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

### 9.5 Reduccion de exposicion de descarga

F3-P06 implementa controles de reduccion de exposicion de descarga. No se presenta como bloqueo absoluto.

Controles aplicados:

* La entrega PDF mantiene `Content-Disposition: inline`.
* No se usa `Content-Disposition: attachment`.
* Se mantiene `Cache-Control: no-store` y `Pragma: no-cache`.
* La respuesta del PDF permite iframe solo desde el mismo origen.
* El iframe del visor usa fragmento `toolbar=0&navpanes=0&scrollbar=1` para reducir toolbar nativo cuando el navegador lo respete.
* El iframe usa `sandbox` sin `allow-downloads`.
* La interfaz no muestra botones ni enlaces de descarga.
* La interfaz no expone la URL fisica del archivo en storage.
* Se agregan controles JavaScript razonables para desalentar menu contextual y atajos de guardar, imprimir o copiar desde la pagina del visor.

Limitaciones:

* El navegador puede seguir ofreciendo opciones nativas de guardar o imprimir.
* Las herramientas del sistema operativo, extensiones, caches internas o visores nativos pueden permitir acciones fuera del control de la aplicacion.
* Estos controles no reemplazan marcas de agua, PDF.js custom ni politicas operativas.
* Una restriccion visual mas fuerte debe evaluarse en un punto posterior con visor especializado, watermarking y controles compensatorios.

### 9.6 Reduccion de exposicion de impresion

F3-P07 implementa controles de reduccion de exposicion de impresion. No se presenta como bloqueo absoluto.

Controles aplicados:

* Se mantiene el bloqueo suave de `Ctrl/Cmd + P` desde la pagina del visor.
* No se agregan botones, enlaces ni acciones visibles de impresion.
* Se agregan reglas CSS `@media print` para ocultar el iframe del visor al imprimir la pagina.
* Se muestra en impresion el mensaje: `La impresion de documentos controlados no esta permitida desde el visor.`
* Se mantiene la trazabilidad documental existente sobre accesos al visor y al archivo controlado.

Limitaciones:

* El visor nativo del navegador o plugin PDF puede ofrecer opciones propias de impresion.
* El sistema operativo, extensiones o herramientas externas pueden imprimir o capturar contenido fuera del control de la aplicacion.
* Controles mas fuertes requieren evaluar PDF.js custom, watermarking y politicas operativas; aun asi, no eliminarian capturas de pantalla o fotografia externa.

### 9.7 Marca de agua o identificacion de usuario

F3-P08 implementa una marca de agua visual en la pagina del visor documental. El control busca aumentar trazabilidad disuasiva y evidencia visual cuando un documento controlado es consultado.

Datos incluidos:

* Usuario autenticado.
* Unidad organizativa del usuario cuando exista.
* Codigo documental.
* Version documental.
* Fecha/hora de visualizacion en la pagina.

Controles aplicados:

* La marca de agua se renderiza en el template del visor, superpuesta al area del iframe.
* La entrega PDF controlada existente no cambia.
* El archivo PDF original no se modifica.
* No se generan copias fisicas ni archivos derivados.
* No se agregan modelos, migraciones, PDF.js custom ni librerias externas.

Limitaciones:

* La marca de agua visual no impide capturas de pantalla, fotografia externa ni herramientas del sistema operativo.
* La marca de agua no queda persistida dentro del PDF descargado o renderizado por el plugin nativo.
* Una marca persistente dentro del PDF requeriria una fase posterior con procesamiento controlado de archivos, evaluacion de rendimiento, almacenamiento temporal o streaming dinamico, y reglas operativas aprobadas por Organizacion y Metodos.

### 9.8 Pruebas de seguridad del visor

F3-P09 no agrega funcionalidades nuevas. Su objetivo es validar con pruebas automatizadas que el visor documental conserva los controles definidos en F3-P02 a F3-P08.

Cobertura reforzada:

* Login requerido para visor y entrega controlada de archivo.
* Acceso permitido cuando existe relacion valida por rol, unidad, copia controlada o registro de implementacion.
* Acceso denegado con `403` para usuario autenticado sin permiso.
* `404` para documento, version o archivo inexistente.
* `404` para archivo activo en base de datos pero no disponible fisicamente.
* `404` para archivo documental inactivo.
* `403` para archivo no PDF o no soportado por el visor inicial.
* Ausencia de rutas fisicas o `MEDIA_URL` en vistas de consulta.
* Headers de seguridad y control de cache en entrega PDF: `Content-Disposition: inline`, `Cache-Control: no-store`, `Pragma: no-cache`, `X-Content-Type-Options`, `X-Frame-Options` y `Content-Security-Policy`.
* Iframe `sandbox` sin `allow-downloads`.
* Ausencia de botones o enlaces de descarga e impresion.
* Presencia del mensaje de impresion restringida.
* Presencia de marca de agua visual.
* Auditoria `DOCUMENT_VIEWED` con resultados `success`, `denied` y `failure`.

F3-P09 no crea modelos, migraciones, PDF.js custom, APIs ni cambios de reglas funcionales. Cualquier desviacion detectada por estas pruebas debe tratarse como correccion estricta de seguridad o trazabilidad, no como expansion funcional.

### 9.9 Limitaciones reales y cierre de Fase 3

F3-P10 cierra documentalmente la Fase 3. El objetivo es dejar una verdad tecnica defendible sobre lo que el visor documental controla, lo que reduce y lo que no puede garantizar.

Controles implementados entre F3-P01 y F3-P09:

* Definicion tecnica del visor documental y su alcance inicial.
* Entrega controlada de archivos mediante backend, sin exponer rutas fisicas ni URL directa de storage.
* Login obligatorio para visor y entrega de archivo.
* Validacion de permisos por rol, documento, version, archivo, unidad, copia controlada y registro de implementacion cuando aplica.
* Respuestas diferenciadas: `403` para usuario autenticado sin permiso y `404` para documento, version, archivo o archivo fisico inexistente.
* Auditoria `DOCUMENT_VIEWED` con resultado `success`, `denied` o `failure`.
* Encabezados de seguridad y cache: `Cache-Control: no-store`, `Pragma: no-cache`, `Content-Disposition: inline`, `X-Content-Type-Options`, `X-Frame-Options` y `Content-Security-Policy`.
* Renderizado del PDF en iframe protegido por ruta controlada.
* Iframe `sandbox` sin `allow-downloads`.
* Reduccion de toolbar nativo mediante fragmento del visor PDF cuando el navegador lo respeta.
* Ausencia de botones o enlaces de descarga e impresion en la interfaz.
* Controles JavaScript razonables para desalentar menu contextual y atajos de guardar, imprimir o copiar desde la pagina.
* CSS de impresion para ocultar el iframe y mostrar mensaje de restriccion.
* Marca de agua visual con usuario, unidad cuando aplica, documento, version y fecha/hora.
* Pruebas automatizadas de seguridad del visor.

Limitaciones y riesgos residuales:

* Captura de pantalla desde sistema operativo, navegador, extension o herramienta externa.
* Fotografia externa tomada con telefono u otro dispositivo.
* Impresion desde visor nativo del navegador, plugin PDF, sistema operativo o herramienta externa.
* Descarga o extraccion mediante herramientas avanzadas si el navegador o plugin expone capacidades fuera del control de la aplicacion.
* OCR sobre capturas, fotografias o copias obtenidas por medios externos.
* Cache o archivos temporales administrados por navegador, sistema operativo o software de terceros.
* Exposicion accidental por configuracion incorrecta de Nginx, `MEDIA_URL`, storage, volumenes o permisos del sistema operativo.
* Falsa sensacion de seguridad si los controles visuales se comunican como bloqueo absoluto.

Controles compensatorios requeridos:

* Mantener permisos backend como control principal, no como control visual.
* Mantener entrega controlada de archivos y evitar publicacion directa de documentos por `MEDIA_URL`.
* Mantener auditoria `DOCUMENT_VIEWED` para accesos exitosos, denegados y fallidos.
* Revisar configuracion Nginx/storage antes de produccion para impedir exposicion directa de documentos.
* Mantener `Cache-Control: no-store` y `Content-Disposition: inline` para la entrega PDF.
* Mantener CSP `frame-ancestors 'self'`, `X-Frame-Options` e iframe sandbox sin `allow-downloads`.
* Mantener marca de agua visual como control disuasivo y evidencia visual.
* Definir politica interna de uso aceptable para documentos controlados.
* Capacitar a usuarios sobre prohibicion de descarga, impresion, copia, captura o redistribucion no autorizada.
* Monitorear eventos de acceso denegado, fallido o patrones anormales de consulta.

Aclaraciones tecnicas de cierre:

* El PDF original no se modifica en Fase 3.
* No se generan copias fisicas, archivos temporales versionados ni PDFs derivados con marca persistente.
* La marca de agua actual es visual en el template, no persistente dentro del archivo.
* Archivos Office quedan pendientes de conversion previa a PDF o evaluacion tecnica posterior.
* PDF.js custom, marcas de agua persistentes, streaming especializado o procesamiento dinamico de PDF quedan fuera de Fase 3.

Criterios de aceptacion de cierre de Fase 3:

* El visor solo permite acceso autenticado.
* El archivo PDF se entrega por ruta backend controlada.
* No se exponen rutas fisicas ni enlaces directos al archivo en la interfaz.
* Los permisos se validan antes de renderizar visor o entregar archivo.
* Los intentos permitidos, denegados y fallidos quedan auditados.
* Los headers de seguridad y cache se validan por pruebas.
* La interfaz no ofrece descarga ni impresion.
* Existe mensaje de impresion restringida y marca de agua visual.
* Las limitaciones reales quedan documentadas sin prometer proteccion absoluta.
* No existen modelos ni migraciones pendientes derivados de Fase 3.

## 10. Riesgos tecnicos reales

| Riesgo | Descripcion |
| --- | --- |
| Exposicion directa de archivos | Publicar `MEDIA_URL` o rutas de storage sin permisos anula el control del visor. |
| Falsa sensacion de seguridad | El visor reduce riesgos, pero no elimina capturas o fotografias externas. |
| Cache del navegador | El navegador puede conservar datos temporales si no se controlan encabezados y flujo. |
| Permisos incompletos | Validar solo rol y no documento/version/unidad puede exponer informacion indebida. |
| Archivos Office editables | Visualizarlos directamente puede facilitar descarga, edicion o copia. |
| OCR | Capturas, fotografias o copias externas pueden procesarse con OCR fuera del sistema. |
| Impresion nativa | Navegador, plugin PDF o sistema operativo pueden ofrecer impresion fuera del control de la aplicacion. |
| Herramientas avanzadas | Extensiones o herramientas externas pueden extraer contenido renderizado en el cliente. |
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
