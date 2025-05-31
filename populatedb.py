import datetime
from backend.models import Autor, Usuario, Livro, Emprestimo
from backend.controllers.controller_autor import AutorController
from backend.controllers.controller_usuario import UsuarioController
from backend.controllers.controller_livro import LivroController
from backend.controllers.controller_emprestimo import EmprestimoController

def popular_autores():
    """Popula o banco com autores de exemplo"""
    autores = [
        Autor(None, "Machado de Assis", "Brasil"),
        Autor(None, "José Saramago", "Portugal"),
        Autor(None, "Gabriel García Márquez", "Colômbia"),
        Autor(None, "J.K. Rowling", "Reino Unido"),
        Autor(None, "George Orwell", "Reino Unido"),
        Autor(None, "Clarice Lispector", "Brasil"),
        Autor(None, "Jorge Amado", "Brasil"),
        Autor(None, "Jane Austen", "Reino Unido"),
        Autor(None, "Franz Kafka", "República Tcheca"),
        Autor(None, "Fiódor Dostoiévski", "Rússia")
    ]
    
    print("Adicionando autores...")
    autores_ids = []
    for autor in autores:
        autor_id = AutorController.inserir_autor(autor)
        autores_ids.append(autor_id)
        print(f"Autor adicionado: {autor.nome} - ID: {autor_id}")
    
    return autores_ids

def popular_livros(autores_ids):
    """Popula o banco com livros de exemplo"""
    
    livros = [
        Livro(None, "Dom Casmurro", 1899, autores_ids[0].id),
        Livro(None, "Memórias Póstumas de Brás Cubas", 1881, autores_ids[0].id),
        Livro(None, "Ensaio sobre a Cegueira", 1995, autores_ids[1].id),
        Livro(None, "Cem Anos de Solidão", 1967, autores_ids[2].id),
        Livro(None, "Harry Potter e a Pedra Filosofal", 1997, autores_ids[3].id),
        Livro(None, "1984", 1949, autores_ids[4].id),
        Livro(None, "A Revolução dos Bichos", 1945, autores_ids[4].id),
        Livro(None, "A Hora da Estrela", 1977, autores_ids[5].id),
        Livro(None, "Gabriela, Cravo e Canela", 1958, autores_ids[6].id),
        Livro(None, "Orgulho e Preconceito", 1813, autores_ids[7].id),
        Livro(None, "A Metamorfose", 1915, autores_ids[8].id),
        Livro(None, "Crime e Castigo", 1866, autores_ids[9].id),
        Livro(None, "O Processo", 1925, autores_ids[8].id),
        Livro(None, "Os Irmãos Karamazov", 1880, autores_ids[9].id),
        Livro(None, "Harry Potter e a Câmara Secreta", 1998, autores_ids[3].id)
    ]

    
    print("\nAdicionando livros...")
    livros_ids = []
    for livro in livros:
        livro_id = LivroController.inserir_livro(livro)
        livros_ids.append(livro_id)
        print(f"Livro adicionado: {livro.titulo} - ID: {livro_id}")
    
    return livros_ids

def popular_usuarios():
    """Popula o banco com usuários de exemplo"""
    usuarios = [
        Usuario(None, "João Silva", "joao.silva@email.com", "(11) 98765-4321"),
        Usuario(None, "Maria Oliveira", "maria.oliveira@email.com", "(21) 91234-5678"),
        Usuario(None, "Carlos Santos", "carlos.santos@email.com", "(31) 92345-6789"),
        Usuario(None, "Ana Costa", "ana.costa@email.com", "(41) 93456-7890"),
        Usuario(None, "Pedro Souza", "pedro.souza@email.com", "(51) 94567-8901"),
        Usuario(None, "Lucia Ferreira", "lucia.ferreira@email.com", "(61) 95678-9012"),
        Usuario(None, "Rafael Almeida", "rafael.almeida@email.com", "(71) 96789-0123"),
        Usuario(None, "Fernanda Lima", "fernanda.lima@email.com", "(81) 97890-1234")
    ]
    
    print("\nAdicionando usuários...")
    usuarios_ids = []
    for usuario in usuarios:
        usuario_id = UsuarioController.inserir_usuario(usuario)
        usuarios_ids.append(usuario_id)
        print(f"Usuário adicionado: {usuario.nome} - ID: {usuario_id}")
    
    return usuarios_ids

def criar_emprestimos(usuarios_ids, livros_ids):
    """Cria alguns empréstimos de exemplo"""
    hoje = datetime.date.today()
    
    # Define data de devolução para 15 dias após hoje
    data_devolucao = hoje + datetime.timedelta(days=15)
    
    # Cria 5 empréstimos de exemplo
    emprestimos = [
        # usuário_id, livro_id, data_emprestimo, data_devolução, devolvido
        Emprestimo(None, usuarios_ids[0].id, livros_ids[0].id, hoje, data_devolucao, False),
        Emprestimo(None, usuarios_ids[1].id, livros_ids[3].id, hoje, data_devolucao, False),
        Emprestimo(None, usuarios_ids[2].id, livros_ids[5].id, hoje, data_devolucao, False),
        Emprestimo(None, usuarios_ids[3].id, livros_ids[8].id, hoje, data_devolucao, False),
        Emprestimo(None, usuarios_ids[4].id, livros_ids[10].id, hoje, data_devolucao, False)
    ]
    
    print("\nCriando empréstimos...")
    for emprestimo in emprestimos:
        resultado = EmprestimoController.inserir_emprestimo(emprestimo)
        if resultado:
            print(f"Empréstimo criado: Usuário ID {emprestimo.id_usuario} emprestou o Livro ID {emprestimo.id_livro}")
        else:
            print(f"FALHA ao criar empréstimo: Usuário ID {emprestimo.id_usuario}, Livro ID {emprestimo.id_livro}")

def main():
    print("=== Iniciando população do banco de dados ===")
    
    # Verifica se já existem dados no banco
    autores_existentes = AutorController.listar_autores()
    if autores_existentes:
        confirm = input("AVISO: Já existem dados no banco. Deseja continuar? (s/n): ")
        if confirm.lower() != 's':
            print("Operação cancelada.")
            return
    
    # Popula as tabelas
    autores_ids = popular_autores()
    livros_ids = popular_livros(autores_ids)
    usuarios_ids = popular_usuarios()
    criar_emprestimos(usuarios_ids, livros_ids)
    
    print("\n=== População do banco de dados concluída com sucesso! ===")
    print(f"Total de autores: {len(autores_ids)}")
    print(f"Total de livros: {len(livros_ids)}")
    print(f"Total de usuários: {len(usuarios_ids)}")
    
if __name__ == "__main__":
    main()