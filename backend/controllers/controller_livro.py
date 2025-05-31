from backend.db import conectar
from backend.models import Livro

class LivroController:
     
    def inserir_livro(livro):
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO livros (titulo, ano_publicacao, id_autor, disponivel) VALUES (%s, %s, %s, %s)"
        val = (livro.titulo, livro.ano, livro.id_autor, livro.disponivel)
        cursor.execute(sql, val)
        conn.commit()
        livro.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return livro

    def listar_livros():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        livros = []
        for (id, titulo, ano_publicacao, id_autor, disponivel) in cursor.fetchall():
            livro = Livro(id, titulo, ano_publicacao, id_autor, disponivel)
            livros.append(livro)
        cursor.close()
        conn.close()
        return livros

    def buscar_livro_por_id(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = %s", (id,))
        livro_data = cursor.fetchone()
        livro = None
        if livro_data:
            livro = Livro(*livro_data)
        cursor.close()
        conn.close()
        return livro

    def atualizar_livro(livro):
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE livros SET titulo = %s, id_autor = %s, ano_publicacao = %s, disponivel = %s WHERE id = %s"
        val = (livro.titulo, livro.id_autor, livro.ano, livro.disponivel, livro.id)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return livro

    def deletar_livro(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def buscar_livro_por_autor(id_autor):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM livros WHERE id_autor = %s"
        cursor.execute(sql, (id_autor,))
        livros = []
        for (id, titulo, id_autor, ano_publicacao, disponivel) in cursor.fetchall():
            livro = Livro(id, titulo, ano_publicacao, id_autor, disponivel)
            livros.append(livro)
        cursor.close()
        conn.close()
        return livros

    def buscar_livro_por_titulo(titulo):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM livros WHERE titulo LIKE %s"
        val = ("%" + titulo + "%",)
        cursor.execute(sql, val)
        livros = []
        for (id, titulo, id_autor, ano_publicacao, disponivel) in cursor.fetchall():
            livro = Livro(id, titulo, ano_publicacao, id_autor, disponivel)
            livros.append(livro)
        cursor.close()
        conn.close()
        return livros

    def buscar_livro_disponivel():
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM livros WHERE disponivel = 1"
        cursor.execute(sql)
        livros = []
        for (id, titulo, id_autor, ano_publicacao, disponivel) in cursor.fetchall():
            livro = Livro(id, titulo, ano_publicacao, id_autor, disponivel)
            livros.append(livro)
        cursor.close()
        conn.close()
        return livros

    def buscar_livro_indisponivel():
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM livros WHERE disponivel = 0"
        cursor.execute(sql)
        livros = []
        for (id, titulo, id_autor, ano_publicacao, disponivel) in cursor.fetchall():
            livro = Livro(id, titulo, ano_publicacao, id_autor, disponivel)
            livros.append(livro)
        cursor.close()
        conn.close()
        return livros

    def buscar_livro_por_ano(ano):
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM livros WHERE ano_publicacao = %s"
        cursor.execute(sql, (ano,))
        livros = []
        for (id, titulo, id_autor, ano_publicacao, disponivel) in cursor.fetchall():
            livro = Livro(id, titulo, ano_publicacao, id_autor, disponivel)
            livros.append(livro)
        cursor.close()
        conn.close()
        return livros