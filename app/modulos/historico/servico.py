from typing import Optional, List
from pathlib import Path

from app.modulos.historico.repositorio import (
    salvar_analise,
    buscar_analises
)


def registrar_historico(
    nome_arquivo: str,
    df,
    severidade_global: dict,
    detalhes: dict
):
    dados = {
        "nome_arquivo": nome_arquivo,
        "linhas": len(df),
        "colunas": len(df.columns),
        "percentual_geral": severidade_global["percentual_geral"],
        "severidade_global": severidade_global["severidade"],
        "justificativa": severidade_global["justificativa"],
        "recomendacao": severidade_global["recomendacao"],
        "detalhes": detalhes
    }

    return salvar_analise(dados)


def consultar_historico(
    nome_arquivo: Optional[str] = None,
    severidade: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None
) -> List[dict]:

    historico = buscar_analises()
    resultados = []

    nome_busca = None
    if nome_arquivo:
        nome_busca = Path(nome_arquivo).stem.lower()

    for registro in historico:
        if nome_busca:
            nome_registro = Path(registro["nome_arquivo"]).stem.lower()
            if nome_registro != nome_busca:
                continue

        if severidade and registro["severidade_global"] != severidade:
            continue

        if data_inicio and registro["data_analise"] < data_inicio:
            continue

        if data_fim and registro["data_analise"] > data_fim:
            continue

        resultados.append(registro)

    return resultados
