from flask import Blueprint, request, jsonify
from databases import conectar_postgres  # Agora usando PostgreSQL
import psycopg2

Route_buscar_produto_bp = Blueprint('Route_buscar_produto_bp', __name__)

@Route_buscar_produto_bp.route("/produto/<codigo_barras>", methods=["GET"])
def buscar_produto(codigo_barras):
    try:
        codigo_barras = codigo_barras.strip()
        conn = conectar_postgres()
        cur = conn.cursor()

        # 1ª tentativa: busca pelo EAN
        query_ean = """
            SELECT s.nomeproduto, ROUND(s.quantidade, 2), p.codigo 
            FROM produto p
            JOIN saldoestoque s ON s.idproduto = p.id
            WHERE p.ean = %s
        """
        cur.execute(query_ean, (codigo_barras,))
        produto = cur.fetchone()

        # 2ª tentativa: busca pelo código (se não encontrou pelo EAN)
        if not produto:
            query_codigo = """
                SELECT s.nomeproduto, ROUND(s.quantidade, 2), p.codigo 
                FROM produto p
                JOIN saldoestoque s ON s.idproduto = p.id
                WHERE p.codigo = %s
            """
            cur.execute(query_codigo, (codigo_barras,))
            produto = cur.fetchone()

        conn.close()

        if produto:
            return{
                "Descricao": produto[0],
                "Quantidade":produto[1],
                "Codigo": produto[2],
                            }
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

