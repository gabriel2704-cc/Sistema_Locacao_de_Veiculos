import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.veiculo_factory import VeiculoFactory
from model.veiculos import *
from dao.veiculo_dao import VeiculoDAO

dao = VeiculoDAO()



novo_carro = VeiculoFactory.criar_veiculo("Carro", "ABC1234", Categoria.ECONOMICO, 150.00)
dao.salvar(novo_carro)


lista_veiculos = dao.listar_todos()
print(f"Total de veículos cadastrados: {len(lista_veiculos)}")

for obj in lista_veiculos:
    print(obj.exibir_dados())