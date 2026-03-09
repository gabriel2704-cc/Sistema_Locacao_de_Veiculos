from .veiculos import Carro, Motorhome, Categoria


class VeiculoFactory:
    @staticmethod
    def criar_veiculo(tipo: str, placa: str, categoria: Categoria):
        """
        Cria uma instância de Veiculo baseada no tipo fornecido.
        Define taxas diárias fixas de exemplo para cada tipo.
        """
        tipo = tipo.lower().strip()
        
        if tipo == "carro":
            # Exemplo: Carros têm taxa_diaria de 100.0
            return Carro(placa=placa, taxa_diaria=100.0, categoria=categoria)
        
        elif tipo == "motorhome":
            # Exemplo: Motorhomes têm taxa_diaria de 250.0
            return Motorhome(placa=placa, taxa_diaria=250.0, categoria=categoria)
        
        else:
            raise ValueError(f"Tipo de veículo '{tipo}' é inválido. Escolha 'carro' ou 'motorhome'.")

