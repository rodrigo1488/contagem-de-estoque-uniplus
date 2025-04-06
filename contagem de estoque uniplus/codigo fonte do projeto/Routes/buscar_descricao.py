from flask import Blueprint
import psycopg2
from databases import conectar_postgres

Buscar_descricao_bp = Blueprint('Buscar_descricao_bp', __name__)

def buscar_descricao_postgres(codigo_barras):
    try:
        conn = conectar_postgres()
        cur = conn.cursor()

        query = """
            SELECT s.nomeproduto, ROUND(s.quantidade, 2)
            FROM produto p
            JOIN saldoestoque s ON s.idproduto = p.id
            WHERE p.ean = %s
        """

        cur.execute(query, (codigo_barras,))
        produto = cur.fetchone()
        conn.close()

        if produto:
            return {
                "descricao": produto[0],
                "quantidade_sist": round(int(produto[1]), 2)
            }
        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar descrição no PostgreSQL: {e}")
        return None
