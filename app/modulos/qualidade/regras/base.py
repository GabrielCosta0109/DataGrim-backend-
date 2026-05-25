class RegraBase:
    nome = "Regra Base"

    def aplicar(self, dataframe):
        raise NotImplementedError("Implementar regra concreta")
