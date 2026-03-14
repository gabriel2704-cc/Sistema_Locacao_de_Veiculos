from .estados_veiculo import DisponivelState
from abc import ABC, abstractmethod
from enum import Enum
from .excecoes_personalizadas import PlacaInvalidaError

class Categoria(Enum):
    ECONOMICO = "ECONOMICO"
    EXECUTIVO = "EXECUTIVO"
    
    
class Veiculo(ABC):
    def __init__(self, placa: str, taxa_diaria: float, categoria: Categoria = Categoria.ECONOMICO):
        self.placa = placa
        self.categoria = categoria
        self.taxa_diaria = taxa_diaria
        self.estado_atual = DisponivelState(self)
    
    @property
    def estado_atual(self):
        return self._estado_atual

    @estado_atual.setter
    def estado_atual(self, novo_estado):
        # Usado pelas classes de estado para mudar o ponteiro do carro
        self._estado_atual = novo_estado
        
    # DELEGAÇÃO:
    def tentar_alugar(self):
        self.estado_atual.alugar()
        
    def tentar_devolver(self):
        self.estado_atual.devolver()
        
    def reter_na_frota_pra_conserto(self):
        self.estado_atual.enviar_manutencao()
    #--------------------------------------------#
    @property
    def placa(self):
        return self.__placa
    
    @placa.setter
    def placa(self, placa):
        if(self.valida_placa(placa)):
            self.__placa = placa
     #--------------------------------------------#
    @property
    def taxa_diaria(self):
        return self.__taxa_diaria
    
    @taxa_diaria.setter
    def taxa_diaria(self, taxa_diaria):
        self.__taxa_diaria = taxa_diaria
     #--------------------------------------------#
        
    def valida_placa(self, placa):
        placa = placa.strip().replace("-", "").upper()
        if (len(placa) != 7):
            raise PlacaInvalidaError("Placa inválida! Placa deve conter 7 caracteres")
        else:
            if not placa[0:3].isalpha():
                raise PlacaInvalidaError(f" {placa} Placa inválida! Os primeiros 3 caracteres devem ser letras")
            else:
                if not placa[3].isdigit() or not placa[5:7].isdigit():
                    raise PlacaInvalidaError(f" {placa} Placa Inválida! O 4º, 6º e 7º caracteres devem ser números")
                elif not placa[4].isalnum():
                    raise PlacaInvalidaError(f" {placa} Placa Inválida!! O 5º caracter deve ser uma letra ou número")
                else:
                    print(f"Placa {placa} válida!!") 
                    return True
                    
      #--------------------------------------------#   
class Carro(Veiculo):
    def __init__(self, placa:str, taxa_diaria:float, categoria:Categoria=Categoria.ECONOMICO):
        super().__init__(placa, taxa_diaria, categoria=categoria)
        self.valor_seguro = 50
    
class Motorhome(Veiculo):
    def __init__(self, placa:str, taxa_diaria:float, categoria:Categoria=Categoria.ECONOMICO):
        super().__init__(placa, taxa_diaria, categoria=categoria)
        self.valor_seguro = 120