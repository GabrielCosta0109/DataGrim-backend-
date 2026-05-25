from .base import RegraBase
from app.modulos.qualidade.severidade.avaliador_severidade import (
    classificar_severidade
)


class RegraDuplicados(RegraBase):
    nome = "Registros Duplicados (Email)"

    def aplicar(self, df):
        total_registros = len(df)

        duplicados = df[df.duplicated(subset=["email"], keep=False)]
        total_duplicados = len(duplicados)

        percentual = (total_duplicados / total_registros) * 100 if total_registros > 0 else 0

        return {
            "total_duplicados": int(total_duplicados),
            "percentual": round(percentual, 2),
            "severidade": classificar_severidade(100 - percentual),
            "emails": duplicados["email"].dropna().unique().tolist()
        }
