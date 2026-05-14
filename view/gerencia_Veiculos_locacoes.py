
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import tkinter as tk
from tkinter import messagebox, ttk
from control.veiculo_controller import VeiculoController

from view.janela_principal_view import JanelaPrincipal

class JanelaGerenciar(tk.Toplevel):
    
    
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gerencia de Cadastros")
        self.geometry("800x400")
        
        self.controller = VeiculoController()
        
        self.criar_widgets()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Gerencia de Cadastros", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        lbl_titulo1 = tk.Label(self, text="Escolha uma opção", font=("Helvetica", 10, "bold"))
        lbl_titulo1.pack(pady=10)

        # Frame para a Treeview e Scrollbar
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        
        # Frame para os botões de ação
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        btn_gerenciar_veiculo = tk.Button(frame_botoes, text="Gerenciar Veículos", width=15, command=self.abrir_veiculo)
        btn_gerenciar_veiculo.pack(side="left", padx=5)

        btn_gerenciar_locacoes = tk.Button(frame_botoes, text="Gerenciar Locações", width=15, command=self.abrir_locacoes)
        btn_gerenciar_locacoes.pack(side="left", padx=5)


        # Botão Fechar no canto direito
        btn_fechar = tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy)
        btn_fechar.pack(side="right", padx=5)

    def abrir_veiculo(self):
        # Vai reaproveitar a JanelaCadastroVeiculo
        from view.veiculo_list_view import JanelaListagemVeiculos
        janela_cadastro = JanelaListagemVeiculos(self)
        
        # Faz a janela de listagem "esperar" até que a janela de cadastro seja fechada
        self.wait_window(janela_cadastro)



    def abrir_locacoes(self):
        
        from view.locacao_list_view import JanelaListagemLocacoes
        janela_cadastro = JanelaListagemLocacoes(self)
        
        # Faz a janela de listagem "esperar" até que a janela de cadastro seja fechada
        self.wait_window(janela_cadastro)