from backend.db import conectar
from backend.models import Autor

class AutorController:
    
    def inserir_autor(autor):
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO autores (nome, nacionalidade) VALUES (%s, %s)"
        val = (autor.nome, autor.nacionalidade)
        cursor.execute(sql, val)
        conn.commit()
        autor.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return autor

    def listar_autores():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM autores")
        autores = []
        for (id, nome, nacionalidade) in cursor.fetchall():
            autor = Autor(id, nome, nacionalidade)
            autores.append(autor)
        cursor.close()
        conn.close()
        return autores

    def buscar_autor_por_id(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM autores WHERE id = %s", (id,))
        autor = cursor.fetchone()
        if autor:
            autor = Autor(autor[0], autor[1], autor[2])
        cursor.close()
        conn.close()
        return autor

    def atualizar_autor(autor):
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE autores SET nome = %s, nacionalidade = %s WHERE id = %s"
        val = (autor.nome, autor.nacionalidade, autor.id)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return autor

    def deletar_autor(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM autores WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True