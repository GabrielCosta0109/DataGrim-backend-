from app.modulos.historico.storage.historico_analises import (
    carregar,
    salvar
)


def salvar_analise(dados: dict):
    return salvar(dados)


def buscar_analises():
    return carregar()
