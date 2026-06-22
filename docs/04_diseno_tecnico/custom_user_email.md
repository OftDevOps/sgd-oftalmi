# Custom User con Email como Username - SGD-OFTALMI

## 1. Propósito del documento

Este documento define la decisión técnica de autenticación para el sistema SGD-OFTALMI.

La regla validada por Organización y Métodos establece que el usuario de acceso al sistema será el correo electrónico institucional.

Por tanto, el backend Django debe implementar un modelo de usuario personalizado desde el inicio del proyecto, usando el campo `email` como identificador principal de autenticación.

## 2. Decisión técnica

El sistema no debe usar el campo `username` tradicional de Django como identificador principal del usuario.

La autenticación debe basarse en correo electrónico institucional.

Decisión:

```text
USERNAME_FIELD = "email"
```

El campo `email` debe ser único.

El modelo de usuario debe definirse antes de ejecutar migraciones definitivas del proyecto.

## 3. Justificación

Esta decisión se toma porque:

* OyM confirmó que el username del sistema será el correo electrónico institucional.
* El correo institucional es un identificador natural para usuarios internos.
* Evita duplicidad entre username y email.
* Facilita notificaciones por correo.
* Facilita auditoría de acciones por usuario.
* Facilita integración futura con directorio corporativo, si se decide posteriormente.
* Evita migraciones complejas si se intenta cambiar el modelo de usuario después.

## 4. Alcance de esta decisión

Esta decisión aplica al módulo:

```text
backend/apps/accounts/
```

Y afecta principalmente:

```text
backend/apps/accounts/models.py
backend/apps/accounts/admin.py
backend/apps/accounts/apps.py
backend/config/settings/base.py
```

También impacta:

```text
AUTH_USER_MODEL
createsuperuser
admin Django
autenticación
auditoría
notificaciones
permisos
relación con unidades ejecutoras
```

## 5. Regla de negocio relacionada

Regla validada por OyM:

```text
El username del sistema será el correo electrónico institucional del usuario.
```

Reglas técnicas derivadas:

| ID          | Regla                                                                        |
| ----------- | ---------------------------------------------------------------------------- |
| RT-AUTH-001 | El sistema debe usar un Custom User desde el inicio.                         |
| RT-AUTH-002 | El campo `email` debe ser único.                                             |
| RT-AUTH-003 | El campo `email` debe ser el `USERNAME_FIELD`.                               |
| RT-AUTH-004 | No debe usarse el campo `username` tradicional como identificador principal. |
| RT-AUTH-005 | El correo debe normalizarse antes de guardar el usuario.                     |
| RT-AUTH-006 | Un usuario inactivo no debe poder autenticarse.                              |
| RT-AUTH-007 | Las acciones críticas deben asociarse al usuario autenticado.                |

## 6. Modelo recomendado

El modelo recomendado debe extender de:

```python
AbstractBaseUser
PermissionsMixin
```

Debe incluir como mínimo:

```text
email
first_name
last_name
is_active
is_staff
is_superuser
date_joined
updated_at
```

Campos recomendados para fases posteriores:

```text
organizational_unit
position
employee_code
is_technical_user
must_change_password
last_password_change
```

Nota: si `organizational_unit` todavía no está definido en el punto 11, puede dejarse para una migración posterior. No debe bloquear la configuración inicial del backend.

## 7. Manager recomendado

Debe implementarse un manager personalizado, por ejemplo:

```python
CustomUserManager
```

Debe soportar:

```text
create_user
create_superuser
normalización de email
validación de email requerido
asignación correcta de is_staff
asignación correcta de is_superuser
```

## 8. Configuración en settings

En `backend/config/settings/base.py` debe declararse:

```python
AUTH_USER_MODEL = "accounts.User"
```

El valor exacto depende del nombre del modelo. Si el modelo se llama `User`, usar:

```python
AUTH_USER_MODEL = "accounts.User"
```

Si se decide llamarlo `CustomUser`, usar:

```python
AUTH_USER_MODEL = "accounts.CustomUser"
```

Recomendación para el proyecto:

```python
AUTH_USER_MODEL = "accounts.User"
```

## 9. Admin Django

El usuario personalizado debe registrarse en el admin de Django.

El admin debe permitir:

* Visualizar email.
* Visualizar nombre y apellido.
* Filtrar por activo, staff y superusuario.
* Buscar por email, nombre y apellido.
* Crear superusuarios correctamente.
* Editar permisos básicos.

Debe evitarse una configuración de admin que dependa del campo `username`.

## 10. Creación de superusuario

El comando:

```bash
python manage.py createsuperuser
```

Debe solicitar el correo electrónico como identificador principal.

Comportamiento esperado:

```text
Email:
Password:
Password confirmation:
```

No debe solicitar un username tradicional como identificador principal.

## 11. Migraciones

Esta decisión debe implementarse antes de generar migraciones de modelos de negocio.

Orden recomendado:

```text
1. Crear modelo User personalizado.
2. Configurar AUTH_USER_MODEL.
3. Crear admin básico.
4. Ejecutar makemigrations accounts.
5. Ejecutar migrate.
6. Validar createsuperuser.
```

No se recomienda cambiar `AUTH_USER_MODEL` después de haber creado modelos relacionados con usuarios.

## 12. Relación con auditoría

Todas las acciones críticas del sistema deberán poder asociarse al usuario autenticado.

Ejemplos:

* Carga documental.
* Visualización documental.
* Solicitud documental.
* Cambio de estado.
* Emisión de constancia.
* Generación de reportes.
* Cambio de permisos.
* Inicio y cierre de sesión.

Por tanto, el modelo de auditoría debe apuntar al usuario configurado en `AUTH_USER_MODEL`, no a un modelo fijo de Django.

## 13. Relación con notificaciones

El correo electrónico institucional será utilizado para:

* Autenticación.
* Notificaciones por documentos pendientes.
* Alertas de nuevas versiones.
* Alertas de solicitudes observadas.
* Alertas operativas cuando aplique.

Por tanto, el campo `email` no debe ser opcional.

## 14. Relación con permisos

El modelo de usuario debe integrarse con el sistema de grupos y permisos de Django.

Recomendación:

* Usar grupos de Django para roles generales.
* Usar permisos personalizados para acciones específicas.
* Mantener la lógica de autorización en `permissions.py` y servicios según corresponda.

Roles funcionales iniciales:

* Organización y Métodos.
* Sistemas.
* Unidad Ejecutora.
* Usuario lector.

## 15. Criterios de aceptación técnica

La implementación se considera correcta cuando:

* Existe un modelo de usuario personalizado.
* El email es único.
* El email es `USERNAME_FIELD`.
* `AUTH_USER_MODEL` apunta al modelo correcto.
* `createsuperuser` usa email.
* El admin Django funciona con el usuario personalizado.
* No se requiere username tradicional para autenticarse.
* Las migraciones iniciales se ejecutan correctamente.
* Las pruebas básicas de creación de usuario y superusuario pasan.

## 16. Pruebas mínimas recomendadas

Agregar pruebas para validar:

* Creación de usuario con email.
* Creación de superusuario.
* Error si el email está vacío.
* Normalización de email.
* Email único.
* Usuario inactivo.
* Flags de superusuario.
* Representación textual del usuario.

## 17. Restricciones para Codex

Codex debe implementar esta decisión en el punto 11 si se configura Django.

Codex no debe:

* Usar el modelo de usuario por defecto de Django.
* Crear dependencias innecesarias para autenticación.
* Implementar login avanzado todavía.
* Implementar recuperación de contraseña en esta fase, salvo que se solicite.
* Implementar integración LDAP o Active Directory en esta fase.
* Implementar roles funcionales completos todavía.
* Crear modelos documentales complejos todavía.

Codex sí puede:

* Crear el modelo de usuario personalizado.
* Crear el manager personalizado.
* Configurar `AUTH_USER_MODEL`.
* Configurar admin básico.
* Crear migración inicial de accounts.
* Crear pruebas básicas para usuario.

