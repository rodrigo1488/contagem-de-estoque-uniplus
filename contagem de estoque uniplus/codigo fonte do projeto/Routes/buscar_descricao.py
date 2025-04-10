from flask import Blueprint, request, jsonify
from databases import conectar_postgres


Buscar_descricao_bp = Blueprint('Buscar_descricao_bp', __name__)

def buscar_descricao_postgres(codigo_barras):
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
            return {
                "descricao": produto[0],
                "quantidade_sist": produto[1],
                "codigo": produto[2]
            }
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

