import pandas as pd
from .base import MetricaBase


class MetricaCompletude:
    nome = "Completude"

    def calcular(self, df, resultados_regras=None):
        total_linhas = len(df)

        por_coluna = {}
        soma_percentuais = 0

        for coluna in df.columns:
            preenchidos = df[coluna].notna().sum()
            percentual = round((preenchidos / total_linhas) * 100, 2)
            por_coluna[coluna] = percentual
            soma_percentuais += percentual

        geral = round(soma_percentuais / len(df.columns), 2)

        return {
            "geral": geral,
            "por_coluna": por_coluna
        }
