import json
from datetime import datetime
from typing import Any, Dict, Optional, List

from .repositorio import AnaliseRepositorio


class AnaliseServico:
  def __init__(self, repo: Optional[AnaliseRepositorio] = None):
    self.repo = repo or AnaliseRepositorio()

  def salvar_resultado(
    self,
    *,
    nome_arquivo: str,
    content_type: Optional[str],
    conteudo_arquivo: bytes,
    resultado_analise: Dict[str, Any],
  ) -> int:
    # 1) salva o arquivo no disco
    sha, caminho, tamanho = self.repo.salvar_arquivo(nome_arquivo, conteudo_arquivo)

    # 2) extrai resumo do resultado (para lista)
    sg = (resultado_analise or {}).get("severidade_global") or {}
    percentual = float(sg.get("percentual_geral") or 0)
    severidade = str(sg.get("severidade") or "OK")
    recomendacao = str(sg.get("recomendacao") or "")

    # 3) timestamp
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4) cria registro
    analise_id = self.repo.criar_analise(
      nome_arquivo=nome_arquivo,
      content_type=content_type,
      sha256=sha,
      caminho_arquivo=caminho,
      tamanho_bytes=tamanho,
      criado_em=criado_em,
      severidade=severidade,
      percentual=percentual,
      recomendacao=recomendacao,
      resultado=resultado_analise,
    )
    return analise_id

  def listar(self, limit: int = 50, q: Optional[str] = None):
    return self.repo.listar_analises(limit=limit, q=q)

  def detalhe(self, analise_id: int):
    return self.repo.obter_analise(analise_id)

  def limpar(self) -> int:
    return self.repo.limpar_analises()
