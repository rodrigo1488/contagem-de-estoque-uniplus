from flask import Flask, request, jsonify, render_template, Blueprint
import psycopg2
import sqlite3
import os
import datetime

Database_bp = Blueprint('Database_bp', __name__)

# Configuração do PostgreSQL
DATABASE_CONFIG = {
    "host": "localhost",
    "database": "unico",  # <-- substitui com o nome real do banco
    "user": "postgres",
    "password": "postgres"
}

# Caminho do arquivo de contagem
diretorio = "C:/contagem_estoque"
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

CAMINHO_ARQUIVO = os.path.join(diretorio, f"contagem_estoque_{datetime.datetime.now().strftime('%d-%m-%Y %H-%M')}.txt")

# Caminho do banco local
CAMINHO_DB_LOCAL = "contagem_estoque.db"

# Criar banco e tabela, se não existirem
def inicializar_banco():
    conn = sqlite3.connect(CAMINHO_DB_LOCAL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contagem_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            codigo_barras TEXT UNIQUE,
            quantidade INTEGER,
            qnt_sist INTEGER,
            nome_user TEXT,
            data_hora timestamp
        )
    """)
    conn.commit()
    conn.close()

# Conectar ao banco PostgreSQL
def conectar_postgres():
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"]
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None
