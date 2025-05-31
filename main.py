from backend.controllers.controller_livro import LivroController
from backend.controllers.controller_autor import AutorController
from backend.controllers.controller_usuario import UsuarioController
from backend.controllers.controller_emprestimo import EmprestimoController
from backend.models import Autor, Livro, Usuario, Emprestimo
from datetime import datetime

def menu():
    print('\n==== Menu Principal ====\n')
    print("1 - Gerenciar Livros")
    print("2 - Gerenciar Autores")
    print("3 - Gerenciar Usuários")
    print("4 - Gerenciar Empréstimos")
    print("0 - Sair")

def menu_livros():
    while True:
        print("\n--- Menu Livros ---")
        print("1. Inserir livro")
        print("2. Listar livros")
        print("3. Atualizar livro")
        print("4. Deletar livro")
        print("5. Buscar por autor")
        print("6. Buscar por título")
        print("7. Buscar por ano")
        print("8. Listar livros disponíveis")
        print("9. Listar livros indisponíveis")
        print("0. Voltar")
        opcao = input("Escolha: ")

        match opcao:
            case '0':
                break
            case '1':
                try:
                    titulo = input("Título: ")
                    ano = int(input("Ano: "))
                    id_autor = int(input("ID do Autor: "))
                    disponivel = input("Disponível (s/n): ").lower() == 's'
                    
                    livro = Livro(None, titulo, ano, id_autor, disponivel)
                    resultado = LivroController.inserir_livro(livro)
                    print(f"Livro inserido com ID: {resultado.id}")
                except ValueError:
                    print("Erro: Valores inválidos inseridos!")
                except Exception as e:
                    print(f"Erro ao inserir livro: {e}")
                    
            case '2':
                try:
                    livros = LivroController.listar_livros()
                    if livros:
                        print("\n--- Lista de Livros ---")
                        for l in livros:
                            status = "Sim" if l.disponivel else "Não"
                            print(f"ID: {l.id}, Título: {l.titulo}, Ano: {l.ano}, Autor ID: {l.id_autor}, Disponível: {status}")
                    else:
                        print("Nenhum livro encontrado.")
                except Exception as e:
                    print(f"Erro ao listar livros: {e}")
                    
            case '3':
                try:
                    id_livro = int(input("ID do livro: "))
                    livro_existente = LivroController.buscar_livro_por_id(id_livro)
                    
                    if livro_existente:
                        print(f"Livro atual: {livro_existente.titulo}")
                        novo_titulo = input("Novo título: ")
                        novo_ano = int(input("Novo ano: "))
                        novo_id_autor = int(input("Novo ID do Autor: "))
                        novo_disponivel = input("Disponível (s/n): ").lower() == 's'
                        
                        livro_atualizado = Livro(id_livro, novo_titulo, novo_ano, novo_id_autor, novo_disponivel)
                        LivroController.atualizar_livro(livro_atualizado)
                        print("Livro atualizado com sucesso!")
                    else:
                        print("Livro não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao atualizar livro: {e}")
                    
            case '4':
                try:
                    id_livro = int(input("ID do livro a remover: "))
                    livro_existente = LivroController.buscar_livro_por_id(id_livro)
                    
                    if livro_existente:
                        confirmacao = input(f"Tem certeza que deseja remover '{livro_existente.titulo}'? (s/n): ")
                        if confirmacao.lower() == 's':
                            LivroController.deletar_livro(id_livro)
                            print("Livro removido com sucesso!")
                    else:
                        print("Livro não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao remover livro: {e}")
                    
            case '5':
                try:
                    id_autor = int(input("ID do autor: "))
                    livros = LivroController.buscar_livro_por_autor(id_autor)
                    if livros:
                        print(f"\n--- Livros do Autor ID {id_autor} ---")
                        for l in livros:
                            status = "Sim" if l.disponivel else "Não"
                            print(f"ID: {l.id}, Título: {l.titulo}, Ano: {l.ano}, Disponível: {status}")
                    else:
                        print("Nenhum livro encontrado para este autor.")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro na busca: {e}")
                    
            case '6':
                try:
                    titulo = input("Título (ou parte do título): ")
                    livros = LivroController.buscar_livro_por_titulo(titulo)
                    if livros:
                        print(f"\n--- Livros com título '{titulo}' ---")
                        for l in livros:
                            status = "Sim" if l.disponivel else "Não"
                            print(f"ID: {l.id}, Título: {l.titulo}, Ano: {l.ano}, Autor ID: {l.id_autor}, Disponível: {status}")
                    else:
                        print("Nenhum livro encontrado.")
                except Exception as e:
                    print(f"Erro na busca: {e}")
                    
            case '7':
                try:
                    ano = int(input("Ano: "))
                    livros = LivroController.buscar_livro_por_ano(ano)
                    if livros:
                        print(f"\n--- Livros do ano {ano} ---")
                        for l in livros:
                            status = "Sim" if l.disponivel else "Não"
                            print(f"ID: {l.id}, Título: {l.titulo}, Autor ID: {l.id_autor}, Disponível: {status}")
                    else:
                        print("Nenhum livro encontrado para este ano.")
                except ValueError:
                    print("Erro: Ano inválido!")
                except Exception as e:
                    print(f"Erro na busca: {e}")
                    
            case '8':
                try:
                    livros = LivroController.buscar_livro_disponivel()
                    if livros:
                        print("\n--- Livros Disponíveis ---")
                        for l in livros:
                            print(f"ID: {l.id}, Título: {l.titulo}, Ano: {l.ano}, Autor ID: {l.id_autor}")
                    else:
                        print("Nenhum livro disponível.")
                except Exception as e:
                    print(f"Erro na busca: {e}")
                    
            case '9':
                try:
                    livros = LivroController.buscar_livro_indisponivel()
                    if livros:
                        print("\n--- Livros Indisponíveis ---")
                        for l in livros:
                            print(f"ID: {l.id}, Título: {l.titulo}, Ano: {l.ano}, Autor ID: {l.id_autor}")
                    else:
                        print("Todos os livros estão disponíveis.")
                except Exception as e:
                    print(f"Erro na busca: {e}")
                    
            case _:
                print("Opção inválida!")

def menu_autores():
    while True:
        print("\n--- Menu Autores ---")
        print("1. Inserir autor")
        print("2. Listar autores")
        print("3. Atualizar autor")
        print("4. Deletar autor")
        print("0. Voltar")
        opcao = input("Escolha: ")

        match opcao:
            case '0':
                break
            case '1':
                try:
                    nome = input("Nome do autor: ")
                    nacionalidade = input("Nacionalidade: ")
                    
                    autor = Autor(None, nome, nacionalidade)
                    resultado = AutorController.inserir_autor(autor)
                    print(f"Autor inserido com ID: {resultado.id}")
                except Exception as e:
                    print(f"Erro ao inserir autor: {e}")
                    
            case '2':
                try:
                    autores = AutorController.listar_autores()
                    if autores:
                        print("\n--- Lista de Autores ---")
                        for a in autores:
                            print(f"ID: {a.id}, Nome: {a.nome}, Nacionalidade: {a.nacionalidade}")
                    else:
                        print("Nenhum autor encontrado.")
                except Exception as e:
                    print(f"Erro ao listar autores: {e}")
                    
            case '3':
                try:
                    id_autor = int(input("ID do autor: "))
                    autor_existente = AutorController.buscar_autor_por_id(id_autor)
                    
                    if autor_existente:
                        print(f"Autor atual: {autor_existente.nome}")
                        novo_nome = input("Novo nome: ")
                        nova_nacionalidade = input("Nova nacionalidade: ")
                        
                        autor_atualizado = Autor(id_autor, novo_nome, nova_nacionalidade)
                        AutorController.atualizar_autor(autor_atualizado)
                        print("Autor atualizado com sucesso!")
                    else:
                        print("Autor não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao atualizar autor: {e}")
                    
            case '4':
                try:
                    id_autor = int(input("ID do autor a remover: "))
                    autor_existente = AutorController.buscar_autor_por_id(id_autor)
                    
                    if autor_existente:
                        confirmacao = input(f"Tem certeza que deseja remover '{autor_existente.nome}'? (s/n): ")
                        if confirmacao.lower() == 's':
                            AutorController.deletar_autor(id_autor)
                            print("Autor removido com sucesso!")
                    else:
                        print("Autor não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao remover autor: {e}")
                    
            case _:
                print("Opção inválida!")

def menu_usuarios():
    while True:
        print("\n--- Menu Usuários ---")
        print("1. Inserir usuário")
        print("2. Listar usuários")
        print("3. Atualizar usuário")
        print("4. Deletar usuário")
        print("0. Voltar")
        opcao = input("Escolha: ")

        match opcao:
            case '0':
                break
            case '1':
                try:
                    nome = input("Nome: ")
                    email = input("Email: ")
                    telefone = input("Telefone: ")
                    
                    usuario = Usuario(None, nome, email, telefone)
                    resultado = UsuarioController.inserir_usuario(usuario)
                    print(f"Usuário inserido com ID: {resultado.id}")
                except Exception as e:
                    print(f"Erro ao inserir usuário: {e}")
                    
            case '2':
                try:
                    usuarios = UsuarioController.listar_usuarios()
                    if usuarios:
                        print("\n--- Lista de Usuários ---")
                        for u in usuarios:
                            print(f"ID: {u.id}, Nome: {u.nome}, Email: {u.email}, Telefone: {u.telefone}")
                    else:
                        print("Nenhum usuário encontrado.")
                except Exception as e:
                    print(f"Erro ao listar usuários: {e}")
                    
            case '3':
                try:
                    id_usuario = int(input("ID do usuário: "))
                    usuario_existente = UsuarioController.buscar_usuario_por_id(id_usuario)
                    
                    if usuario_existente:
                        print(f"Usuário atual: {usuario_existente.nome}")
                        novo_nome = input("Novo nome: ")
                        novo_email = input("Novo email: ")
                        novo_telefone = input("Novo telefone: ")
                        
                        usuario_atualizado = Usuario(id_usuario, novo_nome, novo_email, novo_telefone)
                        UsuarioController.atualizar_usuario(usuario_atualizado)
                        print("Usuário atualizado com sucesso!")
                    else:
                        print("Usuário não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao atualizar usuário: {e}")
                    
            case '4':
                try:
                    id_usuario = int(input("ID do usuário a remover: "))
                    usuario_existente = UsuarioController.buscar_usuario_por_id(id_usuario)
                    
                    if usuario_existente:
                        confirmacao = input(f"Tem certeza que deseja remover '{usuario_existente.nome}'? (s/n): ")
                        if confirmacao.lower() == 's':
                            UsuarioController.deletar_usuario(id_usuario)
                            print("Usuário removido com sucesso!")
                    else:
                        print("Usuário não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao remover usuário: {e}")
                    
            case _:
                print("Opção inválida!")

def menu_emprestimos():
    while True:
        print("\n--- Menu Empréstimos ---")
        print("1. Registrar empréstimo")
        print("2. Listar empréstimos")
        print("3. Devolver livro")
        print("4. Deletar empréstimo")
        print("0. Voltar")
        opcao = input("Escolha: ")

        match opcao:
            case '0':
                break
            case '1':
                try:
                    id_usuario = int(input("ID do usuário: "))
                    id_livro = int(input("ID do livro: "))
                    data_emprestimo = input("Data do empréstimo (YYYY-MM-DD): ")
                    data_devolucao = input("Data da devolução (YYYY-MM-DD): ")
                    
                    # Validar formato das datas
                    datetime.strptime(data_emprestimo, '%Y-%m-%d')
                    datetime.strptime(data_devolucao, '%Y-%m-%d')
                    
                    emprestimo = Emprestimo(None, id_usuario, id_livro, data_emprestimo, data_devolucao, False)
                    resultado = EmprestimoController.inserir_emprestimo(emprestimo)
                    
                    if resultado:
                        print(f"Empréstimo registrado com ID: {resultado.id}")
                    else:
                        print("Erro: Livro não disponível para empréstimo!")
                        
                except ValueError as ve:
                    if "time data" in str(ve):
                        print("Erro: Formato de data inválido! Use YYYY-MM-DD")
                    else:
                        print("Erro: Valores inválidos inseridos!")
                except Exception as e:
                    print(f"Erro ao registrar empréstimo: {e}")
                    
            case '2':
                try:
                    emprestimos = EmprestimoController.listar_emprestimos()
                    if emprestimos:
                        print("\n--- Lista de Empréstimos ---")
                        for e in emprestimos:
                            status = "Sim" if e.devolvido else "Não"
                            print(f"ID: {e.id}, Usuário ID: {e.id_usuario}, Livro ID: {e.id_livro}")
                            print(f"    Empréstimo: {e.data_emprestimo}, Devolução: {e.data_devolucao}, Devolvido: {status}")
                    else:
                        print("Nenhum empréstimo encontrado.")
                except Exception as e:
                    print(f"Erro ao listar empréstimos: {e}")
                    
            case '3':
                try:
                    id_emprestimo = int(input("ID do empréstimo: "))
                    emprestimo_existente = EmprestimoController.buscar_emprestimo_por_id(id_emprestimo)
                    
                    if emprestimo_existente:
                        if emprestimo_existente.devolvido:
                            print("Este empréstimo já foi devolvido!")
                        else:
                            data_devolucao = input("Data da devolução (YYYY-MM-DD) ou ENTER para hoje: ")
                            if not data_devolucao:
                                data_devolucao = datetime.now().strftime('%Y-%m-%d')
                            else:
                                # Validar formato da data
                                datetime.strptime(data_devolucao, '%Y-%m-%d')
                            
                            EmprestimoController.devolver_livro(id_emprestimo, data_devolucao)
                            print("Livro devolvido com sucesso!")
                    else:
                        print("Empréstimo não encontrado!")
                        
                except ValueError as ve:
                    if "time data" in str(ve):
                        print("Erro: Formato de data inválido! Use YYYY-MM-DD")
                    else:
                        print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao devolver livro: {e}")
                    
            case '4':
                try:
                    id_emprestimo = int(input("ID do empréstimo a remover: "))
                    emprestimo_existente = EmprestimoController.buscar_emprestimo_por_id(id_emprestimo)
                    
                    if emprestimo_existente:
                        confirmacao = input(f"Tem certeza que deseja remover o empréstimo ID {id_emprestimo}? (s/n): ")
                        if confirmacao.lower() == 's':
                            EmprestimoController.deletar_emprestimo(id_emprestimo)
                            print("Empréstimo removido com sucesso!")
                    else:
                        print("Empréstimo não encontrado!")
                except ValueError:
                    print("Erro: ID inválido!")
                except Exception as e:
                    print(f"Erro ao remover empréstimo: {e}")
                    
            case _:
                print("Opção inválida!")

def main():
    while True:
        menu()
        op = input("\nEscolha: ")
        match op:
            case "1":
                menu_livros()
            case "2":
                menu_autores()
            case "3":
                menu_usuarios()
            case "4":
                menu_emprestimos()
            case "0":
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    main()