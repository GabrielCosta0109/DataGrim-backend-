import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from app.modulos.historico.storage.servico import AnaliseServico


EXPORT_DIR = Path("data/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)




def _wrap_text(c: canvas.Canvas, text: str, x: float, y: float, max_width: float, line_height: float):
    """
    Quebra texto em linhas para caber no max_width.
    Retorna o novo y após desenhar.
    """
    if not text:
        return y

    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", 10) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= line_height
            line = w
            if y < 20 * mm:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = 280 * mm
    if line:
        c.drawString(x, y, line)
        y -= line_height
    return y


def exportar_analise_pdf(analise_id: int) -> str:
    """
    Gera um PDF do relatório da análise específica salva no SQLite.
    Retorna o caminho do arquivo gerado.
    """
    svc = AnaliseServico()
    row = svc.detalhe(analise_id)
    if not row:
        raise ValueError("Análise não encontrada")

    resultado: Dict[str, Any] = json.loads(row["resultado_json"])

    nome_arquivo = row["nome_arquivo"]
    criado_em = row["criado_em"]
    severidade = row["severidade"]
    percentual = row["percentual"]
    recomendacao = row["recomendacao"]

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = EXPORT_DIR / f"relatorio_analise_{analise_id}_{ts}.pdf"

    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, 285 * mm, "DataGrim — Relatório de Análise")

    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, 278 * mm, f"ID da análise: {analise_id}")
    c.drawString(20 * mm, 273 * mm, f"Arquivo: {nome_arquivo}")
    c.drawString(20 * mm, 268 * mm, f"Data: {criado_em}")

    # Resumo
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, 258 * mm, "Resumo")

    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, 252 * mm, f"Severidade: {severidade}")
    c.drawString(20 * mm, 247 * mm, f"Percentual geral: {percentual}%")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, 240 * mm, "Recomendação:")
    c.setFont("Helvetica", 10)
    y = 235 * mm
    y = _wrap_text(c, str(recomendacao), 20 * mm, y, max_width=170 * mm, line_height=5 * mm)

    # Seções principais do JSON (compacto)
    c.setFont("Helvetica-Bold", 12)
    y -= 4 * mm
    c.drawString(20 * mm, y, "Detalhes (JSON resumido)")
    y -= 8 * mm

    c.setFont("Helvetica", 9)
    # Para não ficar enorme, limitamos a renderização do JSON
    json_text = json.dumps(resultado, ensure_ascii=False, indent=2)

    # Limite de caracteres por PDF (evitar PDF gigante)
    MAX_CHARS = 15000
    if len(json_text) > MAX_CHARS:
        json_text = json_text[:MAX_CHARS] + "\n...\n(Conteúdo truncado no PDF. Consulte o JSON completo pela API.)"

    # Desenha em várias linhas, com quebra de página
    for line in json_text.splitlines():
        if y < 20 * mm:
            c.showPage()
            c.setFont("Helvetica", 9)
            y = 280 * mm
        c.drawString(20 * mm, y, line[:200])  # corta linha muito longa
        y -= 4 * mm

    c.save()
    return str(out_path)
