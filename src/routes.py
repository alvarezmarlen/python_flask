from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flasgger import Swagger

# Importamos desde archivo de servicios (el que adaptamos antes)
from usuarios import * 
app = Flask(__name__)

# Importamos Swagger
cors = CORS(app)

# Plantilla global de Swagger
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Usuarios",
        "description": "API para manejar usuarios",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "definitions": {
        "Usuario": {
            "type": "object",
            "required": ["nombre", "edad", "altura", "pais"],
            "properties": {
                "nombre": {"type": "string", "description": "Nombre completo del usuario"},
                "edad": {"type": "integer", "description": "Edad del usuario"},
                "altura": {"type": "number", "description": "Altura en metros"},
                "pais": {"type": "string", "description": "País de residencia"}
            },
            "example": {
                "nombre": "Luis",
                "edad": 28,
                "altura": 1.75,
                "pais": "España"
            }
        }
    }
}

swagger = Swagger(app, template=swagger_template)


# 1. Obtener todos los usuarios (Carlos, Ana, Luis...)
# Flasgger usa comentarios tipo YAML dentro de cada ruta.
@app.route("/usuarios", methods=['GET'])
def get_usuarios():
    
    """
    Obtener todos los usuarios
    ---
    responses:
      200:
        description: Lista de usuarios
        examples:
          application/json:
            [
              {"id": 1, "altura": 1.75, "edad": 25, "nombre": "Carlos", "pais": "España"},
              {"id": 2, "altura": 1.65, "edad": 30, "nombre": "Ana", "pais": "México"}
            ]
    """
    usuarios = get_all_usuarios()
    return jsonify(usuarios)

# 2. Obtener un usuario específico por su ID
# Flasgger usa comentarios tipo YAML dentro de cada ruta.
@app.route("/usuarios/<user_id>", methods=['GET'])
def get_usuario(user_id):
    
    """
    Obtener usuario por ID
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID del usuario
    responses:
      200:
        description: Usuario encontrado
        schema:
          $ref: '#/definitions/Usuario'
      404: 
          description: Usuario no encontrado
          schema: 
            type: object 
            properties: 
              error: 
                type: string 
                example: "Usuario no encontrado"
    """
    user_id = int(user_id)
    
    usuario = get_usuario_by(user_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario)

# 3. Crear un nuevo usuario
# Flasgger usa comentarios tipo YAML dentro de cada ruta.
@app.route("/usuarios", methods=["POST"])
def new_usuario():

    """
    Crear un nuevo usuario
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Usuario'
    responses:
      201:
        description: Usuario creado correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario recibido"
      400: 
        description: Error en la solicitud (datos inválidos o vacíos) 
        schema: 
          type: object 
          properties: 
            error: 
              type: string 
              example: "No hay datos para actualizar"
    """
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
# Flasgger usa comentarios tipo YAML dentro de cada ruta.
@app.route("/usuarios/<user_id>", methods=["PUT"])
def update_user_route(user_id):

    """
    Actualizar un usuario
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Usuario'
    responses:
      200:
        description: Usuario actualizado correctamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario actualizado"
      400: 
        description: Error en la solicitud (datos inválidos o vacíos) 
        schema: 
          type: object 
          properties: 
            error: 
              type: string 
              example: "No hay datos para actualizar"
      404: 
        description: Usuario no encontrado
        schema: 
          type: object 
          properties: 
            error: 
              type: string 
              example: "Usuario no encontrado"
    """
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
# Flasgger usa comentarios tipo YAML dentro de cada ruta.
@app.route("/usuarios/<user_id>", methods=['DELETE'])
def delete_usuario_route(user_id):

    """
    Eliminar usuario
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Usuario eliminado
      404: 
        description: Usuario no encontrado
        schema: 
          type: object 
          properties: 
            error: 
              type: string 
              example: "Usuario no encontrado"
    """
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
def patch_usuario_route(user_id):

    """
    Actualizar parcialmente un usuario
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              description: Nombre completo del usuario
            edad:
              type: integer
              description: Edad del usuario
            altura:
              type: number
              description: Altura en metros
            pais:
              type: string
              description: País de residencia
          example:
            nombre: "Ana"
            altura: 1.68
    responses:
      200:
        description: Usuario actualizado parcialmente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario actualizado parcialmente"
      400: 
        description: Error en la solicitud (datos inválidos o vacíos) 
        schema: 
          type: object 
          properties: 
            error: 
              type: string 
              example: "No hay datos para actualizar"
      404: 
        description: Usuario no encontrado
        schema: 
          type: object 
          properties: 
            error: 
              type: string 
              example: "Usuario no encontrado"
    """

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