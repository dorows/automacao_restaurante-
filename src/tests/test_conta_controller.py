# src/tests/test_conta_controller.py

import pytest
from controllers.conta_controller import ContaController
from models.conta import Conta
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente

# --- Fixtures ---
@pytest.fixture
def controller() -> ContaController:
    """Cria uma nova instância do ContaController para cada teste."""
    return ContaController()

@pytest.fixture
def mesa_1() -> Mesa:
    """Cria uma mesa (Mesa 1, Cap 4) limpa."""
    return Mesa(id_mesa=1, capacidade=4)

@pytest.fixture
def grupo_1() -> GrupoCliente:
    """Cria um grupo (Grupo 1, 2 pessoas)."""
    return GrupoCliente(id_grupo=1, numero_pessoas=2)

# --- Testes ---

def test_abrir_nova_conta_sucesso(controller, mesa_1, grupo_1):
    """Testa a abertura de conta bem-sucedida."""
    # Ocupa a mesa (pré-condição)
    mesa_1.ocupar(grupo_1)
    
    conta = controller.abrir_nova_conta(grupo_cliente=grupo_1, mesa=mesa_1)
    
    assert isinstance(conta, Conta)
    assert conta.id_conta == 1
    assert conta.mesa == mesa_1
    assert conta.grupo_cliente == grupo_1
    assert conta.esta_aberta is True
    
    # Verifica se a mesa foi associada à conta
    assert mesa_1.conta == conta
    
    # Tenta abrir outra
    grupo_2 = GrupoCliente(2, 1)
    mesa_2 = Mesa(2, 2)
    mesa_2.ocupar(grupo_2)
    
    conta_2 = controller.abrir_nova_conta(grupo_cliente=grupo_2, mesa=mesa_2)
    assert conta_2.id_conta == 2

def test_abrir_nova_conta_tipo_invalido(controller, mesa_1, grupo_1):
    """Testa se levanta TypeError se os argumentos estiverem errados."""
    
    # Grupo inválido
    with pytest.raises(TypeError, match="O argumento 'grupo_cliente'"):
        controller.abrir_nova_conta(grupo_cliente="Grupo Falso", mesa=mesa_1)
        
    # Mesa inválida
    with pytest.raises(TypeError, match="O argumento 'mesa'"):
        controller.abrir_nova_conta(grupo_cliente=grupo_1, mesa="Mesa Falsa")

def test_fechar_conta_sucesso(controller, mesa_1, grupo_1):
    """Testa se a conta é fechada corretamente."""
    mesa_1.ocupar(grupo_1)
    conta = controller.abrir_nova_conta(grupo_cliente=grupo_1, mesa=mesa_1)
    
    assert conta.esta_aberta is True
    
    # Fecha a conta
    controller.fechar_conta(conta)
    
    assert conta.esta_aberta is False

def test_fechar_conta_ja_fechada(controller, mesa_1, grupo_1):
    """Testa se levanta ValueError ao fechar uma conta já fechada."""
    mesa_1.ocupar(grupo_1)
    conta = controller.abrir_nova_conta(grupo_cliente=grupo_1, mesa=mesa_1)
    
    controller.fechar_conta(conta) # Fecha 1ª vez
    
    # Tenta fechar 2ª vez
    with pytest.raises(ValueError, match="já se encontra fechada"):
        controller.fechar_conta(conta)

def test_fechar_conta_tipo_invalido(controller):
    """Testa se levanta TypeError ao passar um objeto inválido."""
    with pytest.raises(TypeError, match="Objeto fornecido não é uma Conta válida"):
        controller.fechar_conta("Eu não sou uma conta")

def test_encontrar_conta_por_mesa_sucesso(controller, mesa_1, grupo_1):
    """Testa se a conta aberta correta é encontrada."""
    mesa_1.ocupar(grupo_1)
    conta_aberta = controller.abrir_nova_conta(grupo_cliente=grupo_1, mesa=mesa_1)
    
    conta_encontrada = controller.encontrar_conta_por_mesa(numero_mesa=1)
    
    assert conta_encontrada is not None
    assert conta_encontrada == conta_aberta
    assert conta_encontrada.id_conta == 1

def test_encontrar_conta_inexistente(controller):
    """Testa se retorna None ao procurar por mesa sem conta."""
    conta_encontrada = controller.encontrar_conta_por_mesa(numero_mesa=99)
    assert conta_encontrada is None

def test_encontrar_conta_ignora_fechada(controller, mesa_1, grupo_1):
    """Testa se o 'encontrar' ignora contas que já foram fechadas."""
    mesa_1.ocupar(grupo_1)
    conta = controller.abrir_nova_conta(grupo_cliente=grupo_1, mesa=mesa_1)
    
    # Fecha a conta
    controller.fechar_conta(conta)
    
    # Tenta encontrar a conta (não deve achar, pois está fechada)
    conta_encontrada = controller.encontrar_conta_por_mesa(numero_mesa=1)
    
    assert conta_encontrada is None