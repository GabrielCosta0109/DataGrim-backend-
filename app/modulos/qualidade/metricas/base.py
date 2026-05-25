from abc import ABC, abstractmethod
import pandas as pd


class MetricaBase(ABC):
    nome: str = "Métrica"

    @abstractmethod
    def calcular(self, df: pd.DataFrame, resultados_regras: list) -> dict:
        pass
