import os
import logging
import pandas as pd
import sqlite3
from fastapi import UploadFile, HTTPException
from io import BytesIO

# ==================================================
# Configuração básica de log
# ==================================================
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ==================================================
# API pública do módulo
# ==================================================
def carregar_arquivo(arquivo: UploadFile) -> pd.DataFrame:
    """
    Responsabilidade:
    - Identificar o tipo do arquivo recebido
    - Carregar os dados para um DataFrame pandas
    - NÃO realizar tratamento, limpeza ou correções nos dados

    Formatos suportados:
    - CSV
    - Excel (.xls, .xlsx)
    - SQL (dump simples, compatível com SQLite)
    """

    if not arquivo or not arquivo.filename:
        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido ou não informado."
        )

    extensao = os.path.splitext(arquivo.filename)[1].lower()
    logger.info(f"Arquivo recebido: {arquivo.filename}")

    try:
        if extensao == ".csv":
            df = _carregar_csv(arquivo)

        elif extensao in [".xls", ".xlsx"]:
            df = _carregar_excel(arquivo)

        elif extensao == ".sql":
            df = _carregar_sql(arquivo)

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de arquivo não suportado: {extensao}"
            )

        if df.empty:
            raise HTTPException(
                status_code=422,
                detail="O arquivo foi carregado, porém não contém registros."
            )

        logger.info(f"Arquivo carregado com sucesso ({len(df)} registros)")
        return df

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Erro inesperado ao processar o arquivo")
        raise HTTPException(
            status_code=422,
            detail=f"Erro ao processar o arquivo: {str(e)}"
        )


# ==================================================
# Parsers internos (uso exclusivo do módulo)
# ==================================================
def _carregar_csv(arquivo: UploadFile) -> pd.DataFrame:
    """
    Carrega arquivos CSV.

    Estratégia:
    - Tenta UTF-8
    - Se falhar, tenta ISO-8859-1 (comum em arquivos brasileiros)
    """
    arquivo.file.seek(0)

    try:
        return pd.read_csv(arquivo.file)

    except UnicodeDecodeError:
        arquivo.file.seek(0)
        return pd.read_csv(arquivo.file, encoding="ISO-8859-1")


def _carregar_excel(arquivo: UploadFile) -> pd.DataFrame:
    """
    Carrega arquivos Excel (.xls, .xlsx).

    Observação:
    - Sempre carrega a primeira aba da planilha.
    """
    arquivo.file.seek(0)
    conteudo = BytesIO(arquivo.file.read())
    return pd.read_excel(conteudo)


def _carregar_sql(arquivo: UploadFile) -> pd.DataFrame:
    """
    Carrega arquivos SQL (dump simples).

    Estratégia:
    - Executa o script em um banco SQLite em memória
    - Lê a primeira tabela encontrada

    Limitações:
    - Compatível apenas com SQL padrão SQLite
    - Apenas a primeira tabela é analisada
    """

    arquivo.file.seek(0)
    sql_script = arquivo.file.read().decode("utf-8")

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    try:
        cursor.executescript(sql_script)

        tabelas = pd.read_sql(
            "SELECT name FROM sqlite_master WHERE type='table';",
            conn
        )

        if tabelas.empty:
            raise Exception("Nenhuma tabela encontrada no arquivo SQL.")

        nome_tabela = tabelas.iloc[0]["name"]
        logger.info(f"Tabela SQL carregada: {nome_tabela}")

        df = pd.read_sql(f"SELECT * FROM {nome_tabela}", conn)
        return df

    finally:
        conn.close()


# ==================================================
# Interface pública explícita do módulo
# ==================================================
__all__ = ["carregar_arquivo"]
