from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from app.modulos.historico.servico import consultar_historico
from app.modulos.historico.servico_exportacao import exportar_analise_pdf

from app.modulos.historico.storage.rotas import router as storage_router

from app.modulos.historico.storage.rotas import router as storage_router

from fastapi import HTTPException
from app.modulos.historico.servico_exportacao import exportar_analise_pdf


router = APIRouter(prefix="/historico", tags=["Histórico"])

router.include_router(storage_router)

@router.get("/")
def listar_historico(
    arquivo: str | None = Query(default=None),
    severidade: str | None = Query(default=None),
    data_inicio: str | None = Query(default=None),
    data_fim: str | None = Query(default=None)
):
    resultados = consultar_historico(
        nome_arquivo=arquivo,
        severidade=severidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return {
        "total": len(resultados),
        "resultados": resultados
    }

@router.get("/exportar/pdf")
def exportar_pdf(
    arquivo: str | None = Query(None),
    severidade: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None)
):
    caminho_pdf = exportar_historico_pdf(
        nome_arquivo=arquivo,
        severidade=severidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return FileResponse(
        caminho_pdf,
        media_type="application/pdf",
        filename="relatorio_historico.pdf"
    )

@router.get("/analises/{analise_id}/exportar/pdf")
def exportar_pdf_analise(analise_id: int):
    try:
        caminho_pdf = exportar_analise_pdf(analise_id)
        return FileResponse(
            caminho_pdf,
            media_type="application/pdf",
            filename=f"relatorio_analise_{analise_id}.pdf"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao gerar PDF: {str(e)}")
