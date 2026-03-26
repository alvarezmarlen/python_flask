from flask import Flask

def create_app():
    app = Flask(__name__)

    # importar rutas
    from .import routes

    return app