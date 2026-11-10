# Construcción de la AppImage

La AppImage contiene **Claude Desktop Installer**, no el binario de Claude. El instalador obtiene el DEB oficial de Anthropic cuando se ejecuta.

## Requisitos
Ubuntu 20.04 recomendado para construir con glibc compatible, Python 3.8, Tkinter, PyInstaller 6.11.1, curl, reportlab y appimagetool.

\`\`\`bash
python3 -m pip install --user "pyinstaller==6.11.1" "reportlab==4.2.5"
bash scripts/build-appimage.sh
python3 scripts/build-help-pdf.py
\`\`\`

Resultados:
- dist/Claude-Desktop-Installer-x86_64.AppImage
- dist/Guia-Ayuda-Claude-Desktop.pdf

## Construcción automatizada
El workflow .github/workflows/ci.yml ejecuta pruebas con Python 3.8, 3.10 y 3.12 y construye la AppImage dentro de Ubuntu 20.04 para mantener compatibilidad con glibc 2.31. El artefacto AppImage y la guía PDF se publican como artefacto de GitHub Actions. Al crear una etiqueta v*, se adjuntan a la release.

## Probar
\`\`\`bash
chmod +x dist/Claude-Desktop-Installer-x86_64.AppImage
./dist/Claude-Desktop-Installer-x86_64.AppImage
\`\`\`
