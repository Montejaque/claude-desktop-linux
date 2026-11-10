# Seguridad

## Procedencia e integridad
- Solo se aceptan manifiestos y paquetes del repositorio APT oficial de Anthropic.
- Huella de la clave fijada: `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`.
- Se verifica la firma OpenPGP de `InRelease`.
- Se compara el SHA-256 de `Packages` con el manifiesto firmado.
- Se compara el SHA-256 del DEB con el índice firmado.
- No se extrae el paquete si falla una comprobación.

## Instalación y datos
- No se ejecutan scripts de instalación del DEB; se utiliza extracción con `dpkg-deb -x`.
- No se usa `sudo` ni se modifica `/usr`, glibc o bibliotecas del sistema.
- La AppImage empaqueta el instalador; no redistribuye el binario de Claude.
- La herramienta no solicita credenciales de Anthropic ni Google.
- La configuración personal de Claude se conserva al actualizar o desinstalar.

## Compatibilidad
El paquete oficial consultado declara `libc6 >= 2.34`. Ubuntu 20.04 normalmente tiene glibc 2.31 y no satisface ese requisito. Se muestra una advertencia antes de continuar. La prueba local no equivale a soporte oficial.

## Contacto del desarrollador
Francisco Javier Gallego Orellana · Punto Vuela Montejaque  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
633 402 959 · montejaque@puntosvuela.es  
https://puntosvuela.es/centros/montejaque
