"""Graphical per-user installer."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from .installer import InstallError, install_latest, is_installed, installed_version, launch, uninstall
from .system_info import compatibility_summary

BG = "#171717"
PANEL = "#222222"
FG = "#f4f4f4"
MUTED = "#b8b8b8"
YELLOW = "#F3D54E"


class InstallerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Claude Desktop Linux Installer")
        root.geometry("760x600")
        root.minsize(680, 540)
        root.configure(bg=BG)
        self.busy = False

        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=FG, font=("DejaVu Sans", 10))
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("Title.TLabel", background=BG, foreground=FG, font=("DejaVu Sans", 21, "bold"))
        style.configure("Status.TLabel", background=PANEL, foreground=YELLOW, font=("DejaVu Sans", 10, "bold"))
        style.configure("TButton", font=("DejaVu Sans", 10), padding=(14, 9))
        style.configure("Install.TButton", background=YELLOW, foreground="#171717")
        style.map("Install.TButton", background=[("active", "#ffe875")])

        outer = ttk.Frame(root, padding=24)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="CLAUDE DESKTOP", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Instalador Linux · instalación en tu usuario · sin permisos root",
                  style="Muted.TLabel").pack(anchor="w", pady=(4, 18))

        warning = tk.Frame(outer, bg="#3a3020", padx=14, pady=12)
        warning.pack(fill="x", pady=(0, 16))
        tk.Label(warning, text="PAQUETE COMUNITARIO NO OFICIAL", bg="#3a3020", fg=YELLOW,
                 font=("DejaVu Sans", 10, "bold")).pack(anchor="w")
        tk.Label(warning, text=("Ubuntu 20.04 no está entre los sistemas admitidos oficialmente por Anthropic. "
                                "Esta vía utiliza una compilación AppImage de terceros, sin respaldo de Anthropic."),
                 bg="#3a3020", fg=FG, justify="left", wraplength=650).pack(anchor="w", pady=(5, 0))

        self.compat = compatibility_summary()
        self.system_text = tk.StringVar(value=self._system_summary())
        panel = ttk.Frame(outer, style="Panel.TFrame", padding=14)
        panel.pack(fill="x")
        tk.Label(panel, text="ESTADO DEL SISTEMA", bg=PANEL, fg=MUTED,
                 font=("DejaVu Sans", 9, "bold")).pack(anchor="w")
        tk.Label(panel, textvariable=self.system_text, bg=PANEL, fg=FG,
                 justify="left", wraplength=670).pack(anchor="w", pady=(6, 0))

        self.status = tk.StringVar(value=self._installed_summary())
        status_panel = ttk.Frame(outer, style="Panel.TFrame", padding=14)
        status_panel.pack(fill="x", pady=14)
        ttk.Label(status_panel, textvariable=self.status, style="Status.TLabel").pack(anchor="w")

        self.progress = ttk.Progressbar(outer, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(4, 8))
        self.detail = tk.StringVar(value="La descarga se verifica mediante SHA-256 publicado en GitHub Releases.")
        ttk.Label(outer, textvariable=self.detail, style="Muted.TLabel", wraplength=690).pack(anchor="w")

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", pady=(20, 0))
        self.install_button = ttk.Button(buttons, text="Instalar / actualizar", style="Install.TButton",
                                          command=self.start_install)
        self.install_button.pack(side="left")
        self.launch_button = ttk.Button(buttons, text="Abrir Claude", command=self.open_app)
        self.launch_button.pack(side="left", padx=8)
        self.remove_button = ttk.Button(buttons, text="Desinstalar", command=self.remove_app)
        self.remove_button.pack(side="left")
        ttk.Button(buttons, text="Cerrar", command=root.destroy).pack(side="right")
        self.refresh_buttons()

    def _system_summary(self):
        s = self.compat["system"]
        return ("%s · %s · %s · glibc %s · sesión %s" %
                (s["distro_name"], s["architecture"], s["kernel"], s["glibc_version"] or "desconocida",
                 s["session_type"]))

    def _installed_summary(self):
        if is_installed():
            return "Instalado: %s · menú de aplicaciones disponible" % (installed_version() or "versión desconocida")
        return "Claude Desktop todavía no está instalado."

    def refresh_buttons(self):
        installed = is_installed()
        self.launch_button.configure(state="normal" if installed and not self.busy else "disabled")
        self.remove_button.configure(state="normal" if installed and not self.busy else "disabled")
        self.install_button.configure(state="disabled" if self.busy else "normal")

    def _set_busy(self, busy):
        self.busy = busy
        self.refresh_buttons()

    def start_install(self):
        if self.busy:
            return
        if not messagebox.askyesno(
            "Confirmar instalación",
            "Se descargará una compilación comunitaria no oficial desde GitHub. "
            "El archivo se verificará con SHA-256 y se instalará solo en tu carpeta personal. "
            "¿Deseas continuar?",
            parent=self.root,
        ):
            return
        self._set_busy(True)
        self.progress["value"] = 0
        self.detail.set("Consultando la última versión…")
        threading.Thread(target=self._install_worker, daemon=True).start()

    def _install_worker(self):
        def progress(received, total):
            percent = int(received * 100 / total) if total else 0
            self.root.after(0, lambda p=percent, r=received, t=total:
                            (self.progress.configure(value=p),
                             self.detail.set("Descargando: %.1f / %.1f MB" % (r / 1048576, t / 1048576))))
        def status(message):
            self.root.after(0, lambda m=message: self.detail.set(m))
        try:
            version = install_latest(progress=progress, status=status)
            self.root.after(0, lambda v=version: self._install_done(v))
        except Exception as exc:
            self.root.after(0, lambda e=str(exc): self._install_failed(e))

    def _install_done(self, version):
        self._set_busy(False)
        self.status.set("Instalación completada: %s" % version)
        self.detail.set("Acceso creado en el menú de aplicaciones. No se han solicitado permisos root.")
        self.refresh_buttons()
        messagebox.showinfo("Instalación completada",
                            "Claude Desktop se ha instalado para tu usuario. Busca “Claude Desktop (versión comunitaria)” en Aplicaciones.",
                            parent=self.root)

    def _install_failed(self, error):
        self._set_busy(False)
        self.detail.set("La instalación no se ha completado.")
        self.refresh_buttons()
        messagebox.showerror("No se pudo instalar", error, parent=self.root)

    def open_app(self):
        try:
            launch()
        except InstallError as exc:
            messagebox.showerror("Claude Desktop", str(exc), parent=self.root)

    def remove_app(self):
        if not messagebox.askyesno("Desinstalar", "Se eliminarán la aplicación y su acceso del menú. "
                                  "No se borrará tu configuración personal de Claude. ¿Continuar?",
                                  parent=self.root):
            return
        try:
            uninstall()
            self.status.set("Aplicación desinstalada. La configuración personal se ha conservado.")
            self.detail.set("Desinstalación completada.")
            self.refresh_buttons()
        except Exception as exc:
            messagebox.showerror("Error al desinstalar", str(exc), parent=self.root)


def main() -> int:
    root = tk.Tk()
    InstallerApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
