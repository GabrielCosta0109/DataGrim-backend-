import pandas as pd
from .base import ValidacaoBase


class ValidacaoFormato(ValidacaoBase):
    nome = "Validação de Formato"

    def __init__(self, colunas_esperadas: dict | None = None):
        self.colunas_esperadas = colunas_esperadas or {}

    def validar(self, df: pd.DataFrame) -> dict:
        problemas = {}

        # -------------------------
        # Estrutura básica
        # -------------------------
        problemas["dataset_vazio"] = df.empty
        problemas["total_linhas"] = int(len(df))
        problemas["total_colunas"] = int(len(df.columns))

        # -------------------------
        # Colunas inválidas
        # -------------------------
        problemas["colunas_duplicadas"] = df.columns[df.columns.duplicated()].tolist()
        problemas["colunas_nulas"] = [c for c in df.columns if not c]

        # -------------------------
        # Validação de schema
        # -------------------------
        if self.colunas_esperadas:
            colunas_df = set(df.columns)
            colunas_esperadas = set(self.colunas_esperadas.keys())

            problemas["colunas_faltantes"] = list(colunas_esperadas - colunas_df)
            problemas["colunas_extras"] = list(colunas_df - colunas_esperadas)

            tipos_invalidos = {}

            for coluna, tipo_esperado in self.colunas_esperadas.items():
                if coluna not in df.columns:
                    continue

                serie = df[coluna]

                if not self._tipo_compativel(serie, tipo_esperado):
                    tipos_invalidos[coluna] = {
                        "esperado": tipo_esperado,
                        "encontrado": str(serie.dtype)
                    }

            problemas["tipos_invalidos"] = tipos_invalidos

        # -------------------------
        # Decisão final
        # -------------------------
        formato_valido = not (
            problemas["dataset_vazio"]
            or problemas["colunas_duplicadas"]
            or problemas.get("colunas_faltantes")
            or problemas.get("tipos_invalidos")
        )

        return {
            "valido": formato_valido,
            "problemas": problemas
        }

    def _tipo_compativel(self, serie: pd.Series, tipo_esperado: str) -> bool:
        tipo_esperado = tipo_esperado.lower()

        # Remove valores nulos para análise de tipo
        serie_nao_nula = serie.dropna()

        if serie_nao_nula.empty:
            return True  # coluna vazia não invalida formato

        if tipo_esperado == "int":
            # aceita int ou float (quando float é causado por NaN)
            return pd.api.types.is_integer_dtype(serie_nao_nula) or \
                pd.api.types.is_float_dtype(serie_nao_nula)

        if tipo_esperado == "float":
            return pd.api.types.is_numeric_dtype(serie_nao_nula)

        if tipo_esperado == "str":
            # pandas usa object para string
            return pd.api.types.is_object_dtype(serie_nao_nula)

        if tipo_esperado == "date":
            return pd.api.types.is_datetime64_any_dtype(serie_nao_nula)

        return True
