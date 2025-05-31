class Autor:
    def __init__(self, id=None, nome="", nacionalidade=""):
        self.id = id
        self.nome = nome
        self.nacionalidade = nacionalidade

class Livro:
    def __init__(self, id=None, titulo="", ano=0, id_autor=None, disponivel=True):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.id_autor = id_autor
        self.disponivel = disponivel

class Usuario:
    def __init__(self, id=None, nome="", email="", telefone=""):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

class Emprestimo:
    def __init__(self, id=None, id_usuario=None, id_livro=None, data_emprestimo=None, data_devolucao=None, devolvido=False):
        self.id = id
        self.id_usuario = id_usuario
        self.id_livro = id_livro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.devolvido = devolvido
