from datetime import datetime

from app.modulos.ingestao.parsers import carregar_arquivo
from app.modulos.qualidade.motor import MotorQualidade
from app.modulos.qualidade.validacoes.formato import ValidacaoFormato
from app.modulos.qualidade.regras.campos_vazios import RegraCamposVazios
from app.modulos.qualidade.regras.duplicados import RegraDuplicados
from app.modulos.qualidade.metricas.completude import MetricaCompletude
from app.modulos.qualidade.severidade.avaliador_severidade import (
    classificar_severidade
)

# ✅ NOVO: persistência da análise + arquivo no SQLite
from app.modulos.historico.storage.servico import AnaliseServico


def analisar_arquivo(file):
    # ==========================================================
    # Leitura do arquivo (bytes) UMA ÚNICA VEZ
    # ==========================================================
    # ⚠️ UploadFile.file é um stream, então ler consome.
    # Por isso: lemos e voltamos o ponteiro.
    file.file.seek(0)
    conteudo_bytes = file.file.read()
    file.file.seek(0)

    # ==========================================================
    # RF001 – Ingestão
    # ==========================================================
    df = carregar_arquivo(file)

    # ==========================================================
    # RF002 – Validação de Formato
    # ==========================================================
    validacao = ValidacaoFormato(
        colunas_esperadas={
            "id": "int",
            "nome": "str",
            "email": "str",
            "idade": "int"
        }
    )

    resultado_validacao = validacao.validar(df)

    if not resultado_validacao["valido"]:
        return {
            "status": "erro_formato",
            "validacoes": [
                {
                    "nome": validacao.nome,
                    "resultado": resultado_validacao
                }
            ]
        }

    # ==========================================================
    # RF003 – Regras de Qualidade
    # ==========================================================
    regras = [
        RegraCamposVazios(),
        RegraDuplicados()
    ]

    motor = MotorQualidade()
    resultados_regras = motor.executar(df, regras=regras)

    # ==========================================================
    # RF003 – Métrica de Completude
    # ==========================================================
    metrica_completude = MetricaCompletude()
    resultado_completude = metrica_completude.calcular(df, resultados_regras)

    por_coluna = resultado_completude.get("por_coluna", {})

    # ==========================================================
    # RF004 – Severidade por Coluna
    # ==========================================================
    severidade_por_coluna = {}

    for coluna, percentual in por_coluna.items():
        severidade_por_coluna[coluna] = {
            "percentual": round(percentual, 2),
            "severidade": classificar_severidade(percentual)
        }

    # ==========================================================
    # RF005 – Severidade Global
    # ==========================================================
    if not por_coluna:
        severidade_global = {
            "percentual_geral": 0,
            "severidade": "ALTA",
            "justificativa": "Não foi possível calcular a completude das colunas.",
            "recomendacao": "Verifique o dataset e as métricas configuradas."
        }
    else:
        media_geral = sum(por_coluna.values()) / len(por_coluna)
        severidade = classificar_severidade(media_geral)

        if severidade == "BAIXA":
            justificativa = "A média geral de completude indica alta qualidade dos dados."
            recomendacao = "Nenhuma ação necessária."
        elif severidade == "MEDIA":
            justificativa = "O dataset apresenta inconsistências moderadas de preenchimento."
            recomendacao = "Recomenda-se revisar campos críticos com valores ausentes."
        else:
            justificativa = "A média geral de completude indica baixa qualidade dos dados."
            recomendacao = (
                "Ação imediata necessária: corrigir falhas de preenchimento "
                "e revisar a origem dos dados."
            )

        severidade_global = {
            "percentual_geral": round(media_geral, 2),
            "severidade": severidade,
            "justificativa": justificativa,
            "recomendacao": recomendacao
        }

    # ==========================================================
    # Monta o JSON final (o mesmo formato que seu front já espera)
    # ==========================================================
    data = {
        "status": "sucesso",
        "validacoes": [
            {
                "nome": validacao.nome,
                "resultado": resultado_validacao
            }
        ],
        "regras": resultados_regras,
        "metricas": [
            {
                "metrica": "Completude (%)",
                "resultado": resultado_completude
            }
        ],
        "severidade": severidade_por_coluna,
        "severidade_global": severidade_global,
    }

    # ==========================================================
    # RF007 – Persistir análise (SQLite + arquivo original)
    # ==========================================================
    svc = AnaliseServico()
    analise_id = svc.salvar_resultado(
        nome_arquivo=file.filename,
        content_type=getattr(file, "content_type", None),
        conteudo_arquivo=conteudo_bytes,
        resultado_analise=data,
    )

    # Timestamp para o front (pode usar o do banco também, mas aqui é simples)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================================================
    # Retorno da API
    # ==========================================================
    data["historico"] = {
        "id_analise": analise_id,
        "timestamp": timestamp
    }

    return data
