import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from control.locacao_controller import LocacaoController
from model.locacao import Locacao, StatusLocacao
from view.locacao_list_view import _montar_detalhes


class JanelaLocacaoUsuario(tk.Toplevel):
    """Tela do Usuário da Locadora — listagem + ações operacionais."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Locar Veículo — Usuário")
        self.geometry("900x470")
        self.controller = LocacaoController()
        self._criar_widgets()
        self.carregar_dados()

    def _criar_widgets(self):
        tk.Label(self, text="Locações — Visão Usuário",
                 font=("Helvetica", 14, "bold")).pack(pady=8)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=15, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Veículo", "Data Início", "Data Fim", "Status")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings",
                                 yscrollcommand=scrollbar.set)
        larguras = {"ID": 50, "Veículo": 100, "Data Início": 110,
                    "Data Fim": 110, "Status": 100}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras.get(col, 100))
        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<<TreeviewSelect>>", self._atualizar_botoes)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=15, pady=5)

        self.btn_nova    = tk.Button(frame_botoes, text="Nova Reserva",  width=14, command=self._nova_reserva)
        self.btn_locar   = tk.Button(frame_botoes, text="Locar",         width=10, command=self._locar)
        self.btn_devolver= tk.Button(frame_botoes, text="Devolver",      width=10, command=self._devolver)
        self.btn_cancelar= tk.Button(frame_botoes, text="Cancelar",      width=10, command=self._cancelar)
        self.btn_detalhe = tk.Button(frame_botoes, text="Ver Detalhes",  width=14, command=self._ver_detalhes)

        self.btn_nova.pack(side="left", padx=4)
        self.btn_locar.pack(side="left", padx=4)
        self.btn_devolver.pack(side="left", padx=4)
        self.btn_cancelar.pack(side="left", padx=4)
        self.btn_detalhe.pack(side="left", padx=4)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=4)

        self._atualizar_botoes()

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        locacoes = self.controller.listar_locacoes()
        for loc in locacoes:
            self.tree.insert("", "end", values=(
                loc.loc_id,
                loc.veiculo.placa,
                loc.data_inicio,
                loc.data_fim if loc.data_fim else "-",
                loc.status.value,  # <-- .value para exibir string na tabela
            ))
        self._atualizar_botoes()

    def _atualizar_botoes(self, event=None):
        sel = self.tree.selection()
        if not sel:
            self.btn_locar.config(state="disabled")
            self.btn_devolver.config(state="disabled")
            self.btn_cancelar.config(state="disabled")
            self.btn_detalhe.config(state="disabled")
            return

        # status na Treeview é string (.value), compara com .value do Enum
        status_str = self.tree.item(sel[0])["values"][4]
        self.btn_detalhe.config(state="normal")
        self.btn_locar.config(   state="normal" if status_str == StatusLocacao.RESERVADO.value else "disabled")
        self.btn_devolver.config( state="normal" if status_str == StatusLocacao.LOCADO.value    else "disabled")
        self.btn_cancelar.config( state="normal" if status_str == StatusLocacao.RESERVADO.value else "disabled")

    def _get_loc_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma locação.", parent=self)
            return None
        return self.tree.item(sel[0])["values"][0]

    def _nova_reserva(self):
        from view.janela_nova_reserva_view import JanelaNovaReserva
        janela = JanelaNovaReserva(self)
        self.wait_window(janela)
        self.carregar_dados()

    def _locar(self):
        loc_id = self._get_loc_id()
        if loc_id is None:
            return
        sucesso, msg = self.controller.locar(loc_id)
        if sucesso:
            messagebox.showinfo("Sucesso", "Veículo locado com sucesso!", parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)
        self.carregar_dados()

    def _devolver(self):
        loc_id = self._get_loc_id()
        if loc_id is None:
            return
        sucesso, msg = self.controller.devolver(loc_id)
        if sucesso:
            messagebox.showinfo("Devolução Concluída", msg, parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)
        self.carregar_dados()

    def _cancelar(self):
        loc_id = self._get_loc_id()
        if loc_id is None:
            return
        if not messagebox.askyesno("Confirmar", "Cancelar esta reserva?", parent=self):
            return
        sucesso, msg = self.controller.cancelar(loc_id)
        if sucesso:
            messagebox.showinfo("Cancelado", "Reserva cancelada com sucesso.", parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)
        self.carregar_dados()

    def _ver_detalhes(self):
        loc_id = self._get_loc_id()
        if loc_id is None:
            return
        loc = self.controller.buscar_por_id(loc_id)
        if not loc:
            messagebox.showerror("Erro", "Locação não encontrada.", parent=self)
            return
        messagebox.showinfo("Detalhes", _montar_detalhes(loc), parent=self)
