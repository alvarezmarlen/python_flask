import sqlite3
import os

# Ruta absoluta hacia la DB dentro de src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # esto apunta a src/
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")

def read_all():
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute("SELECT ID, NOMBRE, EDAD, ALTURA, PAIS FROM LISTADEUSUARIOS")
        usuarios_sql = res.fetchall()
        lista = []
        for u in usuarios_sql:
            lista.append({"id": u[0], "nombre": u[1], "edad": u[2], "altura": u[3], "pais": u[4]})
        return lista
    finally:
        con.close()                                                                                                                     


def read(user_id):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        res = cur.execute("SELECT ID, NOMBRE, EDAD, ALTURA, PAIS FROM LISTADEUSUARIOS WHERE ID=?", [user_id])

        u = res.fetchone()
        
        if not u:
            return None
        
        return {"id": u[0], "nombre": u[1], "edad": u[2], "altura": u[3], "pais": u[4]}
    finally:
        con.close()


def create(new_user):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        # No incluimos ID
        columnas = (new_user['nombre'], new_user['edad'], new_user['altura'], new_user['pais'])
        cur.execute(
            "INSERT INTO LISTADEUSUARIOS (NOMBRE, EDAD, ALTURA, PAIS) VALUES (?, ?, ?, ?)",
            columnas
        )
        con.commit()
        # Devolvemos el id que se generó automáticamente
        return cur.lastrowid
    finally:
        con.close()



def update(user_id, upd_user):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        # Actualizamos por ID
        columnas = (upd_user['nombre'], upd_user['edad'], upd_user['altura'], upd_user['pais'], user_id)
        cur.execute("UPDATE LISTADEUSUARIOS SET NOMBRE=?, EDAD=?, ALTURA=?, PAIS=? WHERE ID=?", columnas)
        con.commit()

        if cur.rowcount == 0:
            return False  # No existe el usuario
        return True
    finally:
        con.close()



def delete(user_id):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM LISTADEUSUARIOS WHERE ID=?", [user_id])
        con.commit()

        if cur.rowcount == 0:
            return False  # no existe
        return True       # eliminado
    finally:
        con.close()

def patch(user_id, fields):
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()

        # Construir query dinámica
        keys = []
        values = []
        allowed = {"nombre", "edad", "altura", "pais"}

        for key, value in fields.items():
            if key not in allowed:
                continue
            keys.append(f"{key.upper()}=?")
            values.append(value)

        values.append(user_id)

        query = f"UPDATE LISTADEUSUARIOS SET {', '.join(keys)} WHERE ID=?"
        cur.execute(query, values)
        con.commit()

        if cur.rowcount == 0:
            return False
        return True
    finally:
        con.close()