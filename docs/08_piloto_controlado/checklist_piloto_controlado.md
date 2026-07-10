# Checklist de Piloto Controlado - SGD-OFTALMI

Este checklist prepara el piloto tecnico controlado. No autoriza por si solo iniciar la prueba, crear usuarios reales ni cargar datos productivos.

## 1. Control previo

- [ ] Existe aprobacion formal para preparar el piloto.
- [ ] Existe aprobacion separada para iniciar el piloto.
- [ ] La rama activa es `develop`.
- [ ] `main` no sera modificada sin autorizacion explicita.
- [ ] No se usara `force push`.
- [ ] `docs/continuidad/` no sera incluida salvo instruccion explicita.
- [ ] No se cargaran datos productivos.
- [ ] No se crearan usuarios reales de operacion.

## 2. Repositorio y validaciones base

- [ ] `git status` revisado.
- [ ] `git log --oneline --decorate -20` revisado.
- [ ] `make check` aprobado.
- [ ] `docker compose exec backend python manage.py makemigrations --check --dry-run` sin cambios.
- [ ] `make test-base` aprobado.
- [ ] `make healthcheck` con respuesta `200`.
- [ ] El commit de referencia del piloto esta identificado.
- [ ] `docs/08_piloto_controlado/datos_demo_y_usuarios_prueba.md` revisado y aprobado antes de crear datos.
- [ ] `seed_base_catalogs` ejecutado antes de `seed_pilot_demo_data`.
- [ ] `seed_pilot_demo_data --dry-run` revisado antes de escribir datos demo.

## 3. Entorno tecnico

- [ ] Ambiente de piloto definido.
- [ ] Variables de entorno no productivas revisadas.
- [ ] `SECRET_KEY` no productiva configurada fuera del repositorio.
- [ ] PostgreSQL operativo.
- [ ] Backend operativo.
- [ ] Volumen de media configurado para archivos demo.
- [ ] Healthcheck disponible.
- [ ] Logs accesibles para diagnostico.
- [ ] No hay exposicion directa de `MEDIA_URL` para documentos controlados.
- [ ] El comando `seed_pilot_demo_data` esta disponible en el backend.
- [ ] La contrasena demo local fue comunicada solo a participantes autorizados del piloto.

## 4. Respaldo y restauracion

- [ ] Respaldo inicial de base de datos creado.
- [ ] Respaldo inicial de archivos demo creado.
- [ ] Respaldo identificado con fecha, ambiente, commit y responsable.
- [ ] Restauracion de prueba ejecutada.
- [ ] Resultado de restauracion documentado.
- [ ] Procedimiento de rollback definido.

## 5. Usuarios demo

- [ ] La matriz usuario -> rol -> unidad -> permisos esperados fue revisada.
- [ ] Usuario demo OyM Administrador preparado.
- [ ] Usuario demo Analista OyM preparado.
- [ ] Usuario demo Unidad Ejecutora preparado.
- [ ] Usuario demo Usuario Lector preparado.
- [ ] Usuario demo Sistemas Tecnico preparado.
- [ ] Usuario demo Auditor preparado.
- [ ] Usuario demo sin permiso preparado para escenarios negativos.
- [ ] Correos demo no corresponden a usuarios productivos reales.
- [ ] Roles asignados coinciden con permisos esperados.

## 6. Datos demo

- [ ] Unidades organizativas demo cargadas.
- [ ] Tipos documentales demo cargados.
- [ ] Documentos demo cargados.
- [ ] Versiones documentales demo cargadas.
- [ ] Archivos PDF demo cargados.
- [ ] Solicitudes documentales demo disponibles.
- [ ] Copias controladas demo disponibles.
- [ ] Registros de implementacion/lectura demo disponibles.
- [ ] No hay documentos sensibles o productivos.
- [ ] Documentos demo cubren estados `active`, `published`, `under_review` y `obsolete`.
- [ ] Copias controladas demo cubren estados `active`, `delivered`, `retired` y `registered`.
- [ ] Registros de implementacion cubren estados `pending`, `accepted` e `implemented`.
- [ ] El resumen de `seed_pilot_demo_data` fue revisado.
- [ ] Reejecutar `seed_pilot_demo_data` no duplica datos demo.

## 7. Seguridad y permisos

- [ ] Usuario anonimo no accede a `/app/`.
- [ ] Usuario anonimo no accede a reportes.
- [ ] Usuario anonimo no accede al visor documental.
- [ ] Usuario autenticado sin permiso recibe 403 donde corresponde.
- [ ] OyM accede a reportes autorizados.
- [ ] Usuario lector no accede a reportes.
- [ ] Sistemas Tecnico no modifica reglas funcionales.
- [ ] Auditor accede solo a auditoria segun helpers existentes.

## 8. Visor documental

- [ ] PDF demo abre desde ruta protegida.
- [ ] PDF demo no expone ruta fisica.
- [ ] PDF demo no expone `MEDIA_URL`.
- [ ] Usuario autorizado puede visualizar.
- [ ] Usuario sin permiso recibe 403.
- [ ] Documento, version o archivo inexistente responde 404.
- [ ] `Cache-Control: no-store` validado.
- [ ] `Content-Disposition: inline` validado.
- [ ] No hay botones de descarga.
- [ ] No hay botones de impresion.
- [ ] Mensaje de restriccion de impresion visible.
- [ ] Marca de agua visual presente.
- [ ] Auditoria de acceso permitido registrada.
- [ ] Auditoria de acceso denegado registrada cuando aplique.

## 9. Reportes y CSV

- [ ] Libro Maestro carga correctamente.
- [ ] Reporte mensual carga correctamente.
- [ ] Reporte de copias controladas carga correctamente.
- [ ] Reporte de implementacion/lectura carga correctamente.
- [ ] Filtros principales funcionan con datos demo.
- [ ] Exportacion CSV de Libro Maestro funciona.
- [ ] Exportacion CSV de reporte mensual funciona.
- [ ] Exportacion CSV de copias controladas funciona.
- [ ] Exportacion CSV de implementacion/lectura funciona.
- [ ] CSV se descarga como `attachment`.
- [ ] CSV usa UTF-8/BOM.
- [ ] CSV no contiene PDFs.
- [ ] CSV no contiene adjuntos.
- [ ] CSV no contiene rutas fisicas.
- [ ] CSV no contiene `MEDIA_URL`.

## 10. Auditoria

- [ ] Evento de visualizacion documental registrado.
- [ ] Evento de acceso denegado registrado cuando aplique.
- [ ] Evento de consulta de reporte registrado.
- [ ] Evento de exportacion CSV registrado.
- [ ] Evento incluye usuario.
- [ ] Evento incluye resultado.
- [ ] Evento incluye modulo o accion.
- [ ] Evento incluye IP cuando esta disponible.
- [ ] Evento incluye user agent cuando esta disponible.
- [ ] Evento no registra contenido sensible del documento.

## 11. Guion funcional OyM

- [ ] `docs/08_piloto_controlado/guion_validacion_funcional_oym.md` revisado por OyM.
- [ ] Escenarios por modulo revisados antes de convocar usuarios.
- [ ] Evidencias requeridas definidas.
- [ ] Formato de observaciones aprobado.
- [ ] OyM valida acceso por rol.
- [ ] OyM valida catalogos.
- [ ] OyM valida documentos y versiones demo.
- [ ] OyM valida solicitud documental base.
- [ ] OyM valida copia controlada base.
- [ ] OyM valida registro de implementacion/lectura.
- [ ] OyM valida Libro Maestro.
- [ ] OyM valida reportes.
- [ ] OyM valida exportacion CSV como salida temporal.
- [ ] OyM registra observaciones funcionales.
- [ ] OyM emite resultado: aprobado, aprobado con observaciones o rechazado.

## 12. Criterios de bloqueo

- [ ] Se detiene si falla healthcheck.
- [ ] Se detiene si existen migraciones pendientes.
- [ ] Se detiene si fallan pruebas base criticas.
- [ ] Se detiene si usuario sin permiso accede a informacion restringida.
- [ ] Se detiene si se exponen rutas directas de archivos.
- [ ] Se detiene si no existe respaldo previo.
- [ ] Se detiene si no se puede restaurar el ambiente.
- [ ] Se detiene si OyM detecta regla funcional incorrecta.

## 13. Cierre del piloto

- [ ] Evidencias recolectadas.
- [ ] Incidencias registradas.
- [ ] Riesgos residuales actualizados.
- [ ] Resultado funcional emitido por OyM.
- [ ] Resultado tecnico emitido por Sistemas.
- [ ] Acciones correctivas priorizadas.
- [ ] Decision de continuar, corregir o rechazar documentada.
- [ ] Recomendacion sobre despliegue interno documentada.

## 14. Preparacion operativa PILOTO-P06

- [ ] `docs/08_piloto_controlado/instructivo_operativo_piloto_oym.md` revisado.
- [ ] `docs/08_piloto_controlado/formato_observaciones_piloto.md` disponible.
- [ ] Responsables OyM y Sistemas identificados.
- [ ] Ambiente objetivo no productivo definido.
- [ ] Ventana de prueba sugerida definida.
- [ ] URLs de acceso esperadas revisadas.
- [ ] Procedimiento de carga o recarga seed demo revisado.
- [ ] Manejo seguro de credenciales demo definido fuera del repositorio.
- [ ] Respaldo previo definido.
- [ ] Restauracion o rollback definido.
- [ ] Checklist de arranque revisado.
- [ ] Checklist de cierre revisado.
- [ ] Criterios para aprobar piloto revisados.
- [ ] Criterios para suspender piloto revisados.
- [ ] Confirmado que PILOTO-P06 no inicia el piloto real.

## 15. Evidencia tecnica local PILOTO-P04

Resultado de la ejecucion controlada local:

- [x] `seed_base_catalogs` ejecutado.
- [x] `seed_pilot_demo_data --dry-run` ejecutado.
- [x] `seed_pilot_demo_data` ejecutado.
- [x] `seed_pilot_demo_data` reejecutado para validar idempotencia.
- [x] Usuarios, unidades, tipos, documentos, versiones, PDFs demo, copias y registros validados.
- [x] Selectors de reportes devuelven datos demo.
- [x] Vistas de reportes cargan con 200.
- [x] Exportaciones CSV cargan con 200 y `attachment`.
- [x] CSV no expone `/media/` ni `MEDIA_URL`.
- [x] Auditoria de consulta/exportacion de reportes validada.
- [x] Visor documental permitido y denegado validado.
- [x] No se inicio piloto real con OyM.
- [x] No se usaron datos productivos.

Evidencia:

```text
docs/08_piloto_controlado/evidencia_seed_demo_local.md
```
