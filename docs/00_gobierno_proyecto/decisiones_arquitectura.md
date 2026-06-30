# Decisiones de Arquitectura - SGD-OFTALMI

## Proposito

Este documento registra decisiones tecnicas relevantes del proyecto SGD-OFTALMI.

Las decisiones deben mantener trazabilidad con el alcance validado por Organizacion y Metodos, las restricciones operativas de Sistemas y el roadmap tecnico del MVP.

---

## ADR-001 - F2-P01: Capa de acceso del MVP

**Fecha:** 2026-06-30

**Estado:** Aprobada para implementacion progresiva

**Decision:** Enfoque hibrido controlado.

El MVP usara Django templates como capa principal de interfaz web interna y Django REST Framework solo para API interna cuando una pantalla, componente o integracion lo justifique.

No se construira una API publica en esta fase.

### Contexto

La primera fase del proyecto dejo consolidado el backend base con modelos, servicios, selectors, permisos, workflows iniciales y auditoria base.

La Fase 2 requiere definir la capa de acceso antes de construir pantallas o endpoints definitivos.

Opciones evaluadas:

| Opcion | Ventajas | Riesgos |
| ------ | -------- | ------- |
| Django templates | Menor complejidad inicial, sesiones y CSRF nativos, buena integracion con permisos Django, despliegue simple. | Menor flexibilidad para experiencias altamente interactivas. |
| API DRF + frontend separado | Mayor separacion frontend/backend, util para SPA o integraciones futuras. | Mayor superficie de seguridad, autenticacion mas compleja, mas piezas operativas. |
| Enfoque hibrido | Permite avanzar con interfaz interna simple y reservar API para casos que lo necesitan. | Requiere disciplina para no duplicar reglas entre vistas y API. |

### Justificacion

El sistema es una aplicacion interna de gestion documental, administrada funcionalmente por Organizacion y Metodos y operada tecnicamente por Sistemas.

Para el MVP conviene reducir complejidad operativa y mantener trazabilidad, permisos y auditoria cerca del backend. Django templates permiten construir pantallas internas con autenticacion por sesion, CSRF y permisos del backend sin introducir una SPA completa desde el inicio.

DRF se reserva para API interna versionada, especialmente en:

* Componentes dinamicos.
* Busquedas y autocompletados.
* Transiciones de estado.
* Registro controlado de eventos de auditoria.
* Notificaciones internas futuras.
* Integracion progresiva con componentes React si se justifica.

### Alcance de la decision

Incluido:

* Interfaz principal del MVP con Django templates.
* Django admin como herramienta tecnica y administrativa de apoyo, no como interfaz funcional final.
* API interna con DRF solo cuando haya necesidad tecnica clara.
* Rutas API internas bajo un prefijo versionado, por ejemplo `/api/v1/`.
* Autenticacion inicial por sesion Django y proteccion CSRF.
* Reutilizacion obligatoria de servicios, selectors, workflows y permisos existentes.

Excluido:

* API publica.
* SPA React completa como primera interfaz del MVP.
* Autenticacion JWT o token externo sin requerimiento aprobado.
* Integraciones externas.
* Exposicion directa de archivos documentales.
* Reglas de negocio dentro de vistas o viewsets.

### Reglas tecnicas derivadas

1. Las reglas de negocio deben vivir en `services.py`, `selectors.py`, `workflows.py` o `permissions.py`, no en templates, vistas ni viewsets.
2. Las vistas Django y los endpoints DRF deben reutilizar la misma capa de servicios.
3. Las vistas funcionales deben respetar permisos por rol y unidad ejecutora.
4. Las operaciones criticas deben registrar auditoria controlada cuando aplique.
5. Los archivos documentales no deben exponerse directamente por URL publica.
6. Los usuarios lectores no deben recibir endpoints de descarga, impresion o copia.
7. DRF se agregara como dependencia solo cuando se implementen endpoints reales.
8. React/Vite queda como opcion para componentes especificos o una fase posterior, no como obligacion inmediata del MVP.

### Consecuencias

* La Fase 2 debe iniciar con estructura de vistas Django, templates base, autenticacion y navegacion interna.
* La API debe documentarse como interna y progresiva.
* El despliegue inicial puede mantenerse centrado en backend Django, PostgreSQL, Nginx y archivos estaticos.
* El frontend React existente permanece como estructura vacia hasta que se justifique su uso.

### Criterios de revision futura

La decision podra revisarse si ocurre alguno de estos casos:

* OyM requiere una experiencia altamente interactiva que Django templates no resuelva razonablemente.
* Se aprueba una integracion externa formal.
* Se requiere una aplicacion frontend independiente.
* Se define una API institucional consumida por otros sistemas.
* El visor documental exige componentes frontend especializados.
