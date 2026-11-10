# Guía de ayuda · Claude Desktop Installer

**Punto Vuela Montejaque** · Versión 1.0.1 · Linux

## 1. Qué hace esta herramienta
Instala Claude Desktop oficial de Anthropic en la cuenta del usuario Linux. La AppImage distribuida es el instalador, no la aplicación Claude. El paquete de Claude se descarga desde el repositorio oficial de Anthropic cuando se realiza la instalación.

## 2. Requisitos
- Linux de 64 bits (x86_64/amd64). La arquitectura ARM64 solo será compatible si Anthropic publica el paquete correspondiente y el instalador la admite.
- Entorno gráfico de escritorio; GNOME es el entorno de referencia.
- Conexión a Internet.
- Python 3.8 o superior y Tkinter si se ejecuta desde el código.
- Herramientas del sistema: `gpg`, `gpgv` y `dpkg-deb`.
- Espacio libre suficiente para descargar y extraer el paquete.

No necesita contraseña de administrador ni permisos `sudo`.

## 3. Abrir la AppImage
1. Descarga `Claude-Desktop-Installer-x86_64.AppImage` desde la sección **Releases** del repositorio.
2. En Propiedades del archivo, activa «Permitir ejecutar el archivo como un programa», o ejecuta:
   ```bash
   chmod +x Claude-Desktop-Installer-x86_64.AppImage
   ```
3. Haz doble clic en el archivo o ejecútalo desde una terminal:
   ```bash
   ./Claude-Desktop-Installer-x86_64.AppImage
   ```

## 4. Instalar Claude Desktop
1. Pulsa **Instalar / actualizar**.
2. El instalador consulta el repositorio APT oficial de Anthropic.
3. Comprueba la huella de la clave pública de Anthropic.
4. Verifica la firma OpenPGP del fichero `InRelease`.
5. Comprueba el SHA-256 del índice `Packages` contra el manifiesto firmado.
6. Descarga el paquete DEB y verifica su SHA-256.
7. Extrae el contenido en `~/.local/opt/claude-desktop`.
8. Crea el lanzador de escritorio, el icono y la asociación del protocolo `claude://`.

No ejecuta `apt install`, no utiliza `sudo` y no modifica `/usr` ni las bibliotecas del sistema.

## 5. Primer inicio de sesión
El instalador registra el protocolo `claude://` para que el navegador pueda devolver a Claude la autorización del inicio de sesión. Si el navegador muestra «Termina de iniciar sesión en la aplicación de Claude», utiliza **Abrir Claude** si se ofrece esa opción.

Si el retorno no abre la aplicación:
1. Cierra Claude.
2. Abre de nuevo el instalador.
3. Pulsa **Reparar acceso**.
4. Repite el inicio de sesión.

Puedes consultar qué aplicación gestiona el protocolo con:
```bash
xdg-mime query default x-scheme-handler/claude
```
El resultado esperado es `claude-desktop.desktop`.

## 6. Comprobar la versión
Pulsa **Comprobar versión** para consultar la versión publicada por Anthropic y compararla con la instalada. Esta acción solo informa: no actualiza la aplicación.

## 7. Actualizar
Pulsa **Instalar / actualizar**. El paquete nuevo se verifica antes de sustituir la versión anterior. Si la extracción falla, el instalador intenta restaurar la instalación previa. La configuración personal de Claude se conserva.

## 8. Reparar el acceso
Pulsa **Reparar acceso** si Claude no aparece en el menú de aplicaciones, falta el icono o el navegador no devuelve el inicio de sesión. Esta función vuelve a crear el wrapper, el lanzador de escritorio y la asociación `claude://`.

## 9. Desinstalar
Pulsa **Desinstalar** y confirma la operación. Se elimina la aplicación instalada por esta herramienta, su wrapper, icono y lanzador. **La configuración y los datos personales de Claude no se eliminan.**

## 10. Aviso para Ubuntu 20.04
El paquete oficial consultado declara `libc6 >= 2.34`. Ubuntu 20.04 normalmente incorpora glibc 2.31 y no satisface ese requisito. En el equipo de pruebas de Montejaque se comprobó que el paquete oficial se podía extraer y abrir en Ubuntu 20.04, pero esto no supone soporte oficial ni garantiza que futuras versiones funcionen.

El instalador informa de esta incompatibilidad antes de continuar. No actualices glibc manualmente ni sustituyas las bibliotecas del sistema para forzar la instalación.

## 11. Seguridad y solución de problemas
- La herramienta verifica la huella de la clave, la firma GPG y los hashes antes de extraer el paquete.
- Si falla una comprobación criptográfica, no continúes ni intentes omitirla.
- Si hay errores de descarga, revisa la conexión a Internet y la fecha y hora del equipo.
- Si falta `dpkg-deb`, debe estar disponible para extraer el paquete.
- Si no aparece el icono o falla el retorno desde el navegador, utiliza **Reparar acceso**.
- La herramienta no solicita ni almacena la contraseña de Anthropic o Google.

## 12. Desarrollador y contacto
**Desarrollador: Francisco Javier Gallego Orellana**  
**Punto Vuela Montejaque**  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
Teléfono: 633 402 959  
Correo: montejaque@puntosvuela.es  
Web: https://puntosvuela.es/centros/montejaque

Proyecto independiente, no afiliado, patrocinado ni certificado por Anthropic.
