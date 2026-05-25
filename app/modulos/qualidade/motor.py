class MotorQualidade:

    def executar(self, df, regras=None, validacoes=None):
        resultados = []

        # -------------------------
        # Validações estruturais
        # -------------------------
        if validacoes:
            for validacao in validacoes:
                resultados.append({
                    "tipo": "validacao",
                    "nome": validacao.nome,
                    "resultado": validacao.validar(df)
                })

        # -------------------------
        # Regras de qualidade
        # -------------------------
        if regras:
            for regra in regras:
                resultados.append({
                    "tipo": "regra",
                    "nome": regra.nome,
                    "resultado": regra.aplicar(df)
                })

        return resultados
