from flask import Blueprint, jsonify, request

# Esto es Segmentación de código (Blueprint)
main_bp = Blueprint('main', __name__)

# Decorador Router para la página principal
@main_bp.route("/")
def hello_world():
    return "<p>Buenos días! Estructura mínima funcionando.</p>"

# Decorador Router para contacto
@main_bp.route("/contacto")
def contacto():
    return "<h1>Grupo D</h1><p>Bilbao, España</p>"

# Uso de jsonify (Librerías y dependencias)
@main_bp.route("/api/info")
def info_json():
    # Devolvemos un diccionario como JSON
    datos = {
        "centro educativo": "Peñascal",
        "curso": "Full Stack",
        "tecnologia": "Python Flask"
    }
    return jsonify(datos)