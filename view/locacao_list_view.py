import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from control.locacao_controller import LocacaoController
from model.locacao import Locacao, StatusLocacao


## Toda aplicação Tkinter só deve possuir uma única janela principal raiz (tk.Tk()). 
# Se tentar dar tk.Tk() em outra tela, vai abrir outra instância na memória 
# e pode dar diversos problemas gráficos e falhas de variáveis.

# No caso do seu projeto da Locadora: As telas herdam de tk.Toplevel (class JanelaCadastroVeiculo(tk.Toplevel):) 
# porque isso permite tratá-las de um jeito modular (como um "Popup").

## O tk.Toplevel é uma classe do Tkinter usada para criar Janelas Secundárias que rodam 
# "por cima" de uma tela principal (que é geralmente o tk.Tk()).
class JanelaListagemLocacoes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Locações Cadastradas")
        self.geometry("800x400")
        
        self.controller = LocacaoController()
        
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Locações Cadastradas", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Frame para a Treeview e Scrollbar
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")


        # Treeview (Tabela)
        colunas = ("ID", "Veículo", "Data Início", "Data Fim", "Total diarias", "Valor Total", "Status")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        
        # Configurar cabeçalhos e colunas
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        # Frame para os botões de ação
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        btn_novo = tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo)
        btn_novo.pack(side="left", padx=5)

        btn_editar = tk.Button(frame_botoes, text="Editar", width=15, command=self.abrir_editar)
        btn_editar.pack(side="left", padx=5)
        
        btn_info = tk.Button(frame_botoes, text="Ver Informações", width=15, command=self.ver_detalhes)
        btn_info.pack(side="left", padx=5)

        btn_remover = tk.Button(frame_botoes, text="Remover", width=10, command=self.remover_locacao)
        btn_remover.pack(side="left", padx=5)

        # Botão Fechar no canto direito
        btn_fechar = tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy)
        btn_fechar.pack(side="right", padx=5)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        locacoes = self.controller.listar_locacoes()
        for loc in locacoes:
            valor_fmt = f"R$ {loc.calcular_valor_locacao():.2f}" if loc.data_fim else "-"
            self.tree.insert("", "end", values=(
                loc.loc_id,
                loc.veiculo.placa,
                loc.data_inicio,
                loc.data_fim if loc.data_fim else "-",
                loc.calcular_total_diarias() if loc.data_fim else "-",
                valor_fmt,
                loc.status.value,  # <-- .value para exibir string na tabela
            ))

    def _get_loc_id_selecionado(self, acao="selecionar"):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", f"Selecione uma locação para {acao}.", parent=self)
            return None
        return self.tree.item(sel[0])["values"][0]

    def abrir_novo(self):
        from view.locacao_view import JanelaCadastroLocacao
        janela = JanelaCadastroLocacao(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        loc_id = self._get_loc_id_selecionado("editar")
        if loc_id is None:
            return
        loc = self.controller.buscar_por_id(loc_id)
        if not loc:
            messagebox.showerror("Erro", "Locação não encontrada.", parent=self)
            return
        from view.locacao_view import JanelaCadastroLocacao
        janela = JanelaCadastroLocacao(self, locacao_existente=loc)
        self.wait_window(janela)
        self.carregar_dados()

    def ver_detalhes(self):
        loc_id = self._get_loc_id_selecionado("visualizar")
        if loc_id is None:
            return
        loc = self.controller.buscar_por_id(loc_id)
        if not loc:
            messagebox.showerror("Erro", "Locação não encontrada.", parent=self)
            return
        info = _montar_detalhes(loc)
        messagebox.showinfo("Detalhes da Locação", info, parent=self)

    def remover_locacao(self):
        loc_id = self._get_loc_id_selecionado("remover")
        if loc_id is None:
            return
        if not messagebox.askyesno("Confirmar", f"Remover locação #{loc_id}?", parent=self):
            return
        sucesso, msg = self.controller.remover_locacao(loc_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)


# ----------------------------------------------------------------- helper
def _montar_detalhes(loc: Locacao) -> str:
    status = loc.status  # agora é StatusLocacao (Enum)
    if status == StatusLocacao.DEVOLVIDO:
        dias  = loc.calcular_total_diarias()
        valor = loc.calcular_valor_locacao()
        return (f"Status: {status.value.upper()}\n"
                f"Veículo: {loc.veiculo.placa}\n"
                f"Data de início: {loc.data_inicio}\n"
                f"Data de devolução: {loc.data_fim}\n"
                f"Número de diárias: {dias}\n"
                f"Valor total: R$ {valor:.2f}")
    elif status == StatusLocacao.CANCELADO:
        return (f"Status: {status.value.upper()}\n"
                f"Veículo: {loc.veiculo.placa}\n"
                f"Data de início: {loc.data_inicio}\n"
                f"Data fim prevista: {loc.data_fim}\n"
                f"A locação foi cancelada.")
    else:  # RESERVADO ou LOCADO
        valor_est = loc.calcular_valor_locacao()
        return (f"Status: {status.value.upper()}\n"
                f"Veículo: {loc.veiculo.placa}\n"
                f"Data de início: {loc.data_inicio}\n"
                f"Data fim prevista: {loc.data_fim}\n"
                f"Valor estimado: R$ {valor_est:.2f}")