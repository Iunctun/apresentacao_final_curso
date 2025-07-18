import tkinter as tk
from tkinter import ttk, messagebox, font
import json
from datetime import datetime
import os
import re

# Cores do Sistema
branco = "#ffffff"
cinza_claro = "#f8f9fa"
cinza_medio = "#e9ecef"
cinza_escuro = "#6c757d"
azul_suave = "#4a90e2"
preto_suave = "#2c3e50"
azul_suave_bg = "#d0d7db"
azul_cinza = "#2a4b61"

class ModernCRUDApp:
    def __init__(self, root):
        self.root = root
        self.usuarios = []
        self.editing_index = None
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        self.carregar_dados()
        
    def setup_window(self):
        self.root.title("Sistema de Cadastro CRUD - S/A")
        self.root.geometry("1700x900")
        self.root.configure(bg=azul_suave_bg)
        self.root.resizable(False, False)
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       background=azul_suave_bg,
                       foreground=preto_suave)
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       background=branco,
                       foreground=preto_suave)
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))
        
        style.configure('Modern.Treeview',
                       font=('Segoe UI', 10),
                       rowheight=30,
                       background=branco,
                       foreground=preto_suave)
        
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       background=azul_cinza,
                       foreground='white')
        
        style.map('Modern.Treeview',
            background=[('selected', azul_suave)],
            foreground=[('selected', branco)])
    
    def formatar_cpf(self, event):
        """Formata o CPF automaticamente enquanto digita"""
        widget = event.widget
        valor = widget.get()
        
        # Remove tudo que não é número
        apenas_numeros = re.sub(r'[^0-9]', '', valor)
        
        # Limita a 11 dígitos
        if len(apenas_numeros) > 11:
            apenas_numeros = apenas_numeros[:11]
        
        # Aplica formatação
        if len(apenas_numeros) <= 3:
            valor_formatado = apenas_numeros
        elif len(apenas_numeros) <= 6:
            valor_formatado = f"{apenas_numeros[:3]}.{apenas_numeros[3:]}"
        elif len(apenas_numeros) <= 9:
            valor_formatado = f"{apenas_numeros[:3]}.{apenas_numeros[3:6]}.{apenas_numeros[6:]}"
        else:
            valor_formatado = f"{apenas_numeros[:3]}.{apenas_numeros[3:6]}.{apenas_numeros[6:9]}-{apenas_numeros[9:]}"
        
        # Atualiza o campo
        widget.delete(0, tk.END)
        widget.insert(0, valor_formatado)
        widget.config(fg=preto_suave)
    
    def formatar_cep(self, event):
        """Formata o CEP automaticamente enquanto digita"""
        widget = event.widget
        valor = widget.get()
        
        # Remove tudo que não é número
        apenas_numeros = re.sub(r'[^0-9]', '', valor)
        
        # Limita a 8 dígitos
        if len(apenas_numeros) > 8:
            apenas_numeros = apenas_numeros[:8]
        
        # Aplica formatação
        if len(apenas_numeros) <= 5:
            valor_formatado = apenas_numeros
        else:
            valor_formatado = f"{apenas_numeros[:5]}-{apenas_numeros[5:]}"
        
        # Atualiza o campo
        widget.delete(0, tk.END)
        widget.insert(0, valor_formatado)
        widget.config(fg=preto_suave)
    
    def limitar_idade(self, event):
        """Limita a idade a apenas números e máximo 3 dígitos"""
        widget = event.widget
        valor = widget.get()
        
        # Remove tudo que não é número
        apenas_numeros = re.sub(r'[^0-9]', '', valor)
        
        # Limita a 3 dígitos
        if len(apenas_numeros) > 3:
            apenas_numeros = apenas_numeros[:3]
        
        # Atualiza o campo
        widget.delete(0, tk.END)
        widget.insert(0, apenas_numeros)
        widget.config(fg=preto_suave)
            
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=azul_suave_bg)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header Titulo
        header_frame = tk.Frame(main_frame, bg=azul_suave_bg, height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ttk.Label(header_frame, text="Sistema de Cadastro CRUD - S/A", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Container principal com duas colunas
        container = tk.Frame(main_frame, bg=azul_suave_bg)
        container.pack(fill='both', expand=True)
        
        # Coluna esquerda - Formulário (reduzida)
        left_frame = tk.Frame(container, bg=branco, relief='solid', bd=1, width=500)
        left_frame.pack(side='left', fill='y', padx=(0, 15))
        left_frame.pack_propagate(False)
        
        # Coluna direita - Lista de usuários
        right_frame = tk.Frame(container, bg=branco, relief='solid', bd=1)
        right_frame.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        self.create_form_section(left_frame)
        self.create_list_section(right_frame)
        
    def create_form_section(self, parent):
        # Título da seção
        form_title = ttk.Label(parent, text="👤 Cadastro de Usuário", style='Header.TLabel')
        form_title.pack(pady=25)

        # Frame principal do formulário
        form_frame = tk.Frame(parent, bg=branco)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Campo Nome
        self.create_form_field(form_frame, "Nome Completo:", "entry_nome", required=True)

        # Campo CPF com formatação
        self.create_form_field(form_frame, "CPF:", "entry_cpf", required=True, 
                              placeholder=" 000.000.000-00", field_type="cpf")

        # Campo Idade (apenas números)
        self.create_form_field(form_frame, "Idade:", "entry_idade", required=True, 
                              field_type="number")

        # Campo Email
        self.create_form_field(form_frame, "E-mail:", "entry_email", required=True, 
                              placeholder=" exemplo@email.com")

        # Campo CEP com formatação
        self.create_form_field(form_frame, "CEP:", "entry_cep", required=True, 
                              placeholder=" 00000-000", field_type="cep")

        # Frame dos botões
        button_frame = tk.Frame(form_frame, bg=branco)
        button_frame.pack(pady=30)

        # Botão Cadastrar/Atualizar
        self.btn_cadastrar = tk.Button(button_frame, text="✅ Cadastrar", 
                        font=('Segoe UI', 11, 'bold'),
                        bg=azul_cinza, fg='white',
                        relief='flat', padx=15, pady=8, 
                        width=12,
                        cursor='hand2',
                        command=self.cadastrar_usuario)
        self.btn_cadastrar.pack(side='left', padx=6)

        btn_limpar = tk.Button(button_frame, text="🧹 Limpar", 
                            font=('Segoe UI', 10, 'bold'),
                            bg=azul_cinza, fg='white',
                            relief='flat', padx=15, pady=10,
                            width=12,
                            cursor='hand2',
                            command=self.limpar_formulario)
        btn_limpar.pack(side='left', padx=6)

        
    def create_form_field(self, parent, label_text, field_name, required=False, field_type="text", placeholder=""):
        # Frame do campo
        field_frame = tk.Frame(parent, bg=branco)
        field_frame.pack(fill='x', pady=10)
        
        # Label
        label = tk.Label(field_frame, 
                        text=label_text + (" *" if required else ""),
                        font=('Segoe UI', 12, 'bold'),
                        bg=branco, 
                        fg=preto_suave)
        label.pack(anchor='w', pady=(0, 5))
        
        # Entry
        entry = tk.Entry(field_frame, 
                        font=('Segoe UI', 12),
                        relief='solid', 
                        bd=1, 
                        width=35,
                        bg=cinza_claro, 
                        fg=preto_suave,
                        insertbackground=preto_suave)
        entry.pack(fill='x', pady=(0, 5))
        
        # Configurar validação e formatação baseada no tipo
        if field_type == "cpf":
            entry.bind('<KeyRelease>', self.formatar_cpf)
        elif field_type == "number":
            entry.bind('<KeyRelease>', self.limitar_idade)
        elif field_type == "cep":
            entry.bind('<KeyRelease>', self.formatar_cep)
        
        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=cinza_escuro)
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=preto_suave)
                    
            def on_focus_out(event):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg=cinza_escuro)
                    
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        # Armazenar referência
        setattr(self, field_name, entry)
        
    def create_list_section(self, parent):
        # Título da seção
        list_title = ttk.Label(parent, text="📋 Lista de Usuários", style='Header.TLabel')
        list_title.pack(pady=25)
        
        # Frame da lista
        list_frame = tk.Frame(parent, bg=branco, relief='solid', bd=1)
        list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview
        columns = ('Nome', 'CPF', 'Idade', 'E-mail', 'CEP')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                style='Modern.Treeview')
        
        # Configurar cabeçalhos
        column_widths = {'Nome': 200, 'CPF': 150, 'Idade': 80, 'E-mail': 200, 'CEP': 120}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor='center')
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Pack treeview e scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.pack(side='right', fill='y')
        
        # Botões de ação
        action_frame = tk.Frame(parent, bg=branco)
        action_frame.pack(fill='x', padx=20, pady=20)
        
        btn_editar = tk.Button(action_frame, text="✏️ Editar", 
                font=('Segoe UI', 11, 'bold'),
                bg=azul_cinza, fg='white',
                relief='flat', padx=15, pady=10,  
                cursor='hand2',
                command=self.editar_usuario)
        btn_editar.pack(side='left', padx=6)

        btn_excluir = tk.Button(action_frame, text="🗑️ Excluir", 
                                font=('Segoe UI', 11, 'bold'),
                                bg=azul_cinza, fg='white',
                                relief='flat', padx=15, pady=10,
                                cursor='hand2',
                                command=self.excluir_usuario)
        btn_excluir.pack(side='left', padx=6)

        # Novo botão para atualizar lista manualmente
        btn_atualizar = tk.Button(action_frame, text="🔄 Atualizar Lista", 
                                font=('Segoe UI', 11, 'bold'),
                                bg= azul_cinza, fg='white',
                                relief='flat', padx=15, pady=10,
                                cursor='hand2',
                                command=self.atualizar_lista_manual)
        btn_atualizar.pack(side='left', padx=6)
        
        # Info label
        self.info_label = tk.Label(parent, text="Total de usuários: 0", 
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=branco, fg=preto_suave)
        self.info_label.pack(pady=15)

    def atualizar_lista_manual(self):
        """Atualiza a lista manualmente e mostra feedback"""
        self.atualizar_lista()
        messagebox.showinfo("Atualizado", "📋 Lista atualizada com sucesso!")
        
    def validar_cpf(self, cpf):
        """Valida CPF brasileiro - deve ter exatamente 11 dígitos"""
        # Remove tudo que não for número
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem exatamente 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se não é uma sequência de números iguais
        if cpf == cpf[0] * 11:
            return False
        
        return True

    def validar_email(self, email):
        """Valida formato de email"""
        if not email or '@' not in email:
            return False
        
        # Padrão mais robusto para validação de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def validar_cep(self, cep):
        """Valida CEP brasileiro - deve ter exatamente 8 dígitos"""
        # Remove formatação
        cep = re.sub(r'[^0-9]', '', cep)
        # Verifica se tem exatamente 8 dígitos
        return len(cep) == 8 and cep.isdigit()
        
    def get_field_value(self, field):
        """Obtém valor do campo removendo placeholder se necessário"""
        value = field.get().strip()
        # Remove placeholder se existir
        placeholders = ["000.000.000-00", "exemplo@email.com", "00000-000"]
        if value in placeholders:
            return ""
        return value
        
    def validar_campos(self):
        """Valida todos os campos do formulário"""
        # Obter valores dos campos
        nome = self.get_field_value(self.entry_nome)
        cpf = self.get_field_value(self.entry_cpf)
        idade = self.get_field_value(self.entry_idade)
        email = self.get_field_value(self.entry_email)
        cep = self.get_field_value(self.entry_cep)
        
        # Validar nome
        if not nome:
            messagebox.showerror("Erro de Validação", "Nome não pode estar vazio!")
            self.entry_nome.focus()
            return False
            
        if len(nome) < 2:
            messagebox.showerror("Erro de Validação", "Nome deve ter pelo menos 2 caracteres!")
            self.entry_nome.focus()
            return False
        
        # Validar CPF
        if not cpf:
            messagebox.showerror("Erro de Validação", "CPF não pode estar vazio!")
            self.entry_cpf.focus()
            return False
            
        if not self.validar_cpf(cpf):
            messagebox.showerror("Erro de Validação", "CPF inválido! Deve ter exatamente 11 dígitos.")
            self.entry_cpf.focus()
            return False
        
        # Validar idade
        if not idade:
            messagebox.showerror("Erro de Validação", "Idade não pode estar vazia!")
            self.entry_idade.focus()
            return False
            
        try:
            idade_int = int(idade)
            if idade_int <= 0 or idade_int > 150:
                messagebox.showerror("Erro de Validação", "Idade deve estar entre 1 e 150 anos!")
                self.entry_idade.focus()
                return False
        except ValueError:
            messagebox.showerror("Erro de Validação", "Idade deve ser um número válido!")
            self.entry_idade.focus()
            return False
        
        # Validar email
        if not email:
            messagebox.showerror("Erro de Validação", "E-mail não pode estar vazio!")
            self.entry_email.focus()
            return False
            
        if not self.validar_email(email):
            messagebox.showerror("Erro de Validação", "E-mail inválido! Verifique o formato.")
            self.entry_email.focus()
            return False
        
        # Validar CEP
        if not cep:
            messagebox.showerror("Erro de Validação", "CEP não pode estar vazio!")
            self.entry_cep.focus()
            return False
            
        if not self.validar_cep(cep):
            messagebox.showerror("Erro de Validação", "CEP inválido! Deve ter exatamente 8 dígitos.")
            self.entry_cep.focus()
            return False
        
        # Verificar duplicatas apenas ao cadastrar novo usuário
        if self.editing_index is None:
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            for i, usuario in enumerate(self.usuarios):
                if re.sub(r'[^0-9]', '', usuario['cpf']) == cpf_limpo:
                    messagebox.showerror("Erro", "Este CPF já está cadastrado!")
                    self.entry_cpf.focus()
                    return False
                if usuario['email'].lower() == email.lower():
                    messagebox.showerror("Erro", "Este e-mail já está cadastrado!")
                    self.entry_email.focus()
                    return False
        else:
            # Verificar duplicatas durante edição (excluindo o registro atual)
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            for i, usuario in enumerate(self.usuarios):
                if i != self.editing_index:
                    if re.sub(r'[^0-9]', '', usuario['cpf']) == cpf_limpo:
                        messagebox.showerror("Erro", "Este CPF já está cadastrado!")
                        self.entry_cpf.focus()
                        return False
                    if usuario['email'].lower() == email.lower():
                        messagebox.showerror("Erro", "Este e-mail já está cadastrado!")
                        self.entry_email.focus()
                        return False
             
        return True
    
    def cadastrar_usuario(self):
        """Cadastra novo usuário ou atualiza existente"""
        if not self.validar_campos():
            return
            
        usuario = {
            'nome': self.get_field_value(self.entry_nome),
            'cpf': self.get_field_value(self.entry_cpf),
            'idade': int(self.get_field_value(self.entry_idade)),
            'email': self.get_field_value(self.entry_email),
            'cep': self.get_field_value(self.entry_cep)
        }
        
        if self.editing_index is None:
            # Cadastrar novo usuário
            usuario['data_cadastro'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            self.usuarios.append(usuario)
            messagebox.showinfo("Sucesso!", "✅ Usuário cadastrado com sucesso!")
        else:
            # Atualizar usuário existente
            usuario['data_cadastro'] = self.usuarios[self.editing_index]['data_cadastro']
            usuario['data_atualizacao'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            self.usuarios[self.editing_index] = usuario
            messagebox.showinfo("Sucesso!", "✅ Usuário atualizado com sucesso!")
            self.cancelar_edicao()
        
        # Atualização automática da lista após cadastro/edição
        self.atualizar_lista()
        self.limpar_formulario()
        self.salvar_dados()
        
    def editar_usuario(self):
        """Carrega dados do usuário selecionado para edição"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar!")
            return
            
        item = self.tree.item(selected)
        values = item['values']
        index = self.tree.index(selected)
        
        # Preencher formulário
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, values[0])
        self.entry_nome.config(fg=preto_suave)
        
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, values[1])
        self.entry_cpf.config(fg=preto_suave)
        
        self.entry_idade.delete(0, tk.END)
        self.entry_idade.insert(0, values[2])
        self.entry_idade.config(fg=preto_suave)
        
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, values[3])
        self.entry_email.config(fg=preto_suave)
        
        self.entry_cep.delete(0, tk.END)
        self.entry_cep.insert(0, values[4])
        self.entry_cep.config(fg=preto_suave)
        
        # Ativar modo de edição
        self.editing_index = index
        self.btn_cadastrar.config(text="💾 Atualizar")
        self.btn_cancelar.config(state='normal')
        
    def excluir_usuario(self):
        """Exclui usuário selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return
            
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este usuário?"):
            index = self.tree.index(selected)
            nome_removido = self.usuarios[index]['nome']
            self.usuarios.pop(index)
            # Atualização automática após exclusão
            self.atualizar_lista()
            self.salvar_dados()
            messagebox.showinfo("Sucesso!", f"🗑️ {nome_removido} foi removido com sucesso!")
            
    def cancelar_edicao(self):
        """Cancela modo de edição"""
        self.editing_index = None
        self.btn_cadastrar.config(text="✅ Cadastrar")
        self.btn_cancelar.config(state='disabled')
        self.limpar_formulario()
        
    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, "000.000.000-00")
        self.entry_cpf.config(fg=cinza_escuro)
        
        self.entry_idade.delete(0, tk.END)
        
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, "exemplo@email.com")
        self.entry_email.config(fg=cinza_escuro)
        
        self.entry_cep.delete(0, tk.END)
        self.entry_cep.insert(0, "00000-000")
        self.entry_cep.config(fg=cinza_escuro)
            
    def atualizar_lista(self):
        """Atualiza lista de usuários na interface"""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Adicionar usuários
        for usuario in self.usuarios:
            self.tree.insert('', 'end', values=(
                usuario['nome'],
                usuario['cpf'],
                usuario['idade'],
                usuario['email'],
                usuario['cep']
            ))
            
        # Atualizar contador
        total = len(self.usuarios)
        emoji = "👥" if total > 0 else "📝"
        self.info_label.config(text=f"Total de usuários: {total} {emoji}")
        
    def salvar_dados(self):
        """Salva dados em arquivo JSON"""
        try:
            with open('usuarios_cadastrados.json', 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")
            
    def carregar_dados(self):
        """Carrega dados do arquivo JSON"""
        try:
            if os.path.exists('usuarios_cadastrados.json'):
                with open('usuarios_cadastrados.json', 'r', encoding='utf-8') as f:
                    self.usuarios = json.load(f)
                self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
            self.usuarios = []
        
    def center_window(self):
        """Centraliza janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCRUDApp(root)
    root.mainloop()