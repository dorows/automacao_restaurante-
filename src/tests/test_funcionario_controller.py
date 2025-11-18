# test_funcionario_controller.py

import pytest
from unittest.mock import Mock

# Importe as classes que vamos testar e usar
from controllers.funcionario_controller import FuncionarioController
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro
from models.mesa import Mesa # Necessário para o teste de "garçom ocupado"

# --- Fixture ---
# Uma 'fixture' é uma função que o pytest executa antes de cada teste.
# Isso garante que cada teste receba uma instância "limpa" do controller,
# para que um teste não afete o outro.
@pytest.fixture
def controller() -> FuncionarioController:
    """Cria uma nova instância do FuncionarioController para cada teste."""
    return FuncionarioController()

# --- Testes ---

def test_setup_inicial(controller):
    """Testa se o setup inicial (chamado no __init__) funciona."""
    funcionarios = controller.listar_funcionarios()
    assert len(funcionarios) == 3
    assert isinstance(funcionarios[0], Garcom)
    assert funcionarios[0].id_funcionario == 101 # Carlos
    assert funcionarios[1].id_funcionario == 102 # Beatriz
    assert isinstance(funcionarios[2], Cozinheiro)
    assert funcionarios[2].id_funcionario == 103 # Ana

def test_contratar_garcom_sucesso(controller):
    """Testa a contratação bem-sucedida de um novo garçom."""
    novo_garcom = controller.contratar_garcom("Roberto", 2000.0)
    
    assert isinstance(novo_garcom, Garcom)
    assert novo_garcom.nome == "Roberto"
    assert novo_garcom.id_funcionario == 104 # 101, 102, 103 já foram usados no setup
    assert len(controller.listar_funcionarios()) == 4

def test_contratar_cozinheiro_sucesso(controller):
    """Testa a contratação bem-sucedida de um novo cozinheiro."""
    novo_coz = controller.contratar_cozinheiro("Julia", 2200.0)
    
    assert isinstance(novo_coz, Cozinheiro)
    assert novo_coz.nome == "Julia"
    assert novo_coz.id_funcionario == 104
    assert len(controller.listar_funcionarios()) == 4

def test_contratar_com_salario_invalido(controller):
    """Testa se o controller levanta um ValueError ao tentar contratar com salário negativo."""
    # 'pytest.raises' verifica se o código dentro do 'with' levanta a exceção esperada.
    with pytest.raises(ValueError, match="não pode ser negativo"):
        controller.contratar_garcom("Invalido", -100)
        
    with pytest.raises(ValueError, match="não pode ser negativo"):
        controller.contratar_cozinheiro("Invalido", -50)

def test_contratar_com_nome_invalido(controller):
    """Testa se o controller levanta um ValueError ao tentar contratar com nome vazio."""
    with pytest.raises(ValueError, match="não pode ser vazio"):
        controller.contratar_garcom("   ", 1500) # Nome vazio/só com espaços

def test_contratar_com_tipo_invalido(controller):
    """Testa se o controller levanta um TypeError com tipos de dados errados."""
    with pytest.raises(TypeError, match="deve ser um valor numérico"):
        controller.contratar_garcom("Nome", "mil_reais")

# --- Testes de Demissão ---

def test_demitir_funcionario_sucesso(controller):
    """Testa a demissão bem-sucedida de um funcionário."""
    func_demitido = controller.demitir_funcionario(101) # Demitindo Carlos
    
    assert func_demitido.id_funcionario == 101
    assert len(controller.listar_funcionarios()) == 2
    assert controller.encontrar_funcionario_por_id(101) is None # Não deve mais encontrar

def test_demitir_funcionario_nao_encontrado(controller):
    """Testa se levanta ValueError ao tentar demitir um ID inexistente."""
    with pytest.raises(ValueError, match="não encontrado"):
        controller.demitir_funcionario(999)

def test_demitir_garcom_ocupado(controller):
    """Testa se impede a demissão de um garçom que está atendendo mesas."""
    # 1. Pegar o garçom
    garcom_carlos = controller.encontrar_funcionario_por_id(101)
    
    # 2. Simular que ele está ocupado (adicionando uma mesa)
    mesa_fake = Mesa(id_mesa=1, capacidade=4)
    garcom_carlos.adicionar_mesa(mesa_fake)
    
    # 3. Tentar demitir
    with pytest.raises(ValueError, match="está atendendo mesas"):
        controller.demitir_funcionario(101)
        
    # 4. Verificar que ele NÃO foi demitido
    assert len(controller.listar_funcionarios()) == 3

def test_demitir_cozinheiro_ocupado(controller):
    """Testa se impede a demissão de um cozinheiro com pedidos em preparo."""
    # 1. Pegar o cozinheiro
    cozinheira_ana = controller.encontrar_funcionario_por_id(103)
    
    # 2. Simular que ela está ocupada.
    # Usamos um 'Mock' para simular um objeto Pedido
    # sem ter que criar um Pedido, Conta, Mesa, etc.
    mock_pedido = Mock()
    # mock_pedido.iniciar_preparo.return_value = True # <- Não precisamos mais disto
    
    # --- CORRIGIDO ---
    # Adicionamos o mock diretamente à lista interna para simular o estado
    # "ocupado", sem passar pela validação de tipo do iniciar_preparo_pedido().
    # Acessar '_pedidos_em_preparo' é aceitável em um teste.
    cozinheira_ana._pedidos_em_preparo.append(mock_pedido)
    
    assert len(cozinheira_ana.pedidos_em_preparo) == 1
    
    # 3. Tentar demitir
    with pytest.raises(ValueError, match="pedidos em preparo"):
        controller.demitir_funcionario(103)
        
    # 4. Verificar que ela NÃO foi demitida
    assert len(controller.listar_funcionarios()) == 3

# --- Testes de Lógica de Busca ---

def test_encontrar_garcom_disponivel(controller):
    """Testa a lógica de encontrar um garçom livre."""
    # No setup, Carlos (101) e Beatriz (102) estão livres.
    garcom = controller.encontrar_garcom_disponivel()
    assert garcom.id_funcionario == 101 # Deve retornar o primeiro, Carlos
    
    # Ocupar Carlos com 4 mesas
    g1 = controller.encontrar_funcionario_por_id(101)
    for i in range(1, 5):
        g1.adicionar_mesa(Mesa(i, 2))
    
    # Agora o disponível deve ser Beatriz (102)
    garcom = controller.encontrar_garcom_disponivel()
    assert garcom.id_funcionario == 102
    
    # Ocupar Beatriz com 4 mesas
    g2 = controller.encontrar_funcionario_por_id(102)
    for i in range(5, 9):
        g2.adicionar_mesa(Mesa(i, 2))
        
    # Agora não deve haver nenhum
    garcom = controller.encontrar_garcom_disponivel()
    assert garcom is None

# --- Testes de Atualização ---

def test_atualizar_nome(controller):
    """Testa a atualização de nome (incluindo normalização)."""
    func = controller.atualizar_nome(101, "  carlos alberto  ") # Nome com espaços
    
    assert func.id_funcionario == 101
    assert func.nome == "Carlos Alberto" # Verifica se o model limpou e capitalizou
    
    # Tentar atualizar funcionário inexistente
    with pytest.raises(ValueError, match="não encontrado"):
        controller.atualizar_nome(999, "Fantasma")
        
    # Tentar atualizar com nome inválido
    with pytest.raises(ValueError, match="não pode ser vazio"):
        controller.atualizar_nome(101, "")

def test_atualizar_salario(controller):
    """Testa a atualização de salário."""
    func = controller.atualizar_salario(102, 1800.50)
    
    assert func.id_funcionario == 102
    assert func.salario_base == 1800.50
    
    # Tentar atualizar funcionário inexistente
    with pytest.raises(ValueError, match="não encontrado"):
        controller.atualizar_salario(999, 3000)
        
    # Tentar atualizar com salário inválido
    with pytest.raises(ValueError, match="não pode ser negativo"):
        controller.atualizar_salario(102, -200)