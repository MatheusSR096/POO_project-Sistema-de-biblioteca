
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from backend.controllers.controller_autor import AutorController
from backend.controllers.controller_livro import LivroController
from backend.controllers.controller_usuario import UsuarioController
from backend.controllers.controller_emprestimo import EmprestimoController

from backend.models import Autor
from backend.models import Livro
from backend.models import Usuario


from frontend.autor_tab import AutorTab
from frontend.livro_tab import LivroTab
from frontend.usuario_tab import UsuarioTab
from frontend.emprestimo_tab import EmprestimoTab
from frontend.relatorio_tab import RelatorioTab

class SistemaBiblioteca:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Biblioteca")
        self.root.configure(bg='#f0f0f0')
        
        self.autor_controller = AutorController
        self.livro_controller = LivroController
        self.usuario_controller = UsuarioController
        self.emprestimo_controller = EmprestimoController
        
        self.setup_frontend()
        self.adicionar_dados_exemplo()
        self.atualizar_combos() 

    def adicionar_dados_exemplo(self):
        if not self.autor_controller.listar_autores(): 
            autor1 = Autor(nome="J.K. Rowling", nacionalidade="Reino Unido")
            autor2 = Autor(nome="George R.R. Martin", nacionalidade="Estados Unidos")
            self.autor_controller.inserir_autor(autor1)
            self.autor_controller.inserir_autor(autor2)
        
        if not self.livro_controller.listar_livros(): 
            autor_jk = self.autor_controller.buscar_autor_por_id(1)
            autor_grrm = self.autor_controller.buscar_autor_por_id(2)

            if autor_jk:
                livro1 = Livro(titulo="Harry Potter e a Pedra Filosofal", ano=1997, id_autor=autor_jk.id)
                self.livro_controller.inserir_livro(livro1)
            if autor_grrm:
                livro2 = Livro(titulo="Game of Thrones", ano=1996, id_autor=autor_grrm.id)
                self.livro_controller.inserir_livro(livro2)
        
        if not self.usuario_controller.listar_usuarios(): 
            usuario1 = Usuario(nome="João Silva", email="joao@email.com", telefone="11999999999")
            usuario2 = Usuario(nome="Maria Santos", email="maria@email.com", telefone="11888888888")
            self.usuario_controller.inserir_usuario(usuario1)
            self.usuario_controller.inserir_usuario(usuario2)
    
    def setup_frontend(self):
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📚 Sistema de Biblioteca", 
                                font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.autor_tab = AutorTab(self.notebook, self)
        self.livro_tab = LivroTab(self.notebook, self)
        self.usuario_tab = UsuarioTab(self.notebook, self)
        self.emprestimo_tab = EmprestimoTab(self.notebook, self)
        self.relatorio_tab = RelatorioTab(self.notebook, self)

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Autores":
            self.autor_tab.carregar_autores()
        elif selected_tab == "Livros":
            self.livro_tab.carregar_livros()
            self.livro_tab.atualizar_autores_combobox() 
        elif selected_tab == "Usuários":
            self.usuario_tab.carregar_usuarios()
        elif selected_tab == "Empréstimos":
            self.emprestimo_tab.carregar_emprestimos()
            self.emprestimo_tab.atualizar_combos_emprestimo() 
        elif selected_tab == "Relatórios":
            self.relatorio_tab.relatorio_text.delete(1.0, tk.END) 

    def atualizar_combos(self):
        
        
        self.livro_tab.atualizar_autores_combobox()
        self.emprestimo_tab.atualizar_combos_emprestimo()

    
    def atualizar_combos_autores(self):
        self.livro_tab.atualizar_autores_combobox()

    def atualizar_combos_livros_disponiveis(self):
        self.emprestimo_tab.atualizar_combos_emprestimo()

    def atualizar_combos_usuarios(self):
        self.emprestimo_tab.atualizar_combos_emprestimo()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SistemaBiblioteca()
    app.run()