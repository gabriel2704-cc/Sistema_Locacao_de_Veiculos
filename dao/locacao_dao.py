import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.locacao import *
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO

class LocacaoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
        
    def salvar(self, objeto_locacao:Locacao):
        if not self.conexao:
            raise Exception("Sem conexão com o BD")
        
        try:
            cursor = self.conexao.cursor()
            query = """INSERT INTO tb_locacoes 
            (loc_veiculo, loc_data_in, loc_data_fim, total_diarias, valor_total) 
            VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (objeto_locacao.loc_veicullo,
                                   objeto_locacao.data_inicio,
                                   objeto_locacao.data_fim,
                                   objeto_locacao.total_diarias,
                                   objeto_locacao.valor_total,
                                   objeto_locacao.status.value))
                                   
            self.conexao.commit()
            return True, "Locação cadastrada com sucesso"
                                
        except Exception as e:
            print(f"Erro ao inserir locação: {objeto_locacao.placa}: {e}")
            self.conexao.rollback()
            return False, f"Erro ao inserir locação: {objeto_locacao.placa}: {e}"
        
        finally:
            if cursor:
                cursor.close()
                
    def listar_todos(self):
        if not self.conexao:
            return []
        
        try:
            cursor = self.conexao.cursor()
            query = """SELECT loc_veiculo, loc_data_in, loc_data_fim, total_diarias, valor_total
            FROM tb_locacoes
            """
            cursor.execute(query)
            linhas = cursor.fetchall()
            veiculos = []
            for cada_linha in linhas:
                obj = Locacao.criar_locacao(cada_linha[0], cada_linha[1], cada_linha[2], float(cada_linha[3]), float(cada_linha[4]))
                veiculos.append(obj)
            
            return veiculos
                                
        except Exception as e:
            print(f"Erro ao buscar veículos: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
        
        
    
    def remover(self, id_objeto: str):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_veiculos WHERE vei_placa = %s"
            cursor.execute(query, (id_objeto,))
            self.conexao.commit()
            return True, "Veículo removido com sucesso"
            
        except Exception as e:
            print(f"Erro ao remover veículo: {id_objeto}. Erro: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover veículo: {id_objeto}: {e}"
        
        finally:
            if cursor:
                cursor.close()
    
    def atualizar(self, objeto: Veiculo):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_veiculos 
                    SET vei_categoria = %s, vei_taxa_diaria = %s, vei_estado_atual = %s, vei_tipo = %s 
                    WHERE vei_placa = %s"""
            cursor.execute(query, (objeto.categoria.value,
                                   objeto.taxa_diaria,
                                   objeto.estado_atual.__class__.__name__,
                                   objeto.__class__.__name__,
                                   objeto.placa))
            self.conexao.commit()
            return True, "Veículo atualizado com sucesso"
            
        except Exception as e:
            print(f"Erro ao atualizar veículo: {objeto.placa}: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar veículo: {objeto.placa}: {e}"
        
        finally:
            if cursor:
                cursor.close()
    
    def buscar_por_placa(self, placa: str):
        if not self.conexao:
            return []
        
        try:
            cursor = self.conexao.cursor()
            query = """select vei_tipo, vei_placa, vei_categoria, vei_taxa_diaria
                    FROM tb_veiculos
                    WHERE vei_placa = %s"""
            cursor.execute(query, (placa,))
            linha = cursor.fetchone()
            
            if linha: 
                return VeiculoFactory.criar_veiculo(linha[0], linha[1], linha[2], linha[3])
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar veículo: {placa}. Erro: {e}")
        
        finally:
            if cursor:
                cursor.close()