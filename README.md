# Claude Desktop Linux Installer

Instalador independiente de Claude Desktop para Linux, diseñado con especial atención a equipos Ubuntu sin permisos de administrador.

> **Estado:** fase inicial de desarrollo. No se promete compatibilidad con Ubuntu 20.04 hasta verificar una solución real y segura.

## Objetivos

- Proyecto independiente; no comparte código ni dependencias con `chatgpt-installer-linux`.
- Instalación por usuario, sin `sudo` ni permisos root.
- Interfaz gráfica propia.
- Acceso desde el menú de aplicaciones de GNOME mediante archivo `.desktop` e icono.
- Detección de arquitectura, distribución, versión de sistema y versión de glibc.
- Validación previa de compatibilidad antes de descargar o instalar.
- Descarga verificable y gestión segura de actualizaciones y desinstalación.
- No modificar bibliotecas del sistema ni reemplazar glibc.

## Compatibilidad

Claude Desktop para Linux tiene requisitos de sistema más recientes que Ubuntu 20.04. La compatibilidad con Ubuntu 20.04 es un objetivo experimental, no una compatibilidad oficial garantizada.

El instalador debe detenerse y explicar el motivo cuando el paquete oficial no pueda ejecutarse de forma segura. No debe intentar resolverlo copiando bibliotecas del sistema, alterando glibc o ignorando dependencias.

## Principios de seguridad

1. No solicitar permisos root.
2. No ejecutar instaladores remotos sin verificar su origen e integridad.
3. No modificar archivos del sistema.
4. No crear enlaces o lanzadores que apunten a rutas inexistentes.
5. Mantener separadas la descarga, validación, instalación y ejecución.
6. Ofrecer desinstalación limpia de los archivos instalados por la aplicación.

## Desarrollo

La primera etapa implementará el diagnóstico del sistema y el diseño del instalador. La integración con el paquete oficial se añadirá después de verificar los requisitos, el formato de distribución y el mecanismo de actualización.

## Licencia

Pendiente de decisión.
