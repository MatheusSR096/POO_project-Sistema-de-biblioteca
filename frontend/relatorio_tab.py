# ui/relatorio_tab.py
import tkinter as tk
from tkinter import ttk
from backend.controllers.controller_livro import LivroController
from backend.controllers.controller_emprestimo import EmprestimoController
from backend.controllers.controller_usuario import UsuarioController
from backend.controllers.controller_autor import AutorController

class RelatorioTab:
    def __init__(self, notebook, main_app_instance):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Relatórios")
        self.main_app = main_app_instance 
        self.livro_controller = LivroController
        self.emprestimo_controller = EmprestimoController
        self.usuario_controller = UsuarioController
        self.autor_controller = AutorController
        self._setup_ui()

    def _setup_ui(self):
        # Frame for report buttons
        btn_frame = ttk.LabelFrame(self.frame, text="Relatórios Disponíveis", padding=10)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Livros Disponíveis", command=self._relatorio_livros_disponiveis, 
                  bg='#3498db', fg='white', width=20).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Livros Emprestados", command=self._relatorio_livros_emprestados, 
                  bg='#e67e22', fg='white', width=20).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Empréstimos Ativos", command=self._relatorio_emprestimos_ativos, 
                  bg='#9b59b6', fg='white', width=20).pack(side='left', padx=5)
        
        # Text area to display reports
        text_frame = ttk.LabelFrame(self.frame, text="Resultado do Relatório", padding=10)
        text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.relatorio_text = tk.Text(text_frame, height=20, width=80)
        scrollbar_text = ttk.Scrollbar(text_frame, orient='vertical', command=self.relatorio_text.yview)
        self.relatorio_text.configure(yscrollcommand=scrollbar_text.set)
        
        self.relatorio_text.pack(side='left', fill='both', expand=True)
        scrollbar_text.pack(side='right', fill='y')
    
    def _relatorio_livros_disponiveis(self):
        self.relatorio_text.delete(1.0, tk.END)
        livros_disponiveis = self.livro_controller.buscar_livro_disponivel()
        
        if not livros_disponiveis:
            self.relatorio_text.insert(tk.END, "Não há livros disponíveis no momento.\n")
            return
        
        self.relatorio_text.insert(tk.END, "--- Relatório de Livros Disponíveis ---\n")
        for livro in livros_disponiveis:
            autor = self.autor_controller.buscar_autor_por_id(livro.id_autor)
            autor_nome = autor.nome if autor else "Desconhecido"
            self.relatorio_text.insert(tk.END, f"ID: {livro.id}, Título: {livro.titulo}, Ano: {livro.ano}, Autor: {autor_nome}\n")
        self.relatorio_text.insert(tk.END, "--------------------------------------\n")

    def _relatorio_livros_emprestados(self):
        self.relatorio_text.delete(1.0, tk.END)
        emprestimos = self.emprestimo_controller.listar_emprestimos()
        
        livros_emprestados = []
        for emp in emprestimos:
            if not emp.devolvido:
                livros_emprestados.append(emp)

        if not livros_emprestados:
            self.relatorio_text.insert(tk.END, "Não há livros emprestados no momento.\n")
            return
            
        self.relatorio_text.insert(tk.END, "--- Relatório de Livros Emprestados ---\n")
        for emp in livros_emprestados:
            livro = self.livro_controller.buscar_livro_por_id(emp.id_livro)
            usuario = self.usuario_controller.buscar_usuario_por_id(emp.id_usuario)

            livro_titulo = livro.titulo if livro else "Desconhecido"
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            data_emp_str = emp.data_emprestimo.strftime('%Y-%m-%d')
            data_dev_str = emp.data_devolucao.strftime('%Y-%m-%d') if emp.data_devolucao else "N/A"

            self.relatorio_text.insert(tk.END, f"Livro: {livro_titulo}, Usuário: {usuario_nome}, Data Empréstimo: {data_emp_str}, Data Prevista Devolução: {data_dev_str}\n")
        self.relatorio_text.insert(tk.END, "----------------------------------------\n")

    def _relatorio_emprestimos_ativos(self):
        self.relatorio_text.delete(1.0, tk.END)
        emprestimos = self.emprestimo_controller.listar_emprestimos()

        emprestimos_ativos = []
        for emp in emprestimos:
            if not emp.devolvido:
                emprestimos_ativos.append(emp)
        
        if not emprestimos_ativos:
            self.relatorio_text.insert(tk.END, "Não há empréstimos ativos no momento.\n")
            return

        self.relatorio_text.insert(tk.END, "--- Relatório de Empréstimos Ativos ---\n")
        for emp in emprestimos_ativos:
            usuario = self.usuario_controller.buscar_usuario_por_id(emp.id_usuario)
            livro = self.livro_controller.buscar_livro_por_id(emp.id_livro)
            
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            livro_titulo = livro.titulo if livro else "Desconhecido"
            data_emp_str = emp.data_emprestimo.strftime('%Y-%m-%d')
            data_dev_str = emp.data_devolucao.strftime('%Y-%m-%d') if emp.data_devolucao else "N/A"
            
            self.relatorio_text.insert(tk.END, f"ID: {emp.id}, Usuário: {usuario_nome}, Livro: {livro_titulo}, Data Empréstimo: {data_emp_str}, Data Prevista Devolução: {data_dev_str}\n")
        self.relatorio_text.insert(tk.END, "---------------------------------------\n")