# Formato de Observaciones e Incidencias de Piloto

## 1. Proposito

Establecer un formato unico para registrar observaciones, incidencias, bloqueos y mejoras detectadas durante la ejecucion del piloto controlado con Organizacion y Metodos.

Este formato no inicia el piloto. Debe usarse solo cuando exista autorizacion explicita para ejecutar la validacion funcional.

## 2. Datos generales de la sesion

| Campo | Valor |
| --- | --- |
| Fecha de sesion |  |
| Ambiente |  |
| Rama | `develop` |
| Commit probado |  |
| Responsable OyM |  |
| Responsable Sistemas |  |
| Observador/auditor |  |
| Hora inicio |  |
| Hora cierre |  |
| Resultado general | Pendiente |

## 3. Registro de observaciones

| Codigo | Fecha/hora | Escenario | Usuario demo | Rol | Modulo | Resultado esperado | Resultado observado | Evidencia | Clasificacion | Responsable sugerido | Estado | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OBS-001 |  |  |  |  |  |  |  |  |  |  | Abierta |  |
| OBS-002 |  |  |  |  |  |  |  |  |  |  | Abierta |  |
| OBS-003 |  |  |  |  |  |  |  |  |  |  | Abierta |  |

## 4. Clasificacion

| Clasificacion | Definicion |
| --- | --- |
| Bloqueo | Impide continuar o compromete seguridad, permisos, datos, auditoria o trazabilidad. |
| Alto | Afecta un flujo principal del MVP, pero permite continuar con control temporal. |
| Medio | Afecta una operacion secundaria, filtro, texto o comportamiento no critico. |
| Bajo | Observacion menor sin impacto funcional critico. |
| Mejora | Solicitud futura fuera del alcance validado del piloto. |

## 5. Estados de seguimiento

| Estado | Uso |
| --- | --- |
| Abierta | Observacion registrada y pendiente de analisis. |
| En analisis | Requiere revision tecnica o funcional. |
| Aceptada | Se acepta como hallazgo valido. |
| Rechazada | No corresponde al alcance o no se reproduce. |
| Diferida | Se pospone para backlog posterior. |
| Cerrada | Quedo resuelta o documentada con decision formal. |

## 6. Evidencia permitida

Se permite adjuntar o referenciar:

* Capturas de pantalla sin datos productivos.
* Ruta de la pantalla visitada.
* Usuario demo utilizado.
* Codigo de escenario del guion.
* Hora aproximada.
* Codigo de evento de auditoria si aplica.
* Archivo CSV demo exportado si no contiene datos sensibles.

No se debe adjuntar:

* Documentos reales.
* Credenciales.
* Respaldos.
* Archivos productivos.
* Capturas con informacion sensible.

## 7. Decision de cierre por observacion

Cada observacion debe cerrar con una de estas decisiones:

| Decision | Significado |
| --- | --- |
| Corregir antes de despliegue interno | Debe resolverse antes de avanzar. |
| Corregir antes de repetir piloto | Debe resolverse antes de nueva sesion. |
| Aceptar con riesgo documentado | OyM y Sistemas aceptan continuar con riesgo conocido. |
| Pasar a backlog | No bloquea el MVP, pero queda pendiente. |
| Fuera de alcance | No corresponde al piloto o al MVP validado. |

## 8. Resultado general de la sesion

Al cerrar la sesion, registrar uno:

| Resultado | Criterio |
| --- | --- |
| Aprobado | Escenarios principales validados sin bloqueos. |
| Aprobado con observaciones | Existen hallazgos no bloqueantes. |
| Suspendido | Existe bloqueo temporal o condicion tecnica recuperable. |
| Rechazado | Existe falla funcional o tecnica critica que invalida el piloto. |

## 9. Firma o conformidad

| Parte | Nombre | Fecha | Conformidad |
| --- | --- | --- | --- |
| Organizacion y Metodos |  |  |  |
| Sistemas |  |  |  |
| Observador/auditor si aplica |  |  |  |

La conformidad puede documentarse mediante acta, correo, ticket interno o registro formal definido por la organizacion.
