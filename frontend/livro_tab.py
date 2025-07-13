# ui/livro_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.models import Livro
from backend.controllers.controller_livro import LivroController
from backend.controllers.controller_autor import AutorController # For author combobox
from backend.controllers.controller_emprestimo import EmprestimoController # To check for active loans

class LivroTab:
    def __init__(self, notebook, main_app_instance):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Livros")
        self.main_app = main_app_instance # Reference to the main app for callbacks
        self.controller = LivroController
        self.autor_controller = AutorController
        self.emprestimo_controller = EmprestimoController
        self.item_selecionado = None
        self._setup_ui()
        self.carregar_livros() # Initial load

    def _setup_ui(self):
        # Frame for form
        form_frame = ttk.LabelFrame(self.frame, text="Cadastro de Livro", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky='w', pady=2)
        self.livro_titulo = tk.Entry(form_frame, width=30)
        self.livro_titulo.grid(row=0, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Ano:").grid(row=0, column=2, sticky='w', pady=2)
        self.livro_ano = tk.Entry(form_frame, width=15)
        self.livro_ano.grid(row=0, column=3, pady=2, padx=5)
        
        tk.Label(form_frame, text="Autor:").grid(row=1, column=0, sticky='w', pady=2)
        self.livro_autor_combo = ttk.Combobox(form_frame, width=27, state='readonly')
        self.livro_autor_combo.grid(row=1, column=1, pady=2, padx=5)
        
        self.livro_disponivel = tk.BooleanVar(value=True)
        tk.Checkbutton(form_frame, text="Disponível", variable=self.livro_disponivel).grid(row=1, column=2, pady=2)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Adicionar", command=self._adicionar_livro, 
                  bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self._atualizar_livro, 
                  bg='#f39c12', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Excluir", command=self._excluir_livro, 
                  bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self._limpar_livro, 
                  bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        # Treeview for listing
        list_frame = ttk.LabelFrame(self.frame, text="Lista de Livros", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Título', 'Ano', 'Autor', 'Disponível'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Título', text='Título')
        self.tree.heading('Ano', text='Ano')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Disponível', text='Disponível')
        self.tree.column('ID', width=50)
        self.tree.column('Ano', width=80)
        self.tree.column('Disponível', width=80)
        self.tree.bind('<Double-1>', self._selecionar_livro)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _adicionar_livro(self):
        titulo = self.livro_titulo.get().strip()
        ano_str = self.livro_ano.get().strip()
        autor_combo_value = self.livro_autor_combo.get()
        disponivel = self.livro_disponivel.get()

        if not titulo or not ano_str or not autor_combo_value:
            messagebox.showwarning("Aviso", "Todos os campos (Título, Ano, Autor) são obrigatórios para o livro!")
            return
        
        try:
            ano = int(ano_str)
            if ano <= 0:
                messagebox.showwarning("Aviso", "O ano deve ser um número positivo.")
                return
            
            autor_id = int(autor_combo_value.split(' - ')[0])

            livro = Livro(
                titulo=titulo,
                ano=ano,
                id_autor=autor_id,
                disponivel=disponivel
            )
            self.controller.inserir_livro(livro)
            self._limpar_livro()
            self.carregar_livros()
            self.main_app.atualizar_combos() # Notify main app to update other combos
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        except ValueError:
            messagebox.showwarning("Aviso", "O ano deve ser um número válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar livro: {str(e)}")
            
    def _atualizar_livro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um livro para atualizar!")
            return
        
        titulo = self.livro_titulo.get().strip()
        ano_str = self.livro_ano.get().strip()
        autor_combo_value = self.livro_autor_combo.get()
        disponivel = self.livro_disponivel.get()

        if not titulo or not ano_str or not autor_combo_value:
            messagebox.showwarning("Aviso", "Todos os campos (Título, Ano, Autor) são obrigatórios para o livro!")
            return
            
        try:
            item = self.tree.item(selected)
            livro_id = item['values'][0]
            
            ano = int(ano_str)
            if ano <= 0:
                messagebox.showwarning("Aviso", "O ano deve ser um número positivo.")
                return

            autor_id = int(autor_combo_value.split(' - ')[0])

            livro = Livro(
                id=livro_id,
                titulo=titulo,
                ano=ano,
                id_autor=autor_id,
                disponivel=disponivel
            )
            self.controller.atualizar_livro(livro)
            self._limpar_livro()
            self.carregar_livros()
            self.main_app.atualizar_combos() # Notify main app to update other combos
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
        except ValueError:
            messagebox.showwarning("Aviso", "O ano deve ser um número válido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar livro: {str(e)}")

    def _excluir_livro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um livro para excluir!")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este livro?"):
            try:
                item = self.tree.item(selected)
                livro_id = item['values'][0]

                # Check for active loans
                emprestimos_ativos = [e for e in self.emprestimo_controller.listar_emprestimos() 
                                     if e.id_livro == livro_id and not e.devolvido]
                if emprestimos_ativos:
                    messagebox.showerror("Erro", "Não é possível excluir o livro, pois ele está emprestado.")
                    return
                
                if self.controller.deletar_livro(livro_id):
                    self._limpar_livro()
                    self.carregar_livros()
                    self.main_app.atualizar_combos() # Notify main app to update other combos
                    messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                else:
                    messagebox.showerror("Erro", "Livro não encontrado para exclusão.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir livro: {str(e)}")
    
    def _limpar_livro(self):
        self.livro_titulo.delete(0, tk.END)
        self.livro_ano.delete(0, tk.END)
        self.livro_autor_combo.set('')
        self.livro_disponivel.set(True)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.item_selecionado = None
    
    def carregar_livros(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for livro in self.controller.listar_livros():
            autor = self.autor_controller.buscar_autor_por_id(livro.id_autor)
            autor_nome = autor.nome if autor else "Desconhecido"
            self.tree.insert('', 'end', values=(livro.id, livro.titulo, livro.ano, autor_nome, "Sim" if livro.disponivel else "Não"))
        self.atualizar_autores_combobox() # Ensure combobox is updated when books are loaded
    
    def _selecionar_livro(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            self.item_selecionado = item['values'][0] # ID do livro
            self.livro_titulo.delete(0, tk.END)
            self.livro_titulo.insert(0, item['values'][1])
            self.livro_ano.delete(0, tk.END)
            self.livro_ano.insert(0, item['values'][2])
            
            autor_nome_selecionado = item['values'][3]
            autores = self.autor_controller.listar_autores()
            for autor in autores:
                if autor.nome == autor_nome_selecionado:
                    self.livro_autor_combo.set(f"{autor.id} - {autor.nome}")
                    break
            
            self.livro_disponivel.set(True if item['values'][4] == "Sim" else False)

    def atualizar_autores_combobox(self):
        autores = self.autor_controller.listar_autores()
        self.livro_autor_combo['values'] = [f"{autor.id} - {autor.nome}" for autor in autores]
        # Keep current selection if it's still valid, otherwise clear
        current_selection = self.livro_autor_combo.get()
        if current_selection and current_selection not in self.livro_autor_combo['values']:
            self.livro_autor_combo.set('')