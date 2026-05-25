from abc import ABC, abstractmethod


class ValidacaoBase(ABC):
    nome: str = "Validação"

    @abstractmethod
    def validar(self, df):
        """
        Executa a validação estrutural.
        Retorna um dicionário com os problemas encontrados.
        """
        pass
