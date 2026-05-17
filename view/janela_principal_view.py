import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk


class JanelaPrincipal(tk.Toplevel):
    """Janela principal com barra de menus conforme especificado no trabalho."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sistema de Locação de Veículos")
        self.geometry("500x300")
        self._criar_menu()
        self._criar_widgets()

    def _criar_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        # ---- Menu Cadastro ----
        menu_cadastro = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Cadastro", menu=menu_cadastro)
        menu_cadastro.add_command(label="Veículo",         command=self._abrir_veiculos)
        menu_cadastro.add_command(label="Locações (Admin)", command=self._abrir_locacoes_admin)

        # ---- Menu Ação ----
        menu_acao = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ação", menu=menu_acao)
        menu_acao.add_command(label="Locar Veículo", command=self._abrir_locacao_usuario)

    def _criar_widgets(self):
        tk.Label(self, text="Sistema de Locação de Veículos",
                 font=("Helvetica", 16, "bold")).pack(pady=30)
        tk.Label(self, text="Utilize o menu acima para acessar as funcionalidades.",
                 font=("Helvetica", 10)).pack()

    def _abrir_veiculos(self):
        from view.veiculo_list_view import JanelaListagemVeiculos
        janela = JanelaListagemVeiculos(self)
        self.wait_window(janela)

    def _abrir_locacoes_admin(self):
        from view.locacao_list_view import JanelaListagemLocacoes
        janela = JanelaListagemLocacoes(self)
        self.wait_window(janela)

    def _abrir_locacao_usuario(self):
        from view.locacao_usuario_view import JanelaLocacaoUsuario
        janela = JanelaLocacaoUsuario(self)
        self.wait_window(janela)
