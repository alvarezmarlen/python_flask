from flask import jsonify, request

# Datos de ejemplo
usuarios = [
    {"id": 1, "nombre": "Juan"},
    {"id": 2, "nombre": "Ana"}
]

def registrar_rutas(app):
    @app.route('/usuarios', methods=['GET'])
    def obtener_usuarios():
        """
        Obtener lista de usuarios
        ---
        responses:
          200:
            description: Lista de usuarios
            examples:
              application/json: [{"id": 1, "nombre": "Juan"}]
        """
        return jsonify(usuarios)

    @app.route('/usuarios/<int:id>', methods=['GET'])
    def obtener_usuario(id):
        """
        Obtener usuario por ID
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID del usuario
        responses:
          200:
            description: Usuario encontrado
          404:
            description: Usuario no encontrado
        """
        usuario = next((u for u in usuarios if u["id"] == id), None)
        if usuario:
            return jsonify(usuario)
        return jsonify({"error": "Usuario no encontrado"}), 404

    @app.route('/usuarios', methods=['POST'])
    def crear_usuario():
        """
        Crear un nuevo usuario
        ---
        parameters:
          - name: usuario
            in: body
            required: true
            schema:
              type: object
              properties:
                nombre:
                  type: string
        responses:
          201:
            description: Usuario creado
        """
        data = request.json
        nuevo = {
            "id": len(usuarios) + 1,
            "nombre": data.get("nombre")
        }
        usuarios.append(nuevo)
        return jsonify(nuevo), 201