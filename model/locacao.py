from datetime import date, datetime
from enum import Enum
from .veiculo import Veiculo
from .ExcecoesPersonalizadas import DataInvalidaError
from .LocacaoStrategy import *


class StatusLocacao(Enum):
    RESERVADO  = "reservado"
    LOCADO     = "locado"
    DEVOLVIDO  = "devolvido"
    CANCELADO  = "cancelado"


class Locacao:

    def __init__(self, veiculo: Veiculo, data_inicio: date = None,
                 data_fim: date = None,
                 estrategia: CalculoLocacaoStrategy = None,
                 status: StatusLocacao = None,
                 loc_id: int = None):

        self.__data_inicio = None
        self.__data_fim    = None

        self.loc_id     = loc_id
        self.veiculo    = veiculo
        self.estrategia = estrategia if estrategia is not None else CalculoPadraoStrategy()
        self.status     = status if status is not None else StatusLocacao.RESERVADO

        self.data_inicio = data_inicio if data_inicio is not None else datetime.now().date()
        self.data_fim    = data_fim

    # ------------------------------------------------------------------ veiculo
    @property
    def veiculo(self):
        return self.__veiculo

    @veiculo.setter
    def veiculo(self, obj: Veiculo):
        if obj is not None:
            self.__veiculo = obj
        else:
            raise Exception("Objeto Veículo obrigatório!!!")

    # ---------------------------------------------------------------- data_inicio
    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data_inicio: date):
        if data_inicio is None:
            raise DataInvalidaError("Data de início é obrigatória!")
        if self.__data_fim is not None and data_inicio > self.__data_fim:
            raise DataInvalidaError("Data de início não pode ser posterior à data de fim.")
        self.__data_inicio = data_inicio

    # ------------------------------------------------------------------ data_fim
    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data_fim: date):
        if data_fim is not None and self.__data_inicio is not None and self.__data_inicio > data_fim:
            raise DataInvalidaError("Data de início não pode ser posterior à data de fim.")
        self.__data_fim = data_fim

    # -------------------------------------------------------- calcular_valor
    def calcular_valor_locacao(self) -> float:
        data_ref = self.__data_fim if self.__data_fim is not None else date.today()
        dias = (data_ref - self.__data_inicio).days
        if dias <= 0:
            dias = 1
        valor_total = self.estrategia.calcular_diarias(self.veiculo, dias)
        return float(valor_total)

    # -------------------------------------------------------- total_diarias
    def calcular_total_diarias(self) -> int:
        data_ref = self.__data_fim if self.__data_fim is not None else date.today()
        dias = (data_ref - self.__data_inicio).days
        return max(dias, 1)