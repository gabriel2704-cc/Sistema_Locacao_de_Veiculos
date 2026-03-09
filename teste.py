from datetime import datetime
# Importe suas classes conforme a estrutura do seu projeto
from model.veiculos import Categoria
from model.veiculo_factory import VeiculoFactory
from model.locacoes import Locacao
from model.excecoes_personalizadas import PlacaInvalidaError, DataInvalidaError

def executar_testes():
    print("=== INICIANDO TESTES DO SISTEMA DE LOCAÇÃO ===\n")

    # 1. Teste: Criação via Factory (Sucesso)
    print("--- Teste 1: Criação via Factory ---")
    try:
        carro = VeiculoFactory.criar_veiculo("carro", "ABC1R34", Categoria.ECONOMICO)
        motorhome = VeiculoFactory.criar_veiculo("motorhome", "XYZ9B99", Categoria.EXECUTIVO)
        print(f"Sucesso: {type(carro).__name__} e {type(motorhome).__name__} criados.")
    except Exception as e:
        print(f"Erro inesperado no Teste 1: {e}")

    print("\n--- Teste 2: Cálculo com múltiplos dias ---")
    # 3 dias: 10/05 a 13/05 (3 * 100.0 + 50.0 = 350.0)
    data_in = datetime(2025, 5, 10)
    data_fim = datetime(2025, 5, 13)
    locacao_longa = Locacao(carro, data_in, data_fim)
    valor = locacao_longa.calcular_valor_locacao()
    print(f"Valor para 3 dias de Carro: R$ {valor:.2f} (Esperado: 350.00)")

    print("\n--- Teste 3: Cálculo com devolução no mesmo dia (Mínimo 1 diária) ---")
    data_mesmo_dia = datetime(2025, 5, 10)
    locacao_curta = Locacao(carro, data_mesmo_dia, data_mesmo_dia)
    valor_curto = locacao_curta.calcular_valor_locacao()
    print(f"Valor para devolução no mesmo dia: R$ {valor_curto:.2f} (Esperado: 150.00)")

    print("\n--- Teste 4: Tratamento de tipo inválido na fábrica ---")
    try:
        VeiculoFactory.criar_veiculo("aviao", "ABC1234", Categoria.ECONOMICO)
    except ValueError as e:
        print(f"Erro inesperado no Teste 4: {e}")

    print("\n--- Teste 5: Validação de Datas Inválidas (Data fim < data início) ---")
    try:
        data_errada_fim = datetime(2025, 5, 9)
        locacao_invalida = Locacao(carro, data_in, data_errada_fim)
        locacao_invalida.calcular_valor_locacao()
    except Exception as e:
        print(f"Erro de cronologia capturado -> {e}")

    print("\n--- Teste 6: Validação de Placa Inválida ---")
    try:
        VeiculoFactory.criar_veiculo("carro", "1234567", Categoria.ECONOMICO)
    except Exception as e:
        print(f"Placa Inválida -> {e}")

    print("\n=== TESTES FINALIZADOS ===")

if __name__ == "__main__":
    executar_testes()