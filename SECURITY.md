# Seguridad

- Solo se aceptan manifiestos y paquetes del repositorio APT oficial de Anthropic.
- Huella de la clave fijada: 31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE.
- Se verifica la firma OpenPGP de InRelease.
- Se compara el SHA-256 de Packages con el manifiesto firmado.
- Se compara el SHA-256 del DEB con el índice firmado.
- No se extrae el paquete si falla una comprobación.
- No se ejecutan scripts de instalación del DEB; se utiliza dpkg-deb -x.
- No se usa sudo ni se modifica /usr, glibc o bibliotecas del sistema.
- La AppImage empaqueta el instalador, no redistribuye Claude.
- No se solicitan credenciales de Anthropic o Google.
- La configuración personal se conserva al actualizar o desinstalar.

Ubuntu 20.04 normalmente tiene glibc 2.31 y no satisface el requisito declarado libc6 >= 2.34. Se advierte antes de continuar.

Desarrollador: Francisco Javier Gallego Orellana · Punto Vuela Montejaque  
montejaque@puntosvuela.es
