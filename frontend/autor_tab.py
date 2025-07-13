# ui/autor_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.models import Autor
from backend.controllers.controller_autor import AutorController
from backend.controllers.controller_livro import LivroController 

class AutorTab:
    def __init__(self, notebook, main_app_instance):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Autores")
        self.main_app = main_app_instance 
        self.controller = AutorController
        self.livro_controller = LivroController 
        self.item_selecionado = None
        self._setup_ui()
        self.carregar_autores()

    def _setup_ui(self):
        # Frame for form
        form_frame = ttk.LabelFrame(self.frame, text="Cadastro de Autor", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky='w', pady=2)
        self.autor_nome = tk.Entry(form_frame, width=30)
        self.autor_nome.grid(row=0, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Nacionalidade:").grid(row=0, column=2, sticky='w', pady=2)
        self.autor_nacionalidade = tk.Entry(form_frame, width=30)
        self.autor_nacionalidade.grid(row=0, column=3, pady=2, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Adicionar", command=self._adicionar_autor, 
                  bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self._atualizar_autor, 
                  bg='#f39c12', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Excluir", command=self._excluir_autor, 
                  bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self._limpar_autor, 
                  bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        list_frame = ttk.LabelFrame(self.frame, text="Lista de Autores", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Nome', 'Nacionalidade'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Nacionalidade', text='Nacionalidade')
        self.tree.column('ID', width=50)
        self.tree.bind('<Double-1>', self._selecionar_autor)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _adicionar_autor(self):
        if not self.autor_nome.get().strip():
            messagebox.showwarning("Aviso", "Nome do autor é obrigatório!")
            return
        
        try:
            autor = Autor(
                nome=self.autor_nome.get().strip(),
                nacionalidade=self.autor_nacionalidade.get().strip()
            )
            self.controller.inserir_autor(autor)
            self._limpar_autor()
            self.carregar_autores()
            self.main_app.atualizar_combos() 
            messagebox.showinfo("Sucesso", "Autor adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar autor: {str(e)}")
    
    def _atualizar_autor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um autor para atualizar!")
            return
        
        if not self.autor_nome.get().strip():
            messagebox.showwarning("Aviso", "Nome do autor é obrigatório para atualização!")
            return

        try:
            item = self.tree.item(selected)
            autor_id = item['values'][0]
            
            autor = Autor(
                id=autor_id,
                nome=self.autor_nome.get().strip(),
                nacionalidade=self.autor_nacionalidade.get().strip()
            )
            self.controller.atualizar_autor(autor)
            self._limpar_autor()
            self.carregar_autores()
            self.main_app.atualizar_combos() 
            messagebox.showinfo("Sucesso", "Autor atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar autor: {str(e)}")
            
    def _excluir_autor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um autor para excluir!")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este autor?"):
            try:
                item = self.tree.item(selected)
                autor_id = item['values'][0]
                
                livros_associados = [livro for livro in self.livro_controller.listar_livros() if livro.id_autor == autor_id]
                if livros_associados:
                    messagebox.showerror("Erro", "Não é possível excluir o autor, pois há livros associados a ele.")
                    return

                if self.controller.deletar_autor(autor_id):
                    self._limpar_autor()
                    self.carregar_autores()
                    self.main_app.atualizar_combos() 
                    messagebox.showinfo("Sucesso", "Autor excluído com sucesso!")
                else:
                    messagebox.showerror("Erro", "Autor não encontrado para exclusão.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir autor: {str(e)}")
    
    def _limpar_autor(self):
        self.autor_nome.delete(0, tk.END)
        self.autor_nacionalidade.delete(0, tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.item_selecionado = None
    
    def carregar_autores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for autor in self.controller.listar_autores():
            self.tree.insert('', 'end', values=(autor.id, autor.nome, autor.nacionalidade))
    
    def _selecionar_autor(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            self.item_selecionado = item['values'][0] # ID do autor
            self.autor_nome.delete(0, tk.END)
            self.autor_nome.insert(0, item['values'][1])
            self.autor_nacionalidade.delete(0, tk.END)
            self.autor_nacionalidade.insert(0, item['values'][2])