from backend.db import conectar
from backend.models import Usuario

class UsuarioController:

    def inserir_usuario(usuario):
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nome, email, telefone) VALUES (%s, %s, %s)"
        val = (usuario.nome, usuario.email, usuario.telefone)
        cursor.execute(sql, val)
        conn.commit()
        usuario.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return usuario

    def listar_usuarios():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = []
        for (id, nome, email, telefone) in cursor.fetchall():
            usuario = Usuario(id, nome, email, telefone)
            usuarios.append(usuario)
        cursor.close()
        conn.close()
        return usuarios

    def buscar_usuario_por_id(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        dados = cursor.fetchone()
        usuario = Usuario(dados[0], dados[1], dados[2], dados[3]) if dados else None
        cursor.close()
        conn.close()
        return usuario

    def atualizar_usuario(usuario):
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET nome = %s, email = %s, telefone = %s WHERE id = %s"
        val = (usuario.nome, usuario.email, usuario.telefone, usuario.id)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return usuario

    def deletar_usuario(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
