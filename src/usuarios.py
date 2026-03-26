# Importamos todas las funciones del archivo que adaptamos antes
from usuarios_repository_sqlite import * 

def get_usuario_by(id_usuario):
    # Llama a la función read() que creamos para usuarios
    return read(id_usuario)

def get_all_usuarios():
    # Llama a la función read_all() que devuelve a Carlos, Ana y Luis
    return read_all()

def post_usuario(nuevo_usuario):
    # Llama a la función create()
    print(create(nuevo_usuario))

def update_usuario(user_id, usuario_actualizado):
    # Llama a la función update()
    update(user_id, usuario_actualizado)

def del_usuario(id_usuario):
    # Llama a la función delete()
    delete(id_usuario)
