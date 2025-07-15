# app.py
import os
from flask import Flask
from db import close_db, init_db

def create_app():
    app = Flask(
        __name__,
        static_folder="static",    # pasta onde estão index.html, style.css, script.js
        static_url_path=""         # monta tudo em http://host/<arquivo> em vez de /static/<arquivo>
    )
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "cvs.db"),
    )

    # Garante que exista a pasta instance/ para o banco
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa o schema do banco (cria tabelas se ainda não existirem)
    with app.app_context():
        init_db()

    # Fecha a conexão com o DB ao fim de cada request
    app.teardown_appcontext(close_db)

    # Registra as rotas da API
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Rota raiz: serve o index.html do front-end
    @app.route("/")
    def home():
        return app.send_static_file("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
