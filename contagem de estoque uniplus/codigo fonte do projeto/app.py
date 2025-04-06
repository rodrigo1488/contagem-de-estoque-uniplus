import sys
import threading
import requests
from flask import Flask, render_template, request, jsonify
import pystray
from pystray import MenuItem as item, Icon
from PIL import Image
from waitress import serve

from Routes.route_buscar_produto import Route_buscar_produto_bp
from Routes.route_salvar import Route_salvar_bp
from Routes.route_excluir import Route_excluir_bp
from Routes.route_editar import Route_editar_bp
from Routes.route_listar_contagem import Route_listar_contagem_bp
from Routes.buscar_descricao import Buscar_descricao_bp
from Routes.route_gerar_txt import Route_gerar_txt_bp
from Routes.check_healt import CheckHealth_bp
from databases import Database_bp
from databases import inicializar_banco
from databases import conectar_postgres
from databases import DATABASE_CONFIG

SUPABASE_URL = "https://warcagsmsewuvioxebur.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndhcmNhZ3Ntc2V3dXZpb3hlYnVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNzkyODIsImV4cCI6MjA1ODg1NTI4Mn0.KjArHtZ3FLDrJILLTQ8eL9mYJrgI-K35nawCpOrragY"

app = Flask(__name__)





@app.route("/")
def index():
    return render_template("index.html")
app.register_blueprint(CheckHealth_bp)
app.register_blueprint(Route_gerar_txt_bp)
app.register_blueprint(Route_buscar_produto_bp)
app.register_blueprint(Route_excluir_bp)
app.register_blueprint(Route_listar_contagem_bp)
app.register_blueprint(Buscar_descricao_bp)
app.register_blueprint(Route_editar_bp)
app.register_blueprint(Route_salvar_bp)
app.register_blueprint(Database_bp)

inicializar_banco()

# def run_flask():
#     serve(app, host="0.0.0.0", port=5000)

def run_flask():
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

def load_icon():
    return Image.open("icon.ico")  # Certifique-se de ter um arquivo 'icon.ico' no diretório

def on_exit(icon, item):
    icon.stop()
    sys.exit()

def run_tray():
    icon = Icon("ServidorFlask", load_icon(), title="Servidor Flask", menu=(
        item('Reiniciar', lambda _: run_flask()),
        item('Sair', on_exit)
    ))    
    icon.run()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    run_tray()
