from flask import Flask, render_template
from flasgger import Swagger
from src.api_swagger import registrar_rutas  # tu API

app = Flask(__name__)
swagger = Swagger(app)

# Registrar rutas de la API
registrar_rutas(app)

# Ejemplo de datos para la plantilla
usuarios = [
    {"id": 1, "nombre": "Juan"},
    {"id": 2, "nombre": "Ana"}
]

# Ruta que renderiza la plantilla Jinja2
@app.route('/')
def index():
    return render_template('index.html', usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)