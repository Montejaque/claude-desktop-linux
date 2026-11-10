from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"docs/GUIA_USUARIO.md"
OUT=ROOT/"dist/Guia-Ayuda-Claude-Desktop.pdf"
YELLOW=colors.HexColor("#F3D54E")
DARK=colors.HexColor("#252525")
GREY=colors.HexColor("#686868")
def xml(text):
    return text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=19*mm,leftMargin=19*mm,topMargin=22*mm,bottomMargin=20*mm,title="Guía de ayuda · Claude Desktop Installer · Versión 1.0.1",author="Francisco Javier Gallego Orellana · Punto Vuela Montejaque")
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BrandTitle",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=22,leading=27,textColor=DARK,alignment=TA_LEFT,spaceAfter=5))
    styles.add(ParagraphStyle(name="Sub",parent=styles["Normal"],fontSize=9,textColor=GREY,leading=13,spaceAfter=10))
    styles.add(ParagraphStyle(name="H2x",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=13,leading=17,textColor=DARK,spaceBefore=12,spaceAfter=6))
    styles.add(ParagraphStyle(name="Bodyx",parent=styles["BodyText"],fontName="Helvetica",fontSize=9,leading=13,textColor=DARK,spaceAfter=6))
    story=[Paragraph("CLAUDE DESKTOP",styles["BrandTitle"]),Paragraph("GUÍA DE AYUDA · INSTALADOR LINUX · PUNTO VUELA MONTEJAQUE · VERSIÓN 1.0.1",styles["Sub"]),HRFlowable(width="100%",thickness=4,color=YELLOW,spaceAfter=12)]
    in_code=False
    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if line.startswith(chr(96)*3): in_code=not in_code; continue
        if in_code or not line: continue
        if line.startswith("# "): continue
        if line.startswith("## "): story.append(Paragraph(xml(line[3:]),styles["H2x"])); continue
        if line.startswith("- "): line="•  "+line[2:]
        text=line.replace("**","").replace(chr(96),"")
        story.append(Paragraph(xml(text),styles["Bodyx"]))
    def footer(canvas,document):
        canvas.saveState(); w,h=A4
        canvas.setStrokeColor(YELLOW); canvas.setLineWidth(3); canvas.line(19*mm,14*mm,w-19*mm,14*mm)
        canvas.setFont("Helvetica",8); canvas.setFillColor(GREY)
        canvas.drawString(19*mm,9*mm,"Francisco Javier Gallego Orellana · Punto Vuela Montejaque · montejaque@puntosvuela.es")
        canvas.drawRightString(w-19*mm,9*mm,str(document.page)); canvas.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)
if __name__=="__main__": build()
