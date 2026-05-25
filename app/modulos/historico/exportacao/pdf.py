from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from datetime import datetime
import tempfile


def gerar_pdf_historico(registros: list[dict]) -> str:
    """
    Gera um PDF com o histórico de análises
    Retorna o caminho do arquivo PDF gerado
    """

    arquivo_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(
        arquivo_temp.name,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    estilos = getSampleStyleSheet()
    elementos = []

    # Título
    elementos.append(
        Paragraph("Relatório de Histórico de Análises", estilos["Title"])
    )
    elementos.append(Spacer(1, 12))

    # Data
    elementos.append(
        Paragraph(
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"]
        )
    )
    elementos.append(Spacer(1, 20))

    if not registros:
        elementos.append(
            Paragraph("Nenhum registro encontrado.", estilos["Normal"])
        )
    else:
        dados = [
            [
                "Arquivo",
                "Linhas",
                "Colunas",
                "Severidade",
                "Percentual",
                "Data"
            ]
        ]

        for r in registros:
            dados.append([
                r.get("nome_arquivo"),
                r.get("linhas"),
                r.get("colunas"),
                r.get("severidade_global"),
                f'{r.get("percentual_geral")}%',
                r.get("data_analise")
            ])

        tabela = Table(dados, repeatRows=1)
        elementos.append(tabela)

    doc.build(elementos)
    return arquivo_temp.name
