import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from control.locacao_controller import LocacaoController
from model.locacao import Locacao, StatusLocacao


class JanelaNovaReserva(tk.Toplevel):
    """Formulário para o usuário criar uma nova reserva com validações de negócio."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Nova Reserva")
        self.geometry("420x380")
        self.controller = LocacaoController()
        self._veiculos_disponiveis = []
        self._criar_widgets()

    def _criar_widgets(self):
        tk.Label(self, text="Nova Reserva", font=("Helvetica", 14, "bold")).pack(pady=8)

        # --- Data Início ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=4)
        tk.Label(f, text="Data Início (AAAA-MM-DD):", width=25, anchor="w").pack(side="left")
        self.txt_data_in = tk.Entry(f)
        self.txt_data_in.insert(0, str(date.today()))
        self.txt_data_in.pack(side="right", expand=True, fill="x")

        # --- Data Fim ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=4)
        tk.Label(f, text="Data Fim (AAAA-MM-DD):", width=25, anchor="w").pack(side="left")
        self.txt_data_fim = tk.Entry(f); self.txt_data_fim.pack(side="right", expand=True, fill="x")

        # --- Categoria (filtro) ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=4)
        tk.Label(f, text="Categoria (opcional):", width=25, anchor="w").pack(side="left")
        self.cb_categoria = ttk.Combobox(f, values=["", "ECONOMICO", "EXECUTIVO"], state="readonly")
        self.cb_categoria.current(0)
        self.cb_categoria.pack(side="right", expand=True, fill="x")

        tk.Button(self, text="Buscar Veículos Disponíveis",
                  command=self._buscar_veiculos).pack(pady=6)

        # --- ComboBox veículos ---
        f = tk.Frame(self); f.pack(fill="x", padx=20, pady=4)
        tk.Label(f, text="Veículo disponível:", width=25, anchor="w").pack(side="left")
        self.cb_veiculo = ttk.Combobox(f, state="readonly")
        self.cb_veiculo.pack(side="right", expand=True, fill="x")

        tk.Button(self, text="Confirmar Reserva",
                  command=self._confirmar).pack(pady=12)

    def _parse_data(self, texto: str) -> date:
        return datetime.strptime(texto.strip(), "%Y-%m-%d").date()

    def _buscar_veiculos(self):
        try:
            data_in  = self._parse_data(self.txt_data_in.get())
            data_fim = self._parse_data(self.txt_data_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas. Use o formato AAAA-MM-DD.", parent=self)
            return
        if data_in < date.today():
            messagebox.showerror("Erro", "A data de início não pode ser no passado.", parent=self)
            return
        if data_in > data_fim:
            messagebox.showerror("Erro", "Data de início deve ser anterior à data de fim.", parent=self)
            return

        categoria = self.cb_categoria.get().strip() or None
        self._veiculos_disponiveis = self.controller.buscar_veiculos_disponiveis(data_in, data_fim, categoria)

        if not self._veiculos_disponiveis:
            messagebox.showwarning("Aviso", "Nenhum veículo disponível para o período/categoria.", parent=self)
            self.cb_veiculo["values"] = []
            return

        opcoes = [f"{v.placa} — {type(v).__name__} — {v.categoria.name} — R$ {v.taxa_diaria:.2f}/dia"
                  for v in self._veiculos_disponiveis]
        self.cb_veiculo["values"] = opcoes
        self.cb_veiculo.current(0)

    def _confirmar(self):
        if not self._veiculos_disponiveis or self.cb_veiculo.current() < 0:
            messagebox.showerror("Erro", "Busque e selecione um veículo disponível.", parent=self)
            return
        try:
            data_in  = self._parse_data(self.txt_data_in.get())
            data_fim = self._parse_data(self.txt_data_fim.get())
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas.", parent=self)
            return

        veiculo = self._veiculos_disponiveis[self.cb_veiculo.current()]
        sucesso, msg = self.controller.salvar_locacao(
            veiculo.placa, data_in, data_fim, StatusLocacao.RESERVADO)

        if sucesso:
            messagebox.showinfo("Sucesso", "Reserva criada com sucesso!", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
