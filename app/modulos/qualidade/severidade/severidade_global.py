from app.modulos.qualidade.severidade.avaliador_severidade import classificar_severidade


def avaliar_severidade_global(percentual_geral: float) -> dict:
    severidade = classificar_severidade(percentual_geral)

    if severidade == "BAIXA":
        justificativa = (
            "A média geral de completude indica que o dataset possui alta qualidade "
            "e está adequado para análises e uso operacional."
        )
        recomendacao = "Nenhuma ação necessária."

    elif severidade == "MEDIA":
        justificativa = (
            "A média geral de completude indica que existem campos parcialmente incompletos, "
            "o que pode impactar algumas análises."
        )
        recomendacao = (
            "Recomenda-se revisar as colunas com menor completude "
            "e aplicar correções antes de análises críticas."
        )

    else:
        justificativa = (
            "A média geral de completude indica baixa qualidade dos dados, "
            "com grande volume de informações ausentes."
        )
        recomendacao = (
            "Ação imediata necessária: revisar a origem dos dados, "
            "corrigir falhas de preenchimento e reavaliar o dataset."
        )

    return {
        "percentual_geral": percentual_geral,
        "severidade": severidade,
        "justificativa": justificativa,
        "recomendacao": recomendacao
    }
