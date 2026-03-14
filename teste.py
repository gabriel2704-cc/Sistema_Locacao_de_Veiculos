from datetime import date, datetime
# Importe suas classes conforme a estrutura do seu projeto
from model.veiculos import Categoria
from model.veiculo_factory import VeiculoFactory
from model.locacoes import Locacao
from model.excecoes_personalizadas import PlacaInvalidaError, DataInvalidaError
from model.calcular_valor_locacao import CalculoPadraoStrategy, CalculoVIPStrategy
from model.estados_veiculo import DisponivelState, AlugadoState, ManutencaoState

def executar_testes():
    print("=== INICIANDO TESTES DO SISTEMA DE LOCAÇÃO ===\n")

    # 1. Teste: Criação via Factory (Sucesso)
    print("--- Teste 1: Criação via Factory ---")
    try:
        carro = VeiculoFactory.criar_veiculo("carro",taxa_diaria=100.0, placa="ABC1R34", categoria=Categoria.ECONOMICO)
        motorhome = VeiculoFactory.criar_veiculo("motorhome", taxa_diaria=250.0, placa="XYZ9B99", categoria=Categoria.EXECUTIVO)
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
        VeiculoFactory.criar_veiculo("aviao", taxa_diaria=100.0, placa="ABC1234", categoria=Categoria.ECONOMICO)
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
        VeiculoFactory.criar_veiculo("carro", taxa_diaria=100.0, placa="1234567", categoria=Categoria.ECONOMICO)
    except Exception as e:
        print(f"Placa {e}")
    
    print("\n--- Teste 7: Calculo Padrão  ---")
    data_in = date(2026, 3, 10)
    data_out = date(2026, 3, 15)
    locacao_normal = Locacao(carro, data_in, data_out, CalculoPadraoStrategy())
    print(f"Valor Padrão: {locacao_normal.calcular_valor_locacao()}")

    print("\n--- Teste 8: Calculo VIP  ---")
    locacao_vip = Locacao(carro, data_in, data_out, CalculoVIPStrategy())
    print(f"Valor Cliente VIP: {locacao_vip.calcular_valor_locacao()}")

    print("\n--- Teste 9: PADRÃO STATE RESTRITIVO ---")
    carro_estado = VeiculoFactory.criar_veiculo("carro", taxa_diaria=100.0, placa="HJI3K45", categoria=Categoria.ECONOMICO)

# 1. Tentar alugar um carro de frota normal
    carro_estado.tentar_alugar() # OK - Transitará

# 2. Tentar locar novamente para outro!
    carro_estado.tentar_alugar() # Erro Interativo ("Já está alugado!")

# 3. Tentar mandar pra manutenção com cleinte
    carro_estado.reter_na_frota_pra_conserto() # Bloqueado

# 4. Devolver 
    carro_estado.tentar_devolver() # Ok (Retorna)

# 5. Colocar em checkups da empresa
    carro_estado.reter_na_frota_pra_conserto() # Ok 
    carro_estado.tentar_alugar() # Falha! Está em Manutenção.



    print("\n=== TESTES FINALIZADOS ===")

if __name__ == "__main__":
    executar_testes()