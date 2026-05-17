import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from control.locacao_controller import LocacaoController
from model.locacao import Locacao, StatusLocacao


class JanelaCadastroLocacao(tk.Toplevel):
    """Formulário de criação/edição de locação (visão Administrador)."""

    # Lista dos valores string dos status para o Combobox
    STATUSES = [s.value for s in StatusLocacao]

    def __init__(self, master=None, locacao_existente: Locacao = None):
        super().__init__(master)
        self.locacao_existente = locacao_existente
        self.controller = LocacaoController()
        self._veiculos_disponiveis = []

        titulo = "Editar Locação" if locacao_existente else "Nova Locação (Admin)"
        self.title(titulo)
        self.geometry("420x420")

        tk.Label(self, text=titulo, font=("Helvetica", 14, "bold")).pack(pady=8)

        # --- Data Início ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=3)
        tk.Label(f, text="Data Início (AAAA-MM-DD):", width=24, anchor="w").pack(side="left")
        self.txt_data_in = tk.Entry(f); self.txt_data_in.pack(side="right", expand=True, fill="x")

        # --- Data Fim ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=3)
        tk.Label(f, text="Data Fim (AAAA-MM-DD):", width=24, anchor="w").pack(side="left")
        self.txt_data_fim = tk.Entry(f); self.txt_data_fim.pack(side="right", expand=True, fill="x")

        # --- Botão buscar veículos ---
        tk.Button(self, text="Buscar Veículos Disponíveis",
                  command=self._buscar_veiculos).pack(pady=4)

        # --- ComboBox veículos ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=3)
        tk.Label(f, text="Veículo:", width=24, anchor="w").pack(side="left")
        self.cb_veiculo = ttk.Combobox(f, state="readonly"); self.cb_veiculo.pack(side="right", expand=True, fill="x")

        # --- Status (somente Admin) ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=3)
        tk.Label(f, text="Status:", width=24, anchor="w").pack(side="left")
        self.cb_status = ttk.Combobox(f, values=self.STATUSES, state="readonly")
        self.cb_status.current(0); self.cb_status.pack(side="right", expand=True, fill="x")

        texto_btn = "Salvar Alterações" if locacao_existente else "Cadastrar Locação"
        tk.Button(self, text=texto_btn, command=self._solicitar_salvar).pack(pady=14)

        # Preenche dados em modo edição
        if locacao_existente:
            self.txt_data_in.insert(0, str(locacao_existente.data_inicio))
            self.txt_data_fim.insert(0, str(locacao_existente.data_fim) if locacao_existente.data_fim else "")
            self.cb_status.set(locacao_existente.status.value)  # <-- .value para exibir string no Combobox
            # mostra placa do veículo atual
            self.cb_veiculo["values"] = [locacao_existente.veiculo.placa]
            self.cb_veiculo.current(0)

    def _parse_data(self, texto: str) -> date:
        return datetime.strptime(texto.strip(), "%Y-%m-%d").date()

    def _buscar_veiculos(self):
        try:
            data_in  = self._parse_data(self.txt_data_in.get())
            data_fim = self._parse_data(self.txt_data_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas. Use o formato AAAA-MM-DD.", parent=self)
            return
        if data_in > data_fim:
            messagebox.showerror("Erro", "Data de início deve ser anterior à data de fim.", parent=self)
            return

        self._veiculos_disponiveis = self.controller.buscar_veiculos_disponiveis(data_in, data_fim)
        # Em modo edição, incluir o veículo atual na lista se não estiver
        if self.locacao_existente:
            placas = [v.placa for v in self._veiculos_disponiveis]
            if self.locacao_existente.veiculo.placa not in placas:
                self._veiculos_disponiveis.insert(0, self.locacao_existente.veiculo)

        if not self._veiculos_disponiveis:
            messagebox.showwarning("Aviso", "Nenhum veículo disponível para o período.", parent=self)
            self.cb_veiculo["values"] = []
            return

        opcoes = [f"{v.placa} — {type(v).__name__} — R$ {v.taxa_diaria:.2f}/dia"
                  for v in self._veiculos_disponiveis]
        self.cb_veiculo["values"] = opcoes
        self.cb_veiculo.current(0)

    def _solicitar_salvar(self):
        try:
            data_in  = self._parse_data(self.txt_data_in.get())
            data_fim = self._parse_data(self.txt_data_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas. Use AAAA-MM-DD.", parent=self)
            return

        if not self.cb_veiculo.get():
            messagebox.showerror("Erro", "Selecione um veículo.", parent=self)
            return

        idx = self.cb_veiculo.current()
        if idx < 0 or idx >= len(self._veiculos_disponiveis):
            placa = self.locacao_existente.veiculo.placa if self.locacao_existente else ""
        else:
            placa = self._veiculos_disponiveis[idx].placa

        # Converte a string selecionada no Combobox de volta para Enum
        status = StatusLocacao(self.cb_status.get())

        if self.locacao_existente:
            sucesso, msg = self.controller.atualizar_locacao(
                self.locacao_existente.loc_id, placa, data_in, data_fim, status)
        else:
            sucesso, msg = self.controller.salvar_locacao(placa, data_in, data_fim, status)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
