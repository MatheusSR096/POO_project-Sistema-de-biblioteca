# Sistema de Biblioteca

![demostração do sistema](sistema_biblioteca_gif.gif)

## Descrição
Este é um sistema de gerenciamento de biblioteca desenvolvido em Python com interface gráfica Tkinter e banco de dados MySQL. O sistema permite o cadastro e gerenciamento de autores, livros, usuários e empréstimos, além de fornecer relatórios sobre o acervo.

## Estrutura do Projeto
```
poo_project/
├── app.py                  # Arquivo principal da aplicação
├── db_scheme.sql           # Esquema do banco de dados
├── populatedb.py           # Script para popular o banco com dados de exemplo
├── .gitignore              # Arquivos ignorados pelo Git
├── backend/
│   ├── db.py              # Conexão com o banco de dados
│   ├── models.py          # Modelos de dados (Autor, Livro, Usuario, Emprestimo)
│   └── controllers/       # Controladores para cada entidade
│       ├── controller_autor.py
│       ├── controller_livro.py
│       ├── controller_usuario.py
│       └── controller_emprestimo.py
└── frontend/
    ├── autor_tab.py       # Interface para gerenciamento de autores
    ├── livro_tab.py       # Interface para gerenciamento de livros
    ├── usuario_tab.py     # Interface para gerenciamento de usuários
    ├── emprestimo_tab.py  # Interface para gerenciamento de empréstimos
    └── relatorio_tab.py   # Interface para geração de relatórios
```

## Funcionalidades

### 1. Gerenciamento de Autores
- Adicionar, atualizar e excluir autores
- Visualizar lista de autores cadastrados
- Campos: Nome e Nacionalidade

### 2. Gerenciamento de Livros
- Adicionar, atualizar e excluir livros
- Visualizar lista de livros com informações do autor
- Campos: Título, Ano de publicação, Autor (seleção), Disponibilidade
- Validação de empréstimos ativos antes da exclusão

### 3. Gerenciamento de Usuários
- Adicionar, atualizar e excluir usuários
- Visualizar lista de usuários cadastrados
- Campos: Nome, Email (com validação), Telefone (com validação)
- Validação de dados obrigatórios e formatos

### 4. Gerenciamento de Empréstimos
- Realizar empréstimos de livros
- Devolver livros emprestados
- Visualizar lista de empréstimos com status de devolução
- Campos: Usuário (seleção), Livro (seleção), Data de empréstimo, Data de devolução prevista
- Validação de disponibilidade de livros antes do empréstimo
- Atualização automática de disponibilidade ao emprestar/devolver

### 5. Relatórios
- Livros disponíveis
- Livros emprestados
- Empréstimos ativos

## Requisitos
- Python 3.12
- MySQL Server
- Bibliotecas Python:
  - mysql-connector-python
  - python-dotenv

## Uso
A aplicação possui uma interface com abas para cada funcionalidade:
- **Autores**: Cadastro e gerenciamento de autores
- **Livros**: Cadastro e gerenciamento de livros
- **Usuários**: Cadastro e gerenciamento de usuários
- **Empréstimos**: Realização de empréstimos e devoluções
- **Relatórios**: Geração de relatórios do acervo

## Validações Implementadas
- Validação de campos obrigatórios
- Validação de formato de email
- Validação de formato de telefone
- Validação de datas de empréstimo/devolução
- Impedimento de exclusão de autores com livros associados
- Impedimento de exclusão de livros com empréstimos ativos
- Impedimento de exclusão de usuários com empréstimos ativos
- Verificação de disponibilidade de livros antes do empréstimo
