# Claude Desktop Installer para Linux

Instalador gráfico independiente para **Claude Desktop oficial de Anthropic**. Descarga el paquete DEB desde el repositorio APT oficial, verifica la firma GPG del manifiesto, el SHA-256 del índice y el SHA-256 del paquete y lo extrae en el perfil del usuario, sin sudo.

Desarrollado por **José Miguel Leotte · La Central Digital**.

## Funciones
- Interfaz en español siguiendo la línea visual de los instaladores de VS Code y Codex: blanco, acento amarillo, estado, progreso y registro.
- Verificación de la huella de la clave de Anthropic, firma InRelease, hash del índice Packages y hash del DEB.
- Instalación y actualización en ~/.local/opt/claude-desktop.
- Lanzador GNOME, icono y asociación del protocolo claude://.
- Reparación de acceso, comprobación de versión y desinstalación no destructiva.
- AppImage del instalador, documentación técnica y guía de ayuda PDF/Markdown.

## Compatibilidad
El paquete oficial consultado declara libc6 >= 2.34. Ubuntu 20.04 normalmente incorpora glibc 2.31 y queda fuera de ese requisito. El instalador avisa y permite continuar bajo responsabilidad del usuario, sin modificar glibc ni bibliotecas del sistema. En el equipo de pruebas de Montejaque, el paquete oficial se extrajo y abrió en Ubuntu 20.04; esto no equivale a soporte oficial ni garantiza futuras versiones.

## Ejecutar desde código
\`\`\`bash
python3 -m claude_installer.app
\`\`\`
Requisitos: Python 3.8+, Tkinter, gpg, gpgv y dpkg-deb.

## Construir AppImage
Consulta docs/BUILD_APPIMAGE.md. La AppImage contiene el instalador; Claude Desktop se descarga directamente de Anthropic al instalar.

## Documentación
- docs/GUIA_USUARIO.md
- docs/INSTALACION.md
- docs/BUILD_APPIMAGE.md
- SECURITY.md

## Desarrollador y contacto
**José Miguel Leotte** · **La Central Digital**  
Teléfono: +34 617 92 57 68  
Correo: info@lacentraldigital.es  
Web: https://lacentraldigital.es

Claude y Anthropic son marcas de sus titulares. Este instalador es independiente y no está afiliado, patrocinado ni certificado por Anthropic.
