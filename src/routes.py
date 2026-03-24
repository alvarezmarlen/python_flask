from flask import Flask, request, jsonify
from flask_cors import CORS

# Importamos desde tu archivo de servicios (el que adaptamos antes)
from usuarios import * 
app = Flask(__name__)
cors = CORS(app)

@app.route("/") 
def hello_root():
    return '<h1>Bienvenido al sistema de Gestión de Usuarios (Bilbao)</h1>'

# 1. Obtener todos los usuarios (Carlos, Ana, Luis...)
@app.route("/usuarios", methods=['GET'])
def get_usuarios():
    return get_all_usuarios()

# 2. Obtener un usuario específico por su ID
@app.route("/usuarios/<user_id>", methods=['GET'])
def get_usuario(user_id):
    return get_usuario_by(user_id)

# 3. Crear un nuevo usuario
@app.route("/usuarios", methods=["POST"])
def new_usuario():
    data = request.get_json()
    print('** Creando nuevo usuario:', data)
    post_usuario(data)
    return jsonify({"message": "Usuario recibido"}), 201

# 4. Actualizar un usuario existente
@app.route("/usuarios/<user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    print('** Actualizando usuario ID:', user_id)
    update_usuario(data)
    return jsonify({"message": "Usuario actualizado"}), 200

# 5. Eliminar un usuario
@app.route("/usuarios/<user_id>", methods=['DELETE'])
def delete_usuario_route(user_id):
    print('** Eliminando usuario ID:', user_id)
    del_usuario(user_id)
    return jsonify({"message": "Usuario eliminado"}), 200

if __name__ == "__main__":
    app.run(debug=True)