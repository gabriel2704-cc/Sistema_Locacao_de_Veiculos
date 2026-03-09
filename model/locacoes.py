from datetime import datetime
from .veiculos import Veiculo


class Locacao:
    def __init__(self, veiculo: Veiculo, data_in: datetime, data_fim: datetime):
        self.veiculo = veiculo # Isso chama o @veiculo.setter
        self.data_in = data_in  # Atributo simples (sem property)
        self.data_fim = data_fim # Atributo simples (sem property)

    @property
    def veiculo(self):
        return self.__veiculo
    
    @veiculo.setter
    def veiculo(self, obj):
        if obj is not None:
            self.__veiculo = obj
        else:
            raise Exception("Objeto veiculo obrigatório!!")
    
    def calcular_valor_locacao(self) -> float:
        
        if self.data_fim < self.data_in:
            raise Exception("Data final não pode ser menor que a data inicial.")

        dias = (self.data_fim - self.data_in).days

        if dias == 0:
            dias = 1

        total_diarias = dias * self.__veiculo.taxa_diaria 
        total = total_diarias + self.__veiculo.valor_seguro

        return total