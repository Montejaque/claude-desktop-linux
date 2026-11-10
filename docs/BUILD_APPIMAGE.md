# Construcción de la AppImage

La AppImage contiene **Claude Desktop Installer**, no el binario de Claude. El instalador obtiene el DEB oficial de Anthropic cuando se ejecuta.

## Requisitos
Ubuntu 20.04 recomendado para construir con glibc compatible, Python 3.8, Tkinter, PyInstaller 6.11.1, curl y appimagetool.

\`\`\`bash
python3 -m pip install --user "pyinstaller==6.11.1"
bash scripts/build-appimage.sh
\`\`\`
Resultado: dist/Claude-Desktop-Installer-x86_64.AppImage

El workflow .github/workflows/ci.yml ejecuta pruebas y construye la AppImage en un contenedor Ubuntu 20.04 para mantener compatibilidad con glibc 2.31. El artefacto se publica en GitHub Actions.

## Probar
\`\`\`bash
chmod +x dist/Claude-Desktop-Installer-x86_64.AppImage
./dist/Claude-Desktop-Installer-x86_64.AppImage
\`\`\`
