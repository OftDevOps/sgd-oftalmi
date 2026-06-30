# API Interna - Especificacion Inicial

## 1. Estado

La API completa aun no esta implementada.

Existe un indice reservado en:

```text
/api/v1/
```

Este indice requiere autenticacion por sesion y solo expone metadata tecnica minima.

La decision F2-P01 define un enfoque hibrido:

```text
Django templates como interfaz principal
+ DRF para API interna progresiva cuando sea necesaria
```

Este documento establece criterios iniciales para evitar que futuros endpoints contradigan la arquitectura del MVP.

---

## 2. Alcance inicial

La API sera interna y versionada.

Prefijo previsto:

```text
/api/v1/
```

No se define API publica en esta fase.

La estructura base no incluye endpoints funcionales de modelos.

---

## 3. Autenticacion

El mecanismo inicial previsto es:

* Sesion Django.
* CSRF.
* Usuario identificado por correo institucional.
* Permisos internos por rol, modulo y unidad cuando aplique.

No se implementara JWT, tokens externos, OAuth, LDAP ni Active Directory sin una decision posterior.

---

## 4. Criterios para crear endpoints

Un endpoint debe crearse solo si cumple al menos una de estas condiciones:

* Lo necesita una pantalla Django para una interaccion asincrona.
* Lo requiere un componente frontend puntual.
* Centraliza una accion que ya existe en servicios o workflows.
* Permite registrar auditoria o trazabilidad de una accion critica.
* Soporta una integracion interna aprobada.

No se deben crear endpoints CRUD genericos para todos los modelos sin necesidad funcional.

---

## 5. Reglas obligatorias

* Los endpoints deben invocar `services.py`, `selectors.py`, `workflows.py` o `permissions.py`.
* No debe duplicarse logica de negocio en serializers o viewsets.
* Toda accion critica debe validar permisos.
* Toda accion critica debe registrar auditoria cuando aplique.
* Los archivos documentales no deben exponerse por URL directa.
* Usuarios lectores no deben recibir endpoints de descarga, impresion o copia.

---

## 6. Endpoints candidatos futuros

Los siguientes endpoints son candidatos, no compromisos de implementacion inmediata:

```text
GET  /api/v1/catalogs/organizational-units/
GET  /api/v1/catalogs/document-types/
GET  /api/v1/documents/
GET  /api/v1/documents/{id}/
POST /api/v1/documents/{id}/transitions/
GET  /api/v1/document-requests/
POST /api/v1/document-requests/{id}/transitions/
POST /api/v1/audit/events/
GET  /api/v1/notifications/
```

La forma final de cada endpoint debe definirse en el punto tecnico correspondiente.
