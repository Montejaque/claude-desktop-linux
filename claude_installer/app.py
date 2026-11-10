"""Spanish graphical installer for official Anthropic Claude Desktop."""
from __future__ import annotations
import threading,tkinter as tk,webbrowser
from tkinter import messagebox,ttk
from .installer import InstallError,check_latest,install_latest,is_installed,installed_version,launch,repair_access,uninstall
from .system_info import compatibility_summary
BG="#FFFFFF"; FG="#252525"; MUTED="#686868"; PANEL="#F6F6F6"; YELLOW="#F3D54E"
DEVELOPER="José Miguel Leotte · La Central Digital"; PHONE="+34 617 92 57 68"; EMAIL="info@lacentraldigital.es"; WEB="https://lacentraldigital.es"
GUIDE="https://github.com/Montejaque/claude-desktop-linux/blob/main/docs/GUIA_USUARIO.md"
class InstallerApp:
 def __init__(self,root):
  self.root=root; root.title("Claude Desktop · Instalador Linux"); root.geometry("820x690"); root.minsize(760,640); root.configure(bg=BG)
  self.busy=False; self.compat=compatibility_summary(); style=ttk.Style(root)
  try: style.theme_use("clam")
  except tk.TclError: pass
  style.configure("TFrame",background=BG); style.configure("Panel.TFrame",background=PANEL)
  style.configure("TLabel",background=BG,foreground=FG,font=("DejaVu Sans",9)); style.configure("Muted.TLabel",background=BG,foreground=MUTED,font=("DejaVu Sans",9))
  style.configure("Status.TLabel",background=PANEL,foreground=FG,font=("DejaVu Sans",10,"bold")); style.configure("TButton",font=("DejaVu Sans",9),padding=(10,8))
  style.configure("Accent.TButton",background=YELLOW,foreground=FG,font=("DejaVu Sans",9,"bold")); style.map("Accent.TButton",background=[("active","#E3C43E")])
  style.configure("Horizontal.TProgressbar",troughcolor="#E8E8E8",background=YELLOW)
  outer=ttk.Frame(root,padding=24); outer.pack(fill="both",expand=True)
  tk.Label(outer,text="CLAUDE DESKTOP",bg=BG,fg=FG,font=("DejaVu Sans",22,"bold")).pack(anchor="w")
  tk.Label(outer,text="INSTALADOR LINUX · PAQUETE OFICIAL DE ANTHROPIC",bg=BG,fg=MUTED,font=("DejaVu Sans",9,"bold")).pack(anchor="w",pady=(4,12))
  tk.Frame(outer,bg=YELLOW,height=4).pack(fill="x",pady=(0,15))
  warning=tk.Frame(outer,bg="#FFF8D9",padx=12,pady=10); warning.pack(fill="x",pady=(0,13))
  tk.Label(warning,text="DESCARGA OFICIAL · VERIFICACIÓN CRIPTOGRÁFICA",bg="#FFF8D9",fg="#5C4A00",font=("DejaVu Sans",9,"bold")).pack(anchor="w")
  tk.Label(warning,text="Verifica la firma GPG de Anthropic y los SHA-256 del índice y del paquete. Ubuntu 20.04 tiene glibc 2.31 y no cumple el requisito declarado libc6 >= 2.34; su uso es experimental aunque se haya probado el arranque.",bg="#FFF8D9",fg=FG,justify="left",wraplength=730).pack(anchor="w",pady=(4,0))
  panel=ttk.Frame(outer,style="Panel.TFrame",padding=13); panel.pack(fill="x"); tk.Label(panel,text="ESTADO DEL EQUIPO",bg=PANEL,fg=MUTED,font=("DejaVu Sans",8,"bold")).pack(anchor="w")
  s=self.compat["system"]; summary="%s · %s · kernel %s · glibc %s · sesión %s"%(s["distro_name"],s["architecture"],s["kernel"],s["glibc_version"] or "desconocida",s["session_type"])
  tk.Label(panel,text=summary,bg=PANEL,fg=FG,wraplength=730,justify="left").pack(anchor="w",pady=(4,0))
  self.status=tk.StringVar(value=self._summary()); state=ttk.Frame(outer,style="Panel.TFrame",padding=13); state.pack(fill="x",pady=12); ttk.Label(state,textvariable=self.status,style="Status.TLabel").pack(anchor="w")
  self.progress=ttk.Progressbar(outer,mode="determinate",maximum=100); self.progress.pack(fill="x",pady=(2,7))
  self.detail=tk.StringVar(value="Preparado para consultar el repositorio oficial de Anthropic."); ttk.Label(outer,textvariable=self.detail,style="Muted.TLabel",wraplength=740).pack(anchor="w")
  actions=ttk.Frame(outer); actions.pack(fill="x",pady=(17,10))
  self.install_button=ttk.Button(actions,text="Instalar / actualizar",style="Accent.TButton",command=self.start_install); self.install_button.pack(side="left",padx=(0,5))
  ttk.Button(actions,text="Comprobar versión",command=self.start_check).pack(side="left",padx=5); ttk.Button(actions,text="Reparar acceso",command=self.repair).pack(side="left",padx=5)
  self.remove_button=ttk.Button(actions,text="Desinstalar",command=self.remove_app); self.remove_button.pack(side="left",padx=5)
  self.open_button=ttk.Button(actions,text="Abrir Claude",command=self.open_app); self.open_button.pack(side="left",padx=5)
  logframe=tk.Frame(outer,bg=PANEL,padx=10,pady=8); logframe.pack(fill="both",expand=True,pady=(4,12)); tk.Label(logframe,text="REGISTRO DE ACTIVIDAD",bg=PANEL,fg=MUTED,font=("DejaVu Sans",8,"bold")).pack(anchor="w")
  self.log=tk.Text(logframe,height=5,wrap="word",bg="#FFFFFF",fg=FG,relief="flat",font=("DejaVu Sans Mono",8),state="disabled"); self.log.pack(fill="both",expand=True,pady=(5,0))
  footer=tk.Frame(outer,bg=BG); footer.pack(fill="x"); tk.Label(footer,text="DESARROLLADO POR",bg=BG,fg=MUTED,font=("DejaVu Sans",8,"bold")).pack(anchor="w")
  tk.Label(footer,text=DEVELOPER,bg=BG,fg=FG,font=("DejaVu Sans",9,"bold")).pack(anchor="w",pady=(2,0))
  tk.Label(footer,text=PHONE+"  ·  "+EMAIL+"  ·  "+WEB,bg=BG,fg="#6A5700",font=("DejaVu Sans",8)).pack(anchor="w",pady=(2,0))
  links=tk.Frame(footer,bg=BG); links.pack(fill="x",pady=(8,0)); tk.Button(links,text="Ver guía de ayuda",command=lambda:webbrowser.open(GUIDE),relief="flat",bg=YELLOW,fg=FG,padx=12,pady=5).pack(side="left")
  ttk.Button(links,text="Cerrar",command=root.destroy).pack(side="right"); self.refresh()
 def _summary(self): return "Claude Desktop instalado · versión %s"%(installed_version() or "desconocida") if is_installed() else "Claude Desktop todavía no está instalado."
 def refresh(self):
  ok=is_installed(); self.open_button.configure(state="normal" if ok and not self.busy else "disabled"); self.remove_button.configure(state="normal" if ok and not self.busy else "disabled"); self.install_button.configure(state="disabled" if self.busy else "normal")
 def _busy(self,v): self.busy=v; self.refresh()
 def _log(self,msg):
  self.log.configure(state="normal"); self.log.insert("end",msg.rstrip()+"\n"); self.log.see("end"); self.log.configure(state="disabled")
 def _status(self,msg): self.root.after(0,lambda m=msg:(self.detail.set(m),self._log(m)))
 def _progress(self,r,t): self.root.after(0,lambda:self.progress.configure(value=int(r*100/t) if t else 0))
 def start_install(self):
  if self.busy:return
  s=self.compat["system"]
  if s["glibc_supported_for_official_linux_build"] is False:
   ok=messagebox.askyesno("Sistema fuera de soporte","Este equipo utiliza glibc %s. El paquete declara glibc >= 2.34. La instalación es local y no modificará bibliotecas del sistema, pero no se garantiza el funcionamiento. ¿Continuar bajo tu responsabilidad?"%s["glibc_version"],parent=self.root)
  else: ok=messagebox.askyesno("Confirmar instalación","Se descargará Claude Desktop del repositorio oficial y se verificarán firma GPG y hashes. ¿Continuar?",parent=self.root)
  if not ok:return
  self._busy(True); self.progress["value"]=0; threading.Thread(target=self._install,daemon=True).start()
 def _install(self):
  try:
   v=install_latest(progress=self._progress,status=self._status); self.root.after(0,lambda:self._done("Instalación completada: "+v))
  except Exception as exc:self.root.after(0,lambda e=str(exc):self._failed(e))
 def _done(self,msg):
  self._busy(False); self.status.set(self._summary()); self.detail.set(msg); self._log(msg); self.refresh(); messagebox.showinfo("Claude Desktop",msg+"\n\nAcceso GNOME y protocolo claude:// configurados.",parent=self.root)
 def _failed(self,e):
  self._busy(False); self.detail.set("La operación no se ha completado."); self._log("ERROR: "+e); self.refresh(); messagebox.showerror("Claude Desktop",e,parent=self.root)
 def start_check(self):
  if self.busy:return
  self._busy(True); self.detail.set("Consultando versión oficial…"); threading.Thread(target=self._check,daemon=True).start()
 def _check(self):
  try:
   p=check_latest(status=self._status); msg="Versión oficial disponible: %s\nVersión instalada: %s"%(p.version,installed_version() or "no instalada"); self.root.after(0,lambda:self._check_done(msg))
  except Exception as exc:self.root.after(0,lambda e=str(exc):self._failed(e))
 def _check_done(self,msg):
  self._busy(False); self.detail.set("Comprobación terminada."); self._log(msg.replace("\n"," · ")); self.refresh(); messagebox.showinfo("Comprobar versión",msg,parent=self.root)
 def repair(self):
  try: repair_access(); self.detail.set("Acceso GNOME y protocolo claude:// reparados."); self._log("Acceso y protocolo reparados."); messagebox.showinfo("Reparación","Se ha reparado el lanzador y el protocolo claude://.",parent=self.root)
  except Exception as exc:messagebox.showerror("Reparar acceso",str(exc),parent=self.root)
 def open_app(self):
  try:launch()
  except InstallError as exc:messagebox.showerror("Claude Desktop",str(exc),parent=self.root)
 def remove_app(self):
  if not messagebox.askyesno("Desinstalar","Se eliminarán la aplicación, el lanzador y el icono. Se conservarán los datos personales de Claude. ¿Continuar?",parent=self.root):return
  try: uninstall(); self.status.set(self._summary()); self.detail.set("Claude Desktop desinstalado. Datos personales conservados."); self.refresh()
  except Exception as exc:messagebox.showerror("Desinstalar",str(exc),parent=self.root)
def main():
 root=tk.Tk(); InstallerApp(root); root.mainloop(); return 0
if __name__=="__main__":raise SystemExit(main())
