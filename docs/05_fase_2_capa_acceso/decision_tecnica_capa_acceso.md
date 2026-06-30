# Decisión Técnica - Fase 2 Capa de Acceso

## 1. Propósito

Este documento formaliza la decisión técnica inicial para la Fase 2 del proyecto SGD-OFTALMI, correspondiente a la capa de acceso del MVP.

La decisión define si la primera interfaz operativa del sistema debe construirse con Django templates, con una API basada en Django REST Framework, o mediante un enfoque híbrido progresivo.

El objetivo es evitar una implementación prematura de pantallas, endpoints, frontend separado o API completa sin una decisión técnica documentada, trazable y coherente con el cierre de la Fase 1.

## 2. Contexto de cierre de Fase 1

La Fase 1 dejó consolidado el backend MVP base del sistema.

Componentes principales ya disponibles:

* Configuración Django, Docker, PostgreSQL y healthcheck.
* Usuario personalizado con correo institucional como identificador.
* Catálogos base de unidades ejecutoras y tipos documentales.
* Modelo documental base.
* Secuencias base de codificación documental.
* Solicitudes documentales base.
* Copias controladas base.
* Registros de implementación base.
* Auditoría base.
* Roles y permisos base.
* Servicios y selectors base.
* Permisos finos por acción y módulo.
* Transiciones de estados documentales.
* Transiciones de estados de solicitudes documentales.
* Servicios de auditoría automática controlada.
* Seed base de catálogos.

La Fase 1 priorizó una base técnica estable, modular y auditable. La lógica de negocio quedó orientada a servicios, selectors, workflows y permisos, lo cual permite construir más de una capa de acceso sin duplicar reglas.

## 3. Necesidad de la Fase 2

La Fase 2 debe habilitar una capa de acceso usable para los perfiles internos del sistema.

Los usuarios finales de unidades ejecutoras necesitan una interfaz sencilla para:

* Consultar documentos asignados o aplicables.
* Confirmar lectura, interpretación, aceptación e implementación.
* Consultar solicitudes documentales según rol.
* Consultar copias controladas según rol.

Organización y Métodos necesita una interfaz operativa para:

* Administrar documentos.
* Gestionar solicitudes documentales.
* Gestionar copias controladas.
* Revisar registros de implementación.
* Consultar auditoría.
* Preparar reportes en fases posteriores.

Sistemas necesita mantener operación técnica, despliegue, soporte y monitoreo sin convertirse en dueño funcional de las reglas documentales.

## 4. Alternativas evaluadas

### 4.1 Django templates

Consiste en construir la interfaz operativa inicial usando vistas Django, templates, formularios, sesiones y permisos del backend.

Ventajas:

* Menor complejidad inicial.
* Adecuado para un MVP interno.
* Reutiliza autenticación, sesiones, CSRF, permisos y formularios de Django.
* Permite construir pantallas operativas más rápido.
* Reduce infraestructura frente a un frontend separado.
* Facilita proteger acciones con permisos backend desde el inicio.

Riesgos:

* Menor flexibilidad que un frontend moderno.
* Puede mezclar lógica en vistas o templates si no se disciplina la arquitectura.
* Requiere cuidado para mantener templates simples y no duplicar reglas.

### 4.2 API con Django REST Framework

Consiste en exponer la capa de acceso inicialmente como API, usando serializers, viewsets o API views, para ser consumida por un frontend separado o integraciones.

Ventajas:

* Mayor separación entre backend y frontend.
* Útil si se confirma un frontend independiente.
* Conveniente para integraciones futuras.
* Escalable para consumo por otras aplicaciones internas.

Riesgos:

* Mayor complejidad inicial.
* Requiere serializers, permisos API, versionado y pruebas de endpoints.
* Puede exigir un frontend separado antes de tener MVP operativo.
* Incrementa la superficie de seguridad y operación.
* Puede retrasar pantallas internas necesarias para OyM.

### 4.3 Enfoque híbrido progresivo

Consiste en iniciar la Fase 2 con Django templates como interfaz operativa interna, manteniendo el backend preparado para exponer API interna con DRF en módulos específicos o fases posteriores.

Ventajas:

* Permite avanzar rápido con pantallas internas.
* No bloquea una API futura.
* Aprovecha los servicios, selectors, workflows y permisos de Fase 1.
* Reduce complejidad temprana.
* Mantiene la lógica de negocio en el backend.
* Permite usar DRF solo cuando exista una necesidad técnica real.

Riesgos:

* Requiere disciplina para no duplicar lógica entre vistas y futuros endpoints.
* Debe quedar claro dónde vive la lógica de negocio.
* Debe evitarse que Django Admin se convierta en interfaz funcional final.
* Requiere documentar cuándo se justifica agregar API.

## 5. Criterios de evaluación

| Criterio | Django templates | API DRF | Enfoque híbrido progresivo |
| --- | --- | --- | --- |
| Velocidad para MVP interno | Alta | Media / baja | Alta |
| Complejidad técnica inicial | Baja | Alta | Media controlada |
| Mantenibilidad | Alta si se usan servicios | Alta si se diseña bien | Alta si no se duplica lógica |
| Seguridad y permisos | Alta con sesiones Django | Alta, pero exige más piezas | Alta si usa permisos compartidos |
| Reutilización de servicios/selectors | Alta | Alta | Alta |
| Experiencia para usuarios internos | Suficiente para MVP | Depende de frontend adicional | Suficiente y extensible |
| Facilidad de pruebas | Alta | Media / alta | Alta si se separan capas |
| Escalabilidad futura | Media | Alta | Alta progresiva |
| Compatibilidad con API futura | Media | Alta | Alta |

## 6. Decisión recomendada

Se recomienda adoptar un enfoque híbrido progresivo para la Fase 2.

La Fase 2 debe iniciar con Django templates como capa de acceso operativa interna del MVP.

Django REST Framework no se descarta. Debe reservarse para API interna en módulos específicos, integraciones futuras, componentes dinámicos o una fase posterior con frontend separado.

Esta decisión se basa en:

* El sistema es interno.
* El usuario funcional principal es Organización y Métodos.
* Los usuarios finales requieren pantallas sencillas y controladas.
* La Fase 1 ya dejó una base backend modular.
* Django Admin no debe ser la interfaz funcional final.
* Django templates permiten avanzar con menor complejidad operativa.
* DRF puede incorporarse sin romper la arquitectura si reutiliza servicios y permisos existentes.

## 7. Alcance inicial de Fase 2

El alcance inicial recomendado para la Fase 2 es:

* Definir estructura base de URLs de la capa web.
* Definir layout base de templates.
* Definir autenticación por sesión Django.
* Definir navegación interna por rol.
* Crear vistas base para módulos principales.
* Mantener Django Admin como herramienta de apoyo técnico y administrativo, no como interfaz funcional final.
* Mantener preparada la ruta futura de API interna bajo un prefijo versionado, por ejemplo `/api/v1/`, sin implementar endpoints funcionales todavía.

## 8. Exclusiones

Esta decisión no autoriza todavía implementar:

* API completa.
* Endpoints funcionales.
* Serializers.
* Viewsets.
* Frontend React completo.
* Integraciones externas.
* JWT, OAuth, LDAP o Active Directory.
* Visor documental final.
* Reportes Excel.
* Workflows completos de aprobación.
* Nuevos modelos.
* Migraciones.
* Cambios de Docker, Nginx o infraestructura.
* Reglas de negocio no validadas por Organización y Métodos.

## 9. Riesgos y controles

| Riesgo | Control |
| --- | --- |
| Mezclar lógica en vistas o templates | Mantener reglas en `services.py`, `selectors.py`, `workflows.py` y `permissions.py`. |
| Duplicar reglas cuando aparezca API | Obligar a vistas y endpoints a reutilizar la misma capa de servicios. |
| Convertir Django Admin en interfaz final | Usar Admin solo como apoyo técnico o administrativo inicial. |
| Construir API prematura | Crear endpoints solo con necesidad funcional o técnica documentada. |
| Exponer archivos documentales directamente | Mantener acceso a archivos detrás de permisos, visor y auditoría. |
| Aumentar complejidad operativa | Mantener despliegue inicial centrado en Django, PostgreSQL y Nginx. |

## 10. Implicaciones para los próximos puntos

Los próximos puntos de Fase 2 deben avanzar en este orden sugerido:

1. Estructura base de URLs, vistas y capa de acceso.
2. Layout base y navegación por rol.
3. Autenticación visual inicial con correo institucional.
4. Pantallas base por módulo.
5. Formularios operativos mínimos para catálogos y solicitudes cuando aplique.
6. Revisión de permisos de acceso por rol y unidad.
7. Definición puntual de endpoints internos solo si alguna pantalla lo requiere.

Todo nuevo punto debe mantener trazabilidad con:

* `AGENTS.md`.
* `docs/00_gobierno_proyecto/alcance_mvp.md`.
* `docs/02_requerimientos/reglas_negocio.md`.
* `docs/03_diseno_funcional/roles_permisos.md`.
* `docs/04_diseno_tecnico/modelo_datos.md`.

## 11. Criterios de aceptación

La decisión se considera aceptada cuando:

* El documento de decisión queda versionado en el repositorio.
* La decisión recomienda enfoque híbrido progresivo.
* Django templates queda definido como primer paso operativo de Fase 2.
* DRF queda reservado para API interna futura o necesidades específicas.
* Las exclusiones quedan explícitas.
* No se implementan cambios de código, modelos, migraciones, templates, URLs ni endpoints como parte de esta tarea documental.
* Las validaciones técnicas del backend siguen pasando.
* El commit se realiza en `develop`.
* El push se realiza únicamente a `origin/develop`.
