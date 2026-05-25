import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


class AnaliseRepositorio:
  def __init__(self, db_path: str = "data/datagrim.db", upload_dir: str = "data/uploads"):
    self.db_path = Path(db_path)
    self.upload_dir = Path(upload_dir)

    self.db_path.parent.mkdir(parents=True, exist_ok=True)
    self.upload_dir.mkdir(parents=True, exist_ok=True)

    self._init_db()

  def _conn(self):
    conn = sqlite3.connect(str(self.db_path))
    conn.row_factory = sqlite3.Row
    return conn

  def _init_db(self):
    with self._conn() as conn:
      conn.execute("""
      CREATE TABLE IF NOT EXISTS analises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_arquivo TEXT NOT NULL,
        content_type TEXT,
        tamanho_bytes INTEGER NOT NULL,
        sha256 TEXT NOT NULL,
        caminho_arquivo TEXT NOT NULL,
        criado_em TEXT NOT NULL,

        severidade TEXT NOT NULL,
        percentual REAL NOT NULL,
        recomendacao TEXT NOT NULL,

        resultado_json TEXT NOT NULL
      );
      """)
      conn.execute("CREATE INDEX IF NOT EXISTS idx_analises_criado_em ON analises(criado_em);")
      conn.execute("CREATE INDEX IF NOT EXISTS idx_analises_sha256 ON analises(sha256);")

  def _sha256_bytes(self, b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

  def salvar_arquivo(self, nome_arquivo: str, conteudo: bytes) -> Tuple[str, str, int]:
    """
    Retorna (sha256, caminho_arquivo, tamanho_bytes)
    """
    sha = self._sha256_bytes(conteudo)
    tamanho = len(conteudo)

    # nome seguro + hash no nome evita colisão
    safe_name = "".join(c for c in nome_arquivo if c.isalnum() or c in "._- ").strip()
    if not safe_name:
      safe_name = "arquivo"

    destino = self.upload_dir / f"{sha}_{safe_name}"
    destino.write_bytes(conteudo)

    return sha, str(destino), tamanho

  def criar_analise(
    self,
    *,
    nome_arquivo: str,
    content_type: Optional[str],
    sha256: str,
    caminho_arquivo: str,
    tamanho_bytes: int,
    criado_em: str,
    severidade: str,
    percentual: float,
    recomendacao: str,
    resultado: Dict[str, Any],
  ) -> int:
    resultado_json = json.dumps(resultado, ensure_ascii=False)

    with self._conn() as conn:
      cur = conn.execute("""
        INSERT INTO analises (
          nome_arquivo, content_type, tamanho_bytes, sha256, caminho_arquivo, criado_em,
          severidade, percentual, recomendacao, resultado_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, (
        nome_arquivo, content_type, tamanho_bytes, sha256, caminho_arquivo, criado_em,
        severidade, float(percentual), recomendacao, resultado_json
      ))
      return int(cur.lastrowid)

  def listar_analises(self, limit: int = 50, q: Optional[str] = None) -> List[sqlite3.Row]:
    sql = """
      SELECT id, nome_arquivo, criado_em, percentual, severidade
      FROM analises
    """
    params: List[Any] = []

    if q:
      sql += " WHERE nome_arquivo LIKE ? OR criado_em LIKE ? "
      like = f"%{q}%"
      params.extend([like, like])

    sql += " ORDER BY datetime(criado_em) DESC LIMIT ?"
    params.append(int(limit))

    with self._conn() as conn:
      rows = conn.execute(sql, params).fetchall()
      return rows

  def obter_analise(self, analise_id: int) -> Optional[sqlite3.Row]:
    with self._conn() as conn:
      row = conn.execute("""
        SELECT * FROM analises WHERE id = ?
      """, (int(analise_id),)).fetchone()
      return row

  def limpar_analises(self) -> int:
    """
    Apaga registros do banco (não apaga arquivos do disco por segurança).
    Retorna quantidade apagada.
    """
    with self._conn() as conn:
      cur = conn.execute("DELETE FROM analises")
      return cur.rowcount
