"""Small GTK-free desktop diagnostic UI.

Tkinter is used because it is commonly available with Python desktop installs.
If Tk is missing, show a clear actionable error rather than silently falling back.
"""
from __future__ import annotations

import json
import tkinter as tk
from tkinter import messagebox, ttk

from .system_info import compatibility_summary


def main() -> int:
    root = tk.Tk()
    root.title("Claude Desktop Linux Installer")
    root.geometry("720x520")
    root.minsize(620, 440)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    outer = ttk.Frame(root, padding=24)
    outer.pack(fill="both", expand=True)

    ttk.Label(
        outer, text="Claude Desktop", font=("Inter", 22, "bold")
    ).pack(anchor="w")
    ttk.Label(
        outer,
        text="Instalador independiente · instalación por usuario · sin root",
    ).pack(anchor="w", pady=(4, 18))

    result = compatibility_summary()
    ok = result["compatible_with_current_official_baseline"]
    status_text = (
        "El sistema cumple la línea base técnica detectada."
        if ok else
        "Compatibilidad oficial no confirmada para este sistema."
    )
    status = ttk.Label(
        outer, text=status_text, font=("Inter", 12, "bold"),
        foreground="#26734d" if ok else "#9a5b00",
    )
    status.pack(anchor="w", pady=(0, 12))

    details = tk.Text(
        outer, wrap="word", height=14, relief="flat",
        background="#f3f3f3", padx=12, pady=12,
    )
    details.pack(fill="both", expand=True)
    details.insert("1.0", json.dumps(result, indent=2, ensure_ascii=False))
    details.configure(state="disabled")

    footer = ttk.Frame(outer)
    footer.pack(fill="x", pady=(16, 0))

    def show_reason() -> None:
        reasons = result["reasons"]
        if reasons:
            messagebox.showwarning(
                "Compatibilidad", "\n\n".join(reasons), parent=root
            )
        else:
            messagebox.showinfo(
                "Compatibilidad",
                "El diagnóstico básico no detecta bloqueos. "
                "Aún falta validar el paquete y sus dependencias reales.",
                parent=root,
            )

    ttk.Button(footer, text="Ver diagnóstico", command=show_reason).pack(side="left")
    ttk.Button(footer, text="Cerrar", command=root.destroy).pack(side="right")

    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
