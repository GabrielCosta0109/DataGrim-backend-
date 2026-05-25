from typing import Optional, List

from app.modulos.historico.servico import consultar_historico


def consultar(
    arquivo: Optional[str] = None,
    severidade: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None
) -> List[dict]:
    """
    RF008 – Consulta e filtros do histórico

    Parâmetros (todos opcionais):
    - arquivo: nome do arquivo (com ou sem extensão)
    - severidade: BAIXA | MEDIA | ALTA
    - data_inicio: YYYY-MM-DD
    - data_fim: YYYY-MM-DD
    """

    return consultar_historico(
        nome_arquivo=arquivo,
        severidade=severidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
