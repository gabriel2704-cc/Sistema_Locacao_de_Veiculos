from datetime import date
from dao.locacao_dao import LocacaoDAO
from dao.veiculo_dao import VeiculoDAO
from model.locacao import Locacao, StatusLocacao
from model.veiculo import VeiculoFactory, Categoria
from model.LocacaoStrategy import CalculoPadraoStrategy


class LocacaoController:
    def __init__(self):
        self.locacao_dao = LocacaoDAO()
        self.veiculo_dao = VeiculoDAO()

    # ------------------------------------------------------------ salvar
    def salvar_locacao(self, placa: str, data_inicio: date,
                       data_fim: date, status: StatusLocacao = StatusLocacao.RESERVADO):
        if not placa or not data_inicio or not data_fim:
            return False, "Preencha todos os campos obrigatórios"
        if data_inicio > data_fim:
            return False, "Data de início deve ser anterior ou igual à data de fim"
        try:
            veiculo = self.veiculo_dao.buscar_por_placa(placa)
            if not veiculo:
                return False, f"Veículo com placa {placa} não encontrado"
            loc = Locacao(veiculo=veiculo, data_inicio=data_inicio,
                          data_fim=data_fim, status=status)
            return self.locacao_dao.salvar(loc)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    # ----------------------------------------------------------- listar
    def listar_locacoes(self):
        try:
            return self.locacao_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return []

    # ---------------------------------------------------------- remover
    def remover_locacao(self, loc_id: int):
        if not loc_id:
            return False, "ID não informado"
        try:
            return self.locacao_dao.remover(loc_id)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    # --------------------------------------------------------- atualizar (admin)
    def atualizar_locacao(self, loc_id: int, placa: str,
                          data_inicio: date, data_fim: date, status: StatusLocacao):
        if not placa or not data_inicio or not data_fim:
            return False, "Preencha todos os campos"
        if data_inicio > data_fim:
            return False, "Data de início deve ser anterior ou igual à data de fim"
        try:
            veiculo = self.veiculo_dao.buscar_por_placa(placa)
            if not veiculo:
                return False, f"Veículo {placa} não encontrado"
            loc = Locacao(veiculo=veiculo, data_inicio=data_inicio,
                          data_fim=data_fim, status=status, loc_id=loc_id)
            return self.locacao_dao.atualizar(loc)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    # ----------------------------------------------------------- buscar
    def buscar_por_id(self, loc_id: int):
        try:
            return self.locacao_dao.buscar_por_id(loc_id)
        except Exception as e:
            print(f"Erro ao buscar locação: {e}")
            return None

    # ------------------------------------------------------------ locar
    def locar(self, loc_id: int):
        loc = self.locacao_dao.buscar_por_id(loc_id)
        if not loc:
            return False, "Locação não encontrada"
        if loc.status != StatusLocacao.RESERVADO:
            return False, "Somente locações com status 'reservado' podem ser locadas"
        hoje = date.today()
        nova_data_inicio = hoje if loc.data_inicio != hoje else loc.data_inicio
        return self.locacao_dao.atualizar_status(
            loc_id, StatusLocacao.LOCADO, data_inicio=nova_data_inicio)

    # ---------------------------------------------------------- devolver
    def devolver(self, loc_id: int):
        loc = self.locacao_dao.buscar_por_id(loc_id)
        if not loc:
            return False, "Locação não encontrada"
        if loc.status != StatusLocacao.LOCADO:
            return False, "Somente locações com status 'locado' podem ser devolvidas"
        hoje = date.today()
        if loc.data_inicio >= hoje:
            return False, "A data de início deve ser anterior à data atual para realizar a devolução"
        loc.data_fim = hoje
        total = loc.calcular_total_diarias()
        valor = loc.calcular_valor_locacao()
        sucesso, msg = self.locacao_dao.atualizar_status(
            loc_id, StatusLocacao.DEVOLVIDO,
            data_fim=hoje, total_diarias=total, valor_total=valor)
        if sucesso:
            info = (f"Data de início: {loc.data_inicio}\n"
                    f"Data de devolução: {hoje}\n"
                    f"Número de diárias: {total}\n"
                    f"Valor total: R$ {valor:.2f}")
            return True, info
        return False, msg

    # ---------------------------------------------------------- cancelar
    def cancelar(self, loc_id: int):
        loc = self.locacao_dao.buscar_por_id(loc_id)
        if not loc:
            return False, "Locação não encontrada"
        if loc.status != StatusLocacao.RESERVADO:
            return False, "Somente locações com status 'reservado' podem ser canceladas"
        return self.locacao_dao.atualizar_status(loc_id, StatusLocacao.CANCELADO)

    # ----------------------------------------- buscar_veiculos_disponiveis
    def buscar_veiculos_disponiveis(self, data_inicio: date, data_fim: date, categoria: str = None):
        try:
            return self.locacao_dao.buscar_veiculos_disponiveis(data_inicio, data_fim, categoria)
        except Exception as e:
            print(f"Erro ao buscar veículos disponíveis: {e}")
            return []

    # ----------------------------------------- listar_todos_veiculos
    def listar_veiculos(self):
        try:
            return self.veiculo_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return []
