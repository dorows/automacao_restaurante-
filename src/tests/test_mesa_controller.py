# src/tests/test_mesa_controller.py

import pytest
from unittest.mock import Mock

from controllers.mesa_controller import MesaController
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.status_enums import StatusMesa

@pytest.fixture
def controller() -> MesaController:
    """Cria uma nova instância do MesaController para cada teste."""
    return MesaController()

@pytest.fixture
def garcom_mock() -> Garcom:
    """Cria um garçom (real, não mock) para testes."""
    return Garcom(id_funcionario=1, nome="Garçom Teste", salario_base=1500)

@pytest.fixture
def grupo_pequeno() -> GrupoCliente:
    """Cria um grupo de 2 pessoas."""
    return GrupoCliente(id_grupo=1, numero_pessoas=2)

@pytest.fixture
def grupo_grande() -> GrupoCliente:
    """Cria um grupo de 5 pessoas."""
    return GrupoCliente(id_grupo=2, numero_pessoas=5)

# --- Testes de Setup e Busca ---

def test_setup_inicial(controller):
    """Testa se as 4 mesas iniciais são carregadas."""
    mesas = controller.listar_mesas()
    assert len(mesas) == 4
    assert mesas[0].id_mesa == 1
    assert mesas[3].capacidade == 6

def test_encontrar_mesa_por_numero(controller):
    """Testa a busca de mesa por ID."""
    mesa = controller.encontrar_mesa_por_numero(1)
    assert mesa is not None
    assert mesa.capacidade == 4
    
    mesa_inexistente = controller.encontrar_mesa_por_numero(999)
    assert mesa_inexistente is None

def test_encontrar_mesa_livre_best_fit(controller):
    """Testa a lógica de 'best-fit' para encontrar a menor mesa adequada."""
    
    # Mesas: (1: 4p), (2: 2p), (3: 2p), (4: 6p)
    
    # Pede para 2 pessoas: deve pegar a mesa 2 (primeira de menor capacidade)
    mesa_2p = controller.encontrar_mesa_livre(2)
    assert mesa_2p.id_mesa == 2
    
    # Pede para 1 pessoa: também deve pegar a mesa 2
    mesa_1p = controller.encontrar_mesa_livre(1)
    assert mesa_1p.id_mesa == 2
    
    # Pede para 5 pessoas: deve pegar a mesa 4 (a única que cabe)
    mesa_5p = controller.encontrar_mesa_livre(5)
    assert mesa_5p.id_mesa == 4
    
    # Pede para 7 pessoas: não deve encontrar
    mesa_7p = controller.encontrar_mesa_livre(7)
    assert mesa_7p is None

def test_encontrar_mesa_livre_quando_ocupada(controller, grupo_pequeno):
    """Testa que a mesa 2 não é encontrada se já estiver ocupada."""
    
    # Ocupa a mesa 2
    controller.ocupar_mesa(2, grupo_pequeno)
    
    # Pede para 2 pessoas de novo: agora deve pegar a mesa 3
    mesa_2p_prox = controller.encontrar_mesa_livre(2)
    assert mesa_2p_prox.id_mesa == 3

# --- Testes de CRUD de Mesa ---

def test_cadastrar_mesa_sucesso(controller):
    """Testa a adição de uma nova mesa."""
    nova_mesa = controller.cadastrar_mesa(id_mesa=5, capacidade=8)
    assert isinstance(nova_mesa, Mesa)
    assert len(controller.listar_mesas()) == 5
    assert controller.encontrar_mesa_por_numero(5).capacidade == 8

def test_cadastrar_mesa_id_duplicado(controller):
    """Testa se impede a criação de mesa com ID repetido."""
    with pytest.raises(ValueError, match="Já existe uma mesa com o ID 1"):
        controller.cadastrar_mesa(id_mesa=1, capacidade=2)

def test_cadastrar_mesa_capacidade_invalida(controller):
    """Testa se o Model (chamado pelo controller) impede capacidade 0 ou negativa."""
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.cadastrar_mesa(id_mesa=5, capacidade=0)
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.cadastrar_mesa(id_mesa=6, capacidade=-2)

# --- Testes de Fluxo (Ocupar, Liberar, Limpar) ---

def test_ocupar_mesa_sucesso(controller, grupo_pequeno):
    """Testa o fluxo de ocupar uma mesa."""
    mesa = controller.ocupar_mesa(1, grupo_pequeno)
    assert mesa.status == StatusMesa.OCUPADA
    assert mesa.grupo_cliente == grupo_pequeno

def test_ocupar_mesa_inexistente(controller, grupo_pequeno):
    """Testa se falha ao tentar ocupar mesa que não existe."""
    with pytest.raises(ValueError, match="não encontrada"):
        controller.ocupar_mesa(99, grupo_pequeno)

def test_ocupar_mesa_nao_livre(controller, grupo_pequeno):
    """Testa se falha ao tentar ocupar uma mesa já ocupada."""
    controller.ocupar_mesa(1, grupo_pequeno) # Ocupa
    
    with pytest.raises(ValueError, match="não está livre"):
        controller.ocupar_mesa(1, grupo_pequeno) # Ocupa de novo

def test_ocupar_mesa_capacidade_insuficiente(controller, grupo_grande):
    """Testa se falha ao tentar ocupar uma mesa menor que o grupo."""
    with pytest.raises(ValueError, match="não cabe na Mesa 1"):
        controller.ocupar_mesa(1, grupo_grande) # Grupo de 5 em mesa de 4

def test_liberar_mesa_sucesso(controller, grupo_pequeno):
    """Testa o fluxo de liberar uma mesa."""
    controller.ocupar_mesa(1, grupo_pequeno) # Ocupada
    
    mesa_liberada = controller.liberar_mesa(1) # Libera
    assert mesa_liberada.status == StatusMesa.SUJA
    assert mesa_liberada.grupo_cliente is None # Verifica se o grupo saiu

def test_liberar_mesa_nao_ocupada(controller):
    """Testa se falha ao tentar liberar uma mesa que não está ocupada."""
    # Mesa 1 está LIVRE
    with pytest.raises(ValueError, match="Apenas uma mesa ocupada"):
        controller.liberar_mesa(1)

def test_limpar_mesa_sucesso(controller, grupo_pequeno):
    """Testa o fluxo completo: Ocupar -> Liberar -> Limpar."""
    controller.ocupar_mesa(1, grupo_pequeno)
    controller.liberar_mesa(1) # Status -> SUJA
    
    mesa_limpa = controller.limpar_mesa(1) # Limpa
    assert mesa_limpa.status == StatusMesa.LIVRE

def test_limpar_mesa_nao_suja(controller):
    """Testa se falha ao tentar limpar uma mesa que não está suja."""
    # Mesa 1 está LIVRE
    with pytest.raises(ValueError, match="Apenas uma mesa suja"):
        controller.limpar_mesa(1)

# --- Teste de Garçom ---

def test_designar_garcom_sucesso(controller, garcom_mock):
    """Testa se o garçom é designado corretamente."""
    mesa = controller.encontrar_mesa_por_numero(1)
    
    controller.designar_garcom(mesa, garcom_mock)
    
    assert mesa.garcom_responsavel == garcom_mock
    assert len(garcom_mock.mesas_atendidas) == 1
    assert garcom_mock.mesas_atendidas[0] == mesa

def test_designar_garcom_limite(controller, garcom_mock):
    """Testa se o garçom atinge o limite de 4 mesas."""
    mesas = controller.listar_mesas() # Pega as 4 mesas do setup
    
    # Designa as 4 mesas
    controller.designar_garcom(mesas[0], garcom_mock)
    controller.designar_garcom(mesas[1], garcom_mock)
    controller.designar_garcom(mesas[2], garcom_mock)
    controller.designar_garcom(mesas[3], garcom_mock)
    
    assert len(garcom_mock.mesas_atendidas) == 4
    
    # Cria uma quinta mesa
    nova_mesa = controller.cadastrar_mesa(5, 2)
    
    # Tenta designar a quinta mesa
    with pytest.raises(ValueError, match="limite de 4 mesas"):
        controller.designar_garcom(nova_mesa, garcom_mock)