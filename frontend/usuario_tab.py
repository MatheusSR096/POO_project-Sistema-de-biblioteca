# ui/usuario_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.models import Usuario
from backend.controllers.controller_usuario import UsuarioController
from backend.controllers.controller_emprestimo import EmprestimoController
import re

class UsuarioTab:
    def __init__(self, notebook, main_app_instance):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Usuários")
        self.main_app = main_app_instance
        self.controller = UsuarioController
        self.emprestimo_controller = EmprestimoController
        self.item_selecionado = None
        self._setup_ui()
        self.carregar_usuarios()

    def _setup_ui(self):
        form_frame = ttk.LabelFrame(self.frame, text="Cadastro de Usuário", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky='w', pady=2)
        self.usuario_nome = tk.Entry(form_frame, width=30)
        self.usuario_nome.grid(row=0, column=1, pady=2, padx=5)

        tk.Label(form_frame, text="Email:").grid(row=0, column=2, sticky='w', pady=2)
        self.usuario_email = tk.Entry(form_frame, width=30)
        self.usuario_email.grid(row=0, column=3, pady=2, padx=5)

        tk.Label(form_frame, text="Telefone:").grid(row=1, column=0, sticky='w', pady=2)
        self.usuario_telefone = tk.Entry(form_frame, width=30)
        self.usuario_telefone.grid(row=1, column=1, pady=2, padx=5)

        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="Adicionar", command=self._adicionar_usuario,
                  bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self._atualizar_usuario,
                  bg='#f39c12', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Excluir", command=self._excluir_usuario,
                  bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self._limpar_usuario,
                  bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)

        list_frame = ttk.LabelFrame(self.frame, text="Lista de Usuários", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Nome', 'Email', 'Telefone'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.column('ID', width=50)
        self.tree.bind('<Double-1>', self._selecionar_usuario)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _validar_email(self, email):
        padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(padrao_email, email) is not None

    def _validar_telefone(self, telefone):
        padrao_telefone = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
        return re.match(padrao_telefone, telefone) is not None

    def _adicionar_usuario(self):
        nome = self.usuario_nome.get().strip()
        email = self.usuario_email.get().strip()
        telefone = self.usuario_telefone.get().strip()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email do usuário são obrigatórios!")
            return

        if not self._validar_email(email):
            messagebox.showwarning("Aviso", "Email inválido!")
            return

        if telefone and not self._validar_telefone(telefone):
            messagebox.showwarning("Aviso", "Telefone inválido!")
            return

        try:
            usuario = Usuario(nome=nome, email=email, telefone=telefone)
            self.controller.inserir_usuario(usuario)
            self._limpar_usuario()
            self.carregar_usuarios()
            self.main_app.atualizar_combos()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar usuário: {str(e)}")

    def _atualizar_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um usuário para atualizar!")
            return

        nome = self.usuario_nome.get().strip()
        email = self.usuario_email.get().strip()
        telefone = self.usuario_telefone.get().strip()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email do usuário são obrigatórios para atualização!")
            return

        if not self._validar_email(email):
            messagebox.showwarning("Aviso", "Email inválido!")
            return

        if telefone and not self._validar_telefone(telefone):
            messagebox.showwarning("Aviso", "Telefone inválido!")
            return

        try:
            item = self.tree.item(selected)
            usuario_id = item['values'][0]

            usuario = Usuario(id=usuario_id, nome=nome, email=email, telefone=telefone)
            self.controller.atualizar_usuario(usuario)
            self._limpar_usuario()
            self.carregar_usuarios()
            self.main_app.atualizar_combos()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar usuário: {str(e)}")

    def _excluir_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?"):
            try:
                item = self.tree.item(selected)
                usuario_id = item['values'][0]

                emprestimos_ativos = [e for e in self.emprestimo_controller.listar_emprestimos()
                                      if e.id_usuario == usuario_id and not e.devolvido]
                if emprestimos_ativos:
                    messagebox.showerror("Erro", "Não é possível excluir o usuário, pois ele possui empréstimos ativos.")
                    return

                if self.controller.deletar_usuario(usuario_id):
                    self._limpar_usuario()
                    self.carregar_usuarios()
                    self.main_app.atualizar_combos()
                    messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                else:
                    messagebox.showerror("Erro", "Usuário não encontrado para exclusão.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")

    def _limpar_usuario(self):
        self.usuario_nome.delete(0, tk.END)
        self.usuario_email.delete(0, tk.END)
        self.usuario_telefone.delete(0, tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.item_selecionado = None

    def carregar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for usuario in self.controller.listar_usuarios():
            self.tree.insert('', 'end', values=(usuario.id, usuario.nome, usuario.email, usuario.telefone))

    def _selecionar_usuario(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            self.item_selecionado = item['values'][0]
            self.usuario_nome.delete(0, tk.END)
            self.usuario_nome.insert(0, item['values'][1])
            self.usuario_email.delete(0, tk.END)
            self.usuario_email.insert(0, item['values'][2])
            self.usuario_telefone.delete(0, tk.END)
            self.usuario_telefone.insert(0, item['values'][3])
