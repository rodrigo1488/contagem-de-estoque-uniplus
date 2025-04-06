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
            return jsonify({
                "Descricao": produto[0],
                "Quantidade": round(float(produto[1]), 2)
            })
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
