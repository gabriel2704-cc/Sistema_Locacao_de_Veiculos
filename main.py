import tkinter as tk
from tkinter import ttk, messagebox
from model.veiculo_factory import VeiculoFactory
from views.veiculo_list_view import VeiculoListView 

if __name__ == "__main__":
    root = tk.Tk()
    app = VeiculoListView(root)
    root.mainloop() 