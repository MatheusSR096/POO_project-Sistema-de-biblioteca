from backend.db import conectar
from backend.models import Emprestimo

class EmprestimoController:

    def inserir_emprestimo(emprestimo):
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se o livro está disponível
        cursor.execute("SELECT disponivel FROM livros WHERE id = %s", (emprestimo.id_livro,))
        status = cursor.fetchone()
        if not status or not status[0]:
            cursor.close()
            conn.close()
            return None  # Livro não disponível

        sql = """
            INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_devolucao, devolvido)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (
            emprestimo.id_usuario,
            emprestimo.id_livro,
            emprestimo.data_emprestimo,
            emprestimo.data_devolucao,
            emprestimo.devolvido
        )
        cursor.execute(sql, val)
        conn.commit()
        emprestimo.id = cursor.lastrowid

        # Atualiza status do livro
        cursor.execute("UPDATE livros SET disponivel = FALSE WHERE id = %s", (emprestimo.id_livro,))
        conn.commit()

        cursor.close()
        conn.close()
        return emprestimo

    def listar_emprestimos():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emprestimos")
        emprestimos = []
        for (id, id_usuario, id_livro, data_emprestimo, data_devolucao, devolvido) in cursor.fetchall():
            emprestimo = Emprestimo(id, id_usuario, id_livro, data_emprestimo, data_devolucao, devolvido)
            emprestimos.append(emprestimo)
        cursor.close()
        conn.close()
        return emprestimos

    def buscar_emprestimo_por_id(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emprestimos WHERE id = %s", (id,))
        dados = cursor.fetchone()
        emprestimo = Emprestimo(*dados) if dados else None
        cursor.close()
        conn.close()
        return emprestimo

    def devolver_livro(id_emprestimo, data_devolucao):
        conn = conectar()
        cursor = conn.cursor()

        # Marca empréstimo como devolvido
        cursor.execute("""
            UPDATE emprestimos 
            SET data_devolucao = %s, devolvido = TRUE
            WHERE id = %s
        """, (data_devolucao, id_emprestimo))

        # Recupera id_livro para atualizar disponibilidade
        cursor.execute("SELECT id_livro FROM emprestimos WHERE id = %s", (id_emprestimo,))
        id_livro = cursor.fetchone()[0]

        # Atualiza livro como disponível
        cursor.execute("UPDATE livros SET disponivel = TRUE WHERE id = %s", (id_livro,))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    def deletar_emprestimo(id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emprestimos WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
