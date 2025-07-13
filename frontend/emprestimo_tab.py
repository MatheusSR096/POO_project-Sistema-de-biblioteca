# ui/emprestimo_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from backend.models import Emprestimo
from backend.controllers.controller_emprestimo import EmprestimoController
from backend.controllers.controller_usuario import UsuarioController
from backend.controllers.controller_livro import LivroController

class EmprestimoTab:
    def __init__(self, notebook, main_app_instance):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Empréstimos")
        self.main_app = main_app_instance 
        self.controller = EmprestimoController
        self.usuario_controller = UsuarioController
        self.livro_controller = LivroController
        self.item_selecionado = None
        self._setup_ui()
        self.carregar_emprestimos()

    def _setup_ui(self):
        # Frame for form
        form_frame = ttk.LabelFrame(self.frame, text="Novo Empréstimo", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="Usuário:").grid(row=0, column=0, sticky='w', pady=2)
        self.emprestimo_usuario_combo = ttk.Combobox(form_frame, width=27, state='readonly')
        self.emprestimo_usuario_combo.grid(row=0, column=1, pady=2, padx=5)
        
        tk.Label(form_frame, text="Livro:").grid(row=0, column=2, sticky='w', pady=2)
        self.emprestimo_livro_combo = ttk.Combobox(form_frame, width=27, state='readonly')
        self.emprestimo_livro_combo.grid(row=0, column=3, pady=2, padx=5)
        
        tk.Label(form_frame, text="Data Empréstimo:").grid(row=1, column=0, sticky='w', pady=2)
        self.emprestimo_data_emp = tk.Entry(form_frame, width=15)
        self.emprestimo_data_emp.grid(row=1, column=1, pady=2, padx=5)
        self.emprestimo_data_emp.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(form_frame, text="Data Devolução:").grid(row=1, column=2, sticky='w', pady=2)
        self.emprestimo_data_dev = tk.Entry(form_frame, width=15)
        self.emprestimo_data_dev.grid(row=1, column=3, pady=2, padx=5)
        self.emprestimo_data_dev.insert(0, (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'))
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Emprestar", command=self._emprestar_livro, 
                  bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Devolver", command=self._devolver_livro_emprestimo, 
                  bg='#3498db', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self._limpar_emprestimo, 
                  bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        
        # Treeview for listing
        list_frame = ttk.LabelFrame(self.frame, text="Lista de Empréstimos", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Usuário', 'Livro', 'Data Emp.', 'Data Dev.', 'Devolvido'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Usuário', text='Usuário')
        self.tree.heading('Livro', text='Livro')
        self.tree.heading('Data Emp.', text='Data Emp.')
        self.tree.heading('Data Dev.', text='Data Dev.')
        self.tree.heading('Devolvido', text='Devolvido')
        self.tree.column('ID', width=50)
        self.tree.column('Data Emp.', width=100)
        self.tree.column('Data Dev.', width=100)
        self.tree.column('Devolvido', width=80)
        self.tree.bind('<Double-1>', self._selecionar_emprestimo)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _emprestar_livro(self):
        usuario_combo_value = self.emprestimo_usuario_combo.get()
        livro_combo_value = self.emprestimo_livro_combo.get()
        data_emp_str = self.emprestimo_data_emp.get().strip()
        data_dev_str = self.emprestimo_data_dev.get().strip()

        if not usuario_combo_value or not livro_combo_value or not data_emp_str or not data_dev_str:
            messagebox.showwarning("Aviso", "Todos os campos (Usuário, Livro, Data Empréstimo, Data Devolução) são obrigatórios!")
            return

        try:
            usuario_id = int(usuario_combo_value.split(' - ')[0])
            livro_id = int(livro_combo_value.split(' - ')[0])
            data_emprestimo = datetime.strptime(data_emp_str, '%Y-%m-%d')
            data_devolucao = datetime.strptime(data_dev_str, '%Y-%m-%d')

            if data_emprestimo > data_devolucao:
                messagebox.showwarning("Aviso", "A data de devolução não pode ser anterior à data de empréstimo.")
                return

            emprestimo = Emprestimo(
                id_usuario=usuario_id,
                id_livro=livro_id,
                data_emprestimo=data_emprestimo,
                data_devolucao=data_devolucao
            )
            
            emprestimo_criado = self.controller.inserir_emprestimo(emprestimo)
            if emprestimo_criado:
                self._limpar_emprestimo()
                self.carregar_emprestimos()
                self.main_app.livro_tab.carregar_livros() # Notify LivroTab to update its treeview (availability)
                self.main_app.atualizar_combos_livros_disponiveis() # Update available books for new loans
                messagebox.showinfo("Sucesso", "Livro emprestado com sucesso!")
            else:
                messagebox.showerror("Erro", "O livro selecionado não está disponível para empréstimo ou não existe.")
        except ValueError:
            messagebox.showwarning("Aviso", "As datas devem estar no formato AAAA-MM-DD.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar empréstimo: {str(e)}")

    def _devolver_livro_emprestimo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para devolver!")
            return
        
        try:
            item = self.tree.item(selected)
            emprestimo_id = item['values'][0]
            
            emprestimo = self.controller.buscar_emprestimo_por_id(emprestimo_id)
            if not emprestimo:
                messagebox.showerror("Erro", "Empréstimo não encontrado.")
                return

            if emprestimo.devolvido:
                messagebox.showwarning("Aviso", "Este livro já foi devolvido.")
                return

            if messagebox.askyesno("Confirmar Devolução", "Confirmar a devolução deste livro?"):
                data_devolucao_real = datetime.now() # Current return date
                if self.controller.devolver_livro(emprestimo_id, data_devolucao_real):
                    self._limpar_emprestimo()
                    self.carregar_emprestimos()
                    self.main_app.livro_tab.carregar_livros() # Notify LivroTab to update its treeview (availability)
                    self.main_app.atualizar_combos_livros_disponiveis() # Update available books for new loans
                    messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível realizar a devolução.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao devolver livro: {str(e)}")
    
    def _limpar_emprestimo(self):
        self.emprestimo_usuario_combo.set('')
        self.emprestimo_livro_combo.set('')
        self.emprestimo_data_emp.delete(0, tk.END)
        self.emprestimo_data_emp.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.emprestimo_data_dev.delete(0, tk.END)
        self.emprestimo_data_dev.insert(0, (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'))
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.item_selecionado = None
    
    def carregar_emprestimos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        emprestimos = self.controller.listar_emprestimos()
        for emprestimo in emprestimos:
            usuario = self.usuario_controller.buscar_usuario_por_id(emprestimo.id_usuario)
            livro = self.livro_controller.buscar_livro_por_id(emprestimo.id_livro)
            
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            livro_titulo = livro.titulo if livro else "Desconhecido"
            data_emp_str = emprestimo.data_emprestimo.strftime('%Y-%m-%d') if emprestimo.data_emprestimo else ""
            data_dev_str = emprestimo.data_devolucao.strftime('%Y-%m-%d') if emprestimo.data_devolucao else ""
            devolvido_str = "Sim" if emprestimo.devolvido else "Não"
            
            self.tree.insert('', 'end', values=(emprestimo.id, usuario_nome, livro_titulo, data_emp_str, data_dev_str, devolvido_str))
    
    def _selecionar_emprestimo(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            self.item_selecionado = item['values'][0] # ID do empréstimo

            self._limpar_emprestimo() # Clear before populating

            # Populate user combobox
            usuario_nome_selecionado = item['values'][1]
            usuarios = self.usuario_controller.listar_usuarios()
            for usuario in usuarios:
                if usuario.nome == usuario_nome_selecionado:
                    self.emprestimo_usuario_combo.set(f"{usuario.id} - {usuario.nome}")
                    break
            
            livro_titulo_selecionado = item['values'][2]
            livros = self.livro_controller.listar_livros()
            for livro in livros:
                if livro.titulo == livro_titulo_selecionado:
                    autor = self.main_app.autor_tab.controller.buscar_autor_por_id(livro.id_autor) # Access autor controller via main_app
                    autor_nome = autor.nome if autor else "Desconhecido"
                    self.emprestimo_livro_combo.set(f"{livro.id} - {livro.titulo} ({autor_nome})")
                    break

            self.emprestimo_data_emp.delete(0, tk.END)
            self.emprestimo_data_emp.insert(0, item['values'][3])
            self.emprestimo_data_dev.delete(0, tk.END)
            self.emprestimo_data_dev.insert(0, item['values'][4])

    def atualizar_combos_emprestimo(self):
        # Update user combobox
        usuarios = self.usuario_controller.listar_usuarios()
        self.emprestimo_usuario_combo['values'] = [f"{usuario.id} - {usuario.nome}" for usuario in usuarios]
        # Update book combobox (only available ones for new loans)
        livros_disponiveis = self.livro_controller.buscar_livro_disponivel()
        livro_options = []
        for livro in livros_disponiveis:
            # Get autor name for display in combobox
            autor = self.main_app.autor_tab.controller.buscar_autor_por_id(livro.id_autor)
            autor_nome = autor.nome if autor else "Desconhecido"
            livro_options.append(f"{livro.id} - {livro.titulo}")
        self.emprestimo_livro_combo['values'] = livro_options