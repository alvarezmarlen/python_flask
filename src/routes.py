from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flasgger import Swagger, swag_from


# Importamos desde archivo de servicios (el que adaptamos antes)
from usuarios import * 
app = Flask(__name__)

# Importamos Swagger
cors = CORS(app)

# Plantilla global de Swagger

# Flasgger crea un documento Swagger global en memoria
# @swag_from("...") Lee el archivo YAML y lo inyecta dentro del Swagger global
Swagger(app, template_file="swagger/global_template.yml")

# 1. Obtener todos los usuarios (Carlos, Ana, Luis...)
@app.route("/usuarios", methods=['GET'])
@swag_from("swagger/get_usuarios.yml")
def get_usuarios():
    
    usuarios = get_all_usuarios()
    return jsonify(usuarios)

# 2. Obtener un usuario específico por su ID
@app.route("/usuarios/<user_id>", methods=['GET'])
@swag_from("swagger/get_usuarios_id.yml")
def get_usuario(user_id):
  
    user_id = int(user_id)
    
    usuario = get_usuario_by(user_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario)

# 3. Crear un nuevo usuario
@app.route("/usuarios", methods=["POST"])
@swag_from("swagger/post_usuarios.yml")
def new_usuario():

    data = request.get_json()
    
    # 1. Body vacío
    if not data:
        return jsonify({"error": "Body vacío"}), 400

    # 2. Validar campos obligatorios
    required_fields = ["nombre", "edad", "altura", "pais"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "faltan": missing
        }), 400
    
    print('** Creando nuevo usuario:', data)
    post_usuario(data)
    return jsonify({"message": "Usuario recibido"}), 201

# 4. Actualizar un usuario existente
@app.route("/usuarios/<user_id>", methods=["PUT"])
@swag_from("swagger/put_usuarios.yml")
def update_user_route(user_id):

    data = request.get_json()

    if not data:
      return jsonify({"error": "Body vacío"}), 400

    required_fields = ["nombre", "edad", "altura", "pais"]

    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "faltan": missing
        }), 400

    actualizado = update_usuario(user_id, data)

    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return jsonify({"message": "Usuario actualizado"}), 200

# 5. Eliminar un usuario
@app.route("/usuarios/<user_id>", methods=['DELETE'])
@swag_from("swagger/delete_usuarios.yml")
def delete_usuario_route(user_id):

    print('** Eliminando usuario ID:', user_id)
    eliminado = del_usuario(user_id)

    if not eliminado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return jsonify({"message": "Usuario eliminado"}), 200

# 6. Ruta que accede a una plantilla JInga2 
@app.route("/")
def index():

    # Obtenemos todos los usuarios usando tu función del servicio
    usuarios = get_all_usuarios()  # esto devuelve una lista de dicts
    
    # Pasamos la lista a la plantilla
    return render_template("panel.html", usuarios=usuarios)

@app.route("/usuarios/<user_id>", methods=["PATCH"])
@swag_from("swagger/patch_usuarios.yml")
def patch_usuario_route(user_id):

    data = request.get_json()
    print('** PATCH usuario ID:', user_id, data)

    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400


    actualizado = patch_usuario(user_id, data)

    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"message": "Usuario actualizado parcialmente"}), 200

if __name__ == "__main__":
    app.run(debug=True)