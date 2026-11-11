# Construcción de AppImage y guía PDF

**Versión del proyecto: 1.0.4**

La AppImage contiene **Claude Desktop Installer**, no el binario de Claude Desktop. Al instalar, la herramienta descarga el paquete oficial desde la infraestructura de Anthropic y verifica su autenticidad e integridad.

## Requisitos de construcción
- Ubuntu 20.04 como entorno de construcción recomendado para generar un binario compatible con glibc 2.31.
- Python 3.8.
- Tkinter.
- PyInstaller 6.11.1.
- curl, file y appimagetool.
- ReportLab 4.2.5 para generar la guía PDF.

## Construcción local
```bash
python3 -m pip install --user "pyinstaller==6.11.1" "reportlab==4.2.5"
bash scripts/build-appimage.sh
python3 scripts/build-help-pdf.py
```

Resultados:
- `dist/Claude-Desktop-Installer-x86_64.AppImage`
- `dist/Guia-Ayuda-Claude-Desktop.pdf`

## Integración continua y publicación
El workflow `.github/workflows/ci.yml` ejecuta las pruebas unitarias y construye la AppImage y el PDF dentro de un contenedor Ubuntu 20.04 para mantener compatibilidad con glibc 2.31.

Al publicar una etiqueta `v*`, el workflow intenta adjuntar la AppImage y el PDF a la GitHub Release asociada. La publicación solo debe considerarse completa cuando ambos archivos aparezcan en la sección **Assets** de la release y la ejecución del workflow haya finalizado correctamente.

## Probar
```bash
chmod +x dist/Claude-Desktop-Installer-x86_64.AppImage
./dist/Claude-Desktop-Installer-x86_64.AppImage
```

## Contacto
Francisco Javier Gallego Orellana · Punto Vuela Montejaque  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
633 402 959 · montejaque@puntosvuela.es  
https://puntosvuela.es/centros/montejaque
