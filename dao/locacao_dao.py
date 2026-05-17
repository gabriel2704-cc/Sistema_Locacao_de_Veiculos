import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from model.locacao import Locacao, StatusLocacao
from model.veiculo import VeiculoFactory
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class LocacaoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    # ------------------------------------------------------------------ salvar
    def salvar(self, objeto_locacao: Locacao):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        cursor = None
        try:
            cursor = self.conexao.cursor()
            total_diarias = objeto_locacao.calcular_total_diarias()
            valor_total   = objeto_locacao.calcular_valor_locacao()
            query = """INSERT INTO tb_locacoes
                (loc_veiculo, loc_data_in, loc_data_fim, total_diarias, valor_total, status)
                VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                objeto_locacao.veiculo.placa,
                objeto_locacao.data_inicio,
                objeto_locacao.data_fim,
                total_diarias,
                valor_total,
                objeto_locacao.status.value,  # <-- .value para gravar string no BD
            ))
            self.conexao.commit()
            return True, "Locação cadastrada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao inserir locação: {e}"
        finally:
            if cursor:
                cursor.close()

    # ---------------------------------------------------------------- listar_todos
    def listar_todos(self):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
               SELECT l.loc_id, v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria,
                        l.loc_data_in, l.loc_data_fim, l.total_diarias, l.valor_total, l.status
                FROM tb_locacoes l
                JOIN tb_veiculos v ON v.vei_placa = l.loc_veiculo
                ORDER BY loc_id ASC
            """)
            locacoes = []
            for row in cursor.fetchall():
                loc_id, vei_tipo, vei_placa, vei_cat, vei_taxa, data_in, data_fim, _, _, status = row
                veiculo = VeiculoFactory.criar_veiculo(vei_tipo, vei_placa, vei_cat, float(vei_taxa))
                loc = Locacao(veiculo=veiculo, data_inicio=data_in,
                              data_fim=data_fim,
                              status=StatusLocacao(status),  # <-- converte string → Enum
                              loc_id=loc_id)
                locacoes.append(loc)
            return locacoes
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    # ------------------------------------------------------------------ remover
    def remover(self, id_objeto: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM tb_locacoes WHERE loc_id = %s", (id_objeto,))
            self.conexao.commit()
            return True, "Locação removida com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover locação: {e}"
        finally:
            if cursor:
                cursor.close()

    # ----------------------------------------------------------------- atualizar
    def atualizar(self, objeto_locacao: Locacao):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        cursor = None
        try:
            cursor = self.conexao.cursor()
            total_diarias = objeto_locacao.calcular_total_diarias()
            valor_total   = objeto_locacao.calcular_valor_locacao()
            cursor.execute("""
                UPDATE tb_locacoes
                SET loc_veiculo = %s, loc_data_in = %s, loc_data_fim = %s,
                    total_diarias = %s, valor_total = %s, status = %s
                WHERE loc_id = %s""",
                (objeto_locacao.veiculo.placa,
                 objeto_locacao.data_inicio,
                 objeto_locacao.data_fim,
                 total_diarias,
                 valor_total,
                 objeto_locacao.status.value,  # <-- .value para gravar string no BD
                 objeto_locacao.loc_id))
            self.conexao.commit()
            return True, "Locação atualizada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar locação: {e}"
        finally:
            if cursor:
                cursor.close()

    # --------------------------------------------------------- atualizar_status
    def atualizar_status(self, loc_id: int, novo_status: StatusLocacao,
                         data_inicio: date = None, data_fim: date = None,
                         total_diarias: int = None, valor_total: float = None):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        cursor = None
        try:
            cursor = self.conexao.cursor()
            campos  = ["status = %s"]
            valores = [novo_status.value]  # <-- .value para gravar string no BD
            if data_inicio is not None:
                campos.append("loc_data_in = %s");  valores.append(data_inicio)
            if data_fim is not None:
                campos.append("loc_data_fim = %s"); valores.append(data_fim)
            if total_diarias is not None:
                campos.append("total_diarias = %s"); valores.append(total_diarias)
            if valor_total is not None:
                campos.append("valor_total = %s"); valores.append(valor_total)
            valores.append(loc_id)
            cursor.execute(
                f"UPDATE tb_locacoes SET {', '.join(campos)} WHERE loc_id = %s",
                valores)
            self.conexao.commit()
            return True, "Status atualizado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar status: {e}"
        finally:
            if cursor:
                cursor.close()

    # ------------------------------------------------------- buscar_por_id
    def buscar_por_id(self, loc_id: int):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                SELECT l.loc_id, v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria,
                       l.loc_data_in, l.loc_data_fim, l.total_diarias, l.valor_total, l.status
                FROM tb_locacoes l
                JOIN tb_veiculos v ON v.vei_placa = l.loc_veiculo
                WHERE l.loc_id = %s
            """, (loc_id,))
            row = cursor.fetchone()
            if row:
                loc_id, vei_tipo, vei_placa, vei_cat, vei_taxa, data_in, data_fim, _, _, status = row
                veiculo = VeiculoFactory.criar_veiculo(vei_tipo, vei_placa, vei_cat, float(vei_taxa))
                return Locacao(veiculo=veiculo, data_inicio=data_in,
                               data_fim=data_fim,
                               status=StatusLocacao(status),  # <-- converte string → Enum
                               loc_id=loc_id)
            return None
        except Exception as e:
            print(f"Erro ao buscar locação: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    # ------------------------------------------------ buscar_veiculos_disponiveis
    def buscar_veiculos_disponiveis(self, data_inicio: date, data_fim: date, categoria: str = None):
        """Retorna veículos sem locação ativa que conflite com o período informado."""
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            status_ativos = (StatusLocacao.RESERVADO.value, StatusLocacao.LOCADO.value)
            if categoria:
                cursor.execute("""
                    SELECT v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria
                    FROM tb_veiculos v
                    WHERE v.vei_placa NOT IN (
                        SELECT l.loc_veiculo FROM tb_locacoes l
                        WHERE l.status IN (%s, %s)
                          AND l.loc_data_in  <= %s
                          AND l.loc_data_fim >= %s
                    ) AND v.vei_categoria = %s
                    ORDER BY v.vei_placa
                """, (*status_ativos, data_fim, data_inicio, categoria))
            else:
                cursor.execute("""
                    SELECT v.vei_tipo, v.vei_placa, v.vei_categoria, v.vei_taxa_diaria
                    FROM tb_veiculos v
                    WHERE v.vei_placa NOT IN (
                        SELECT l.loc_veiculo FROM tb_locacoes l
                        WHERE l.status IN (%s, %s)
                          AND l.loc_data_in  <= %s
                          AND l.loc_data_fim >= %s
                    )
                    ORDER BY v.vei_placa
                """, (*status_ativos, data_fim, data_inicio))
            linhas = cursor.fetchall()
            return [VeiculoFactory.criar_veiculo(r[0], r[1], r[2], float(r[3])) for r in linhas]
        except Exception as e:
            print(f"Erro ao buscar veículos disponíveis: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
