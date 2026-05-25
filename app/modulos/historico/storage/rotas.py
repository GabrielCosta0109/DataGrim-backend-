import json
from fastapi import APIRouter, HTTPException, Query

from .servico import AnaliseServico
from .schema import AnaliseResumoOut, AnaliseDetalheOut

# ✅ SEM prefix aqui!
# Porque quem define /historico é o router "pai" em app/modulos/historico/rotas.py
router = APIRouter(tags=["Histórico"])

svc = AnaliseServico()


@router.get("/analises", response_model=list[AnaliseResumoOut])
def listar_analises(
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    rows = svc.listar(limit=limit, q=q)
    return [
        {
            "id": int(r["id"]),
            "nomeArquivo": r["nome_arquivo"],
            "timestamp": r["criado_em"],
            "percentual": float(r["percentual"]),
            "severidade": r["severidade"],
        }
        for r in rows
    ]


@router.get("/analises/{analise_id}", response_model=AnaliseDetalheOut)
def obter_analise(analise_id: int):
    r = svc.detalhe(analise_id)
    if not r:
        raise HTTPException(status_code=404, detail="Análise não encontrada")

    resultado = json.loads(r["resultado_json"])

    return {
        "id": int(r["id"]),
        "nomeArquivo": r["nome_arquivo"],
        "timestamp": r["criado_em"],
        "caminhoArquivo": r["caminho_arquivo"],
        "sha256": r["sha256"],
        "contentType": r["content_type"],
        "tamanhoBytes": int(r["tamanho_bytes"]),
        "percentual": float(r["percentual"]),
        "severidade": r["severidade"],
        "recomendacao": r["recomendacao"],
        "resultado": resultado,
    }


@router.delete("/analises")
def limpar_analises():
    apagadas = svc.limpar()
    return {"status": "ok", "apagadas": apagadas}
