from .base import RegraBase
from app.modulos.qualidade.severidade.avaliador_severidade import (
    classificar_severidade
)


class RegraCamposVazios(RegraBase):
    nome = "Campos Vazios"

    def aplicar(self, df):
        total_linhas = len(df)
        resultado = {}

        for coluna in df.columns:
            vazios = df[coluna].isnull().sum()
            percentual = (vazios / total_linhas) * 100 if total_linhas > 0 else 0

            resultado[coluna] = {
                "vazios": int(vazios),
                "percentual": round(percentual, 2),
                "severidade": classificar_severidade(100 - percentual)
            }

        return resultado
