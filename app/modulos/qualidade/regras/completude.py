from .base import RegraBase

class RegraCompletude(RegraBase):
    nome = "Completude dos Dados"

    def aplicar(self, df):
        total_linhas = len(df)
        resultados = {}

        for coluna in df.columns:
            preenchidos = df[coluna].notna().sum()
            percentual = (preenchidos / total_linhas) * 100

            resultados[coluna] = {
                "preenchidos": int(preenchidos),
                "percentual": round(percentual, 2)
            }

        return resultados
