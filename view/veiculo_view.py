import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from model.veiculo import VeiculoFactory, Categoria
import view.veiculo_list_view as list_view
from control.veiculo_controller import VeiculoController

class JanelaCadastroVeiculo(tk.Toplevel):
    def __init__(self, master=None, veiculo_existente=None):
        super().__init__(master)
        
        self.veiculo_existente = veiculo_existente
        self.title("Atualizar Veículo" if veiculo_existente else "Cadastro de Novo Veículo")
        
        self.geometry("400x350")
        self.controller = VeiculoController()
        
        
        
        # Label de título
        texto_titulo = "Atualizar Veículo" if veiculo_existente else "Cadastrar Veículo"
        lbl_titulo = tk.Label(self, text=texto_titulo, font=("Helvetica", 16, "bold"))
        
        lbl_titulo.pack(pady=10)

        # Placa
        frame_placa = tk.Frame(self)
        frame_placa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_placa, text="Placa:").pack(side="left")
        self.txt_placa = tk.Entry(frame_placa)
        self.txt_placa.pack(side="right")

        # Tipo
        frame_tipo = tk.Frame(self)
        frame_tipo.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_tipo, text="Tipo (carro/motorhome):").pack(side="left")
        self.txt_tipo = tk.Entry(frame_tipo)
        self.txt_tipo.pack(side="right", expand=True, fill="x")

        # Categoria (ComboBox)
        frame_cat = tk.Frame(self)
        frame_cat.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_cat, text="Categoria:").pack(side="left")
        self.cb_categoria = ttk.Combobox(frame_cat, values=["ECONOMICO", "EXECUTIVO", "LUXO"])
        self.cb_categoria.current(0)
        self.cb_categoria.pack(side="right", expand=True, fill="x")

        # Taxa Diária
        frame_taxa = tk.Frame(self)
        frame_taxa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_taxa, text="Taxa Diária (R$):").pack(side="left")
        self.txt_taxa = tk.Entry(frame_taxa)
        self.txt_taxa.pack(side="right", expand=True, fill="x")

        # Botão Cadastrar \ Atualizar
        # Removido bg/fg para compatibilidade com botões nativos do macOS
        texto_botao = "Atualizar Veículo" if veiculo_existente else "Salvar Veículo"
        btn_cadastrar = tk.Button(self, text=texto_botao, command=self.solicitar_cadastro)
        
        btn_cadastrar.pack(pady=20)
        
        # Preencher dados se for edição
        if self.veiculo_existente:
            self.txt_placa.insert(0, self.veiculo_existente.placa)
            self.txt_placa.config(state="disabled") # Placa não pode ser alterada
            self.txt_tipo.insert(0, self.veiculo_existente.__class__.__name__)
            self.cb_categoria.set(self.veiculo_existente.categoria)
            self.txt_taxa.insert(0, f"{self.veiculo_existente.taxa_diaria}")

    def solicitar_cadastro(self):
        placa = self.txt_placa.get().strip().upper()
        tipo = self.txt_tipo.get().strip()
        categoria = self.cb_categoria.get().strip()
        taxa_str = self.txt_taxa.get().strip()

        if self.veiculo_existente:
            sucesso, msg = self.controller.atualizar_veiculo(placa, tipo, categoria, taxa_str)
        else:
            sucesso, msg = self.controller.salvar_veiculo(placa, tipo, categoria, taxa_str)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)    
            
        self.destroy() # Fecha a janela de cadastro e volta pro menu local
        
