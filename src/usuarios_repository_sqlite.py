import sqlite3
from flask import jsonify

def read_all():
    con = sqlite3.connect("usuarios.db")
    try:
        cur = con.cursor()
        res = cur.execute("SELECT ID, NOMBRE, EDAD, ALTURA, PAIS FROM LISTADEUSUARIOS")
        usuarios_sql = res.fetchall()
        lista = []
        for u in usuarios_sql:
            lista.append({"id": u[0], "nombre": u[1], "edad": u[2], "altura": u[3], "pais": u[4]})
        # Movido jsonify(lista) a @app.route("/usuarios", methods=['GET'])
        # De esta forma, la función de servicio devuelve siempre datos puros 
        # y luego decides si los mandas como JSON
        return lista
    finally:
        con.close()


def read(user_id):
    con = sqlite3.connect("usuarios.db")
    try:
        cur = con.cursor()
        res = cur.execute("SELECT ID, NOMBRE, EDAD, ALTURA, PAIS FROM LISTADEUSUARIOS WHERE ID=?", [user_id])
        u = res.fetchone()
        return {"id": u[0], "nombre": u[1], "edad": u[2], "altura": u[3], "pais": u[4]}
    finally:
        con.close()


def create(new_user):
    con = sqlite3.connect("usuarios.db")
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



def update(upd_user):
    con = sqlite3.connect("usuarios.db")
    try:
        cur = con.cursor()
        # Actualizamos por ID
        columnas = (upd_user['nombre'], upd_user['edad'], upd_user['altura'], upd_user['pais'], upd_user['id'])
        cur.execute("UPDATE LISTADEUSUARIOS SET NOMBRE=?, EDAD=?, ALTURA=?, PAIS=? WHERE ID=?", columnas)
        con.commit()
    finally:
        con.close()



def delete(user_id):
    con = sqlite3.connect("usuarios.db")
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM LISTADEUSUARIOS WHERE ID=?", [user_id])
        con.commit()
    finally:
        con.close()