from flask import Flask
import os # Librería de la guía
from src.routes import main_bp # Import de archivos (Segmentación)

# Estructura mínima
app = Flask(__name__)

# Registramos las rutas que están en el otro archivo
app.register_blueprint(main_bp)

if __name__ == "__main__":
    # Ejecución del servidor
    app.run(debug=True)