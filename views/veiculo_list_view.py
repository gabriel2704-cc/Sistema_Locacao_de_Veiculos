import tkinter as tk
from tkinter import ttk, messagebox
from model.veiculo_factory import VeiculoFactory 
from model.veiculos import Categoria, Veiculo
from model.excecoes_personalizadas import PlacaInvalidaError

class VeiculoListView:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Painel Principal - Locadora de Veículos") 
        self.janela.geometry("600x400")
        self.veiculos_na_memoria = {} # Dicionário para mapear ID -> Objeto Veiculo

        
        lbl_titulo = tk.Label(self.janela, text="Veículos Cadastrados", font=("Arial", 14, "bold"), pady=10)
        lbl_titulo.pack()

        # Criando a Tabela
        self.tree = ttk.Treeview(self.janela, columns=("Placa", "Tipo", "Categoria", "Taxa"), show='headings')
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Taxa", text="Taxa Diária")
        self.tree.pack(expand=True, fill="both", padx=10) # garante a responsividade da tabela

        #  BOTÕES
        frame_botoes = tk.Frame(self.janela) 
        frame_botoes.pack(pady=20)

        self.btn_novo = tk.Button(frame_botoes, text="Novo", command=self.abrir_cadastro, width=15) 
        self.btn_novo.pack(side="left", padx=5)

        self.btn_info = tk.Button(frame_botoes, text="Ver Informações", command=self.exibir_info, width=15) 
        self.btn_info.pack(side="left", padx=5)

        self.btn_remover = tk.Button(frame_botoes, text="Remover", command=self.remover_veiculo, width=15) 
        self.btn_remover.pack(side="left", padx=5)

   
    def abrir_cadastro(self):
        self.janela_cad = tk.Toplevel(self.janela) 
        self.janela_cad.title("Cadastro de Veículo")
        self.janela_cad.geometry("300x350")
        self.janela_cad.grab_set() # Torna a janela modal

        
        tk.Label(self.janela_cad, text="Placa:").pack(pady=5)
        self.ent_placa = tk.Entry(self.janela_cad)
        self.ent_placa.pack()

        tk.Label(self.janela_cad, text="Tipo:").pack(pady=5)
        self.cb_tipo = ttk.Combobox(self.janela_cad, values=["Carro", "Motorhome"], state="readonly")
        self.cb_tipo.pack()

        tk.Label(self.janela_cad, text="Categoria:").pack(pady=5)
        self.cb_cat = ttk.Combobox(self.janela_cad, values=["ECONOMICO", "EXECUTIVO"], state="readonly")
        self.cb_cat.pack()

        tk.Label(self.janela_cad, text="Taxa Diária:").pack(pady=5)
        self.ent_taxa = tk.Entry(self.janela_cad)
        self.ent_taxa.pack()

        btn_salvar = tk.Button(self.janela_cad, text="Salvar", command=self.processar_cadastro, bg="green", fg="white")
        btn_salvar.pack(pady=20)

    def processar_cadastro(self):
        placa = self.ent_placa.get()
        tipo = self.cb_tipo.get()
        cat = self.cb_cat.get()
        taxa = self.ent_taxa.get()

        # Dentro do método processar_cadastro:
        cat_selecionada = self.cb_cat.get() 
        # Converte a string do Combobox para o objeto Enum correspondente
        categoria_enum = Categoria[cat_selecionada]

        # Validação Simples (Passo 2.3.2) 
        if not all([placa, tipo, cat, taxa]):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        try:
            taxa_float = float(taxa)
            # Chama a factory passando o Enum e a taxa convertida
            novo_v = VeiculoFactory.criar_veiculo(tipo, placa, taxa_float, categoria_enum)
    
            # Se chegou aqui, a placa é válida! (O Model retornou True internamente)
            id_linha = self.tree.insert("", "end", values=(placa, tipo, cat_selecionada, f"R$ {taxa_float:.2f}"))
            self.veiculos_na_memoria[id_linha] = novo_v # Armazena o objeto real no dicionário usando o ID da linha como chave

            messagebox.showinfo("Sucesso", "Veículo cadastrado!")
            
            self.janela_cad.destroy()
        except PlacaInvalidaError as e:
            # Exibe a mensagem exata que você definiu no Model (ex: "Os primeiros 3 caracteres...")
            messagebox.showerror("Erro de Placa", str(e))
        except ValueError:
            messagebox.showerror("Erro de Valor", "A taxa diária deve ser um número!") 

    def exibir_info(self):
        item_selecionado = self.tree.selection() # Retorna uma tupla de IDs

        if item_selecionado:
            id_da_linha = item_selecionado[0]
            # Recupera o objeto real do dicionário
            veiculo_obj = self.veiculos_na_memoria[id_da_linha]
             # Agora sim você chama o método do MODEL 
            mensagem = veiculo_obj.exibir_dados() 
            messagebox.showinfo("Detalhes do Veículo", mensagem)
        else:
            messagebox.showwarning("Aviso", "Selecione um veículo na lista!")

    def remover_veiculo(self):
        selecionado = self.tree.selection()
        if selecionado:
            id_da_linha = selecionado[0]
            self.tree.delete(id_da_linha)
            
            if id_da_linha in self.veiculos_na_memoria:
                del self.veiculos_na_memoria[id_da_linha] 
            messagebox.showinfo("Remoção", "Veículo removido com sucesso!") 
        else:
            messagebox.showwarning("Aviso", "Selecione um veículo para remover!")
