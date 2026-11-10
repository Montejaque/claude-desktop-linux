# Guía de ayuda · Claude Desktop Installer

**La Central Digital** · José Miguel Leotte · Versión 1.0 · Linux

## 1. Qué hace
Instala Claude Desktop oficial de Anthropic en la cuenta del usuario Linux. La AppImage distribuida es el instalador, no Claude. El paquete de Claude se descarga de Anthropic al realizar la instalación.

## 2. Requisitos
- Linux amd64 o ARM64, si Anthropic publica el paquete para esa arquitectura.
- Escritorio GNOME u otro compatible y conexión a Internet.
- Herramientas del sistema: gpg, gpgv y dpkg-deb.
- Espacio libre suficiente para descargar y extraer el paquete.

No necesita contraseña de administrador. Si falta una herramienta, informa del requisito y no intenta instalarla.

## 3. Abrir la AppImage
1. Descarga Claude-Desktop-Installer-x86_64.AppImage.
2. En Propiedades, activa «Permitir ejecutar el archivo como un programa», o ejecuta chmod +x sobre el archivo.
3. Haz doble clic para abrirlo o ejecútalo desde terminal.

## 4. Instalar Claude
1. Pulsa **Instalar / actualizar**.
2. El instalador consulta el repositorio APT oficial de Anthropic.
3. Descarga la clave y comprueba su huella digital fijada en esta versión.
4. Verifica la firma GPG de InRelease.
5. Comprueba el SHA-256 del índice Packages contra el manifiesto firmado.
6. Selecciona la versión más reciente para la arquitectura.
7. Descarga el DEB y verifica su SHA-256.
8. Extrae en ~/.local/opt/claude-desktop-official.
9. Crea el lanzador GNOME, el icono y el protocolo claude://.

No ejecuta apt install, no utiliza sudo y no modifica /usr.

## 5. Inicio de sesión con Google
El instalador registra claude:// para devolver la autorización del navegador a la aplicación. Si aparece «Termina de iniciar sesión en la aplicación de Claude», pulsa **Abrir Claude**. Si no vuelve a la app, pulsa **Reparar acceso** en el instalador y repite el proceso.

Consulta la asociación con:
\`\`\`bash
xdg-mime query default x-scheme-handler/claude
\`\`\`
El resultado esperado es claude-desktop-official.desktop.

## 6. Comprobar versión
**Comprobar versión** consulta la versión publicada y la compara con la instalada. No actualiza por sí sola.

## 7. Actualizar
Pulsa **Instalar / actualizar**. El nuevo paquete se verifica antes de sustituir la versión anterior. Si la extracción falla, se intenta restaurar la instalación previa. Los datos personales se conservan.

## 8. Reparar acceso
Pulsa **Reparar acceso** si Claude no aparece en el menú, falta el icono o el navegador no devuelve el inicio de sesión. Recrea el wrapper, el archivo .desktop y la asociación claude://.

## 9. Desinstalar
Pulsa **Desinstalar**. Elimina solo la aplicación instalada por este instalador, el wrapper, icono y lanzador. Conserva la configuración personal de Claude.

## 10. Ubuntu 20.04
El paquete oficial consultado declara libc6 >= 2.34; Ubuntu 20.04 normalmente incorpora glibc 2.31. Por tanto, no cumple el requisito declarado. En el equipo de pruebas de Montejaque se comprobó que el paquete oficial se podía extraer y abrir en Ubuntu 20.04, pero no equivale a soporte oficial. El instalador advierte antes de continuar y no sustituye glibc.

## 11. Seguridad
- Verificación de firma GPG, huella de clave y hashes.
- No se solicitan credenciales de Anthropic o Google.
- No se modifica el sistema ni se necesita root.
- La configuración personal se conserva.

## 12. Solución de problemas
- **No abre la AppImage:** activa el permiso de ejecución y comprueba la arquitectura.
- **No se verifica el repositorio:** revisa Internet, fecha/hora, gpg y gpgv. No omitas la verificación.
- **No aparece Claude:** usa Reparar acceso.
- **El navegador no vuelve a Claude:** usa Reparar acceso y consulta xdg-mime query default x-scheme-handler/claude.
- **Falta dpkg-deb:** debe estar disponible para extraer el DEB; el instalador no lo instala automáticamente.
- **La versión nueva falla:** revisa compatibilidad. No fuerces cambios de glibc.

## 13. Desarrollador
**José Miguel Leotte** · **La Central Digital**  
Teléfono: +34 617 92 57 68  
Correo: info@lacentraldigital.es  
Web: https://lacentraldigital.es

Proyecto independiente, no afiliado a Anthropic.
