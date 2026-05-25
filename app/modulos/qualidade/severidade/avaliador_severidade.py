SEVERIDADE_BAIXA = "BAIXA"
SEVERIDADE_MEDIA = "MEDIA"
SEVERIDADE_ALTA = "ALTA"


def classificar_severidade(percentual: float) -> str:
    """
    Classifica a severidade da qualidade dos dados
    com base no percentual de completude.
    """

    if percentual >= 95:
        return SEVERIDADE_BAIXA

    if percentual >= 80:
        return SEVERIDADE_MEDIA

    return SEVERIDADE_ALTA
