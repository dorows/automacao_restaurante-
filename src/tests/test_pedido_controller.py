# src/tests/test_pedido_controller.py

import pytest
from controllers.pedido_controller import PedidoController
from controllers.conta_controller import ContaController
from controllers.cardapio_controller import CardapioController
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.status_enums import StatusPedido

# --- Fixtures ---

@pytest.fixture
def cardapio_ctrl():
    return CardapioController()

@pytest.fixture
def conta_ctrl():
    return ContaController()

@pytest.fixture
def controller(conta_ctrl, cardapio_ctrl):
    return PedidoController(conta_ctrl, cardapio_ctrl)

@pytest.fixture
def setup_completo(conta_ctrl):
    """Cria um cenário pronto para pedidos: Mesa ocupada, garçom, conta aberta."""
    mesa = Mesa(1, 4)
    grupo = GrupoCliente(1, 2)
    garcom = Garcom(101, "Carlos", 1500)
    
    # Configuração manual para simular o estado
    mesa.garcom_responsavel = garcom
    mesa.ocupar(grupo)
    conta = conta_ctrl.abrir_nova_conta(grupo, mesa)
    
    return {"mesa": mesa, "conta": conta, "garcom": garcom}

# --- Testes ---

def test_realizar_pedido_sucesso(controller, setup_completo):
    """Testa criar um pedido (item) com sucesso."""
    mesa_id = setup_completo["mesa"].id_mesa
    
    # Pede o item ID 1 (Carbonara)
    conta_atualizada = controller.realizar_pedido(mesa_id, prato_id=1, quantidade=2)
    
    assert len(conta_atualizada.pedidos) == 1
    pedido = conta_atualizada.pedidos[0]
    assert pedido.status == StatusPedido.ABERTO
    assert len(pedido.itens) == 1
    assert pedido.itens[0].prato.id_prato == 1
    assert pedido.itens[0].quantidade == 2

def test_realizar_pedido_mesa_sem_conta(controller):
    """Testa falha ao pedir para mesa sem conta."""
    with pytest.raises(ValueError, match="Não há conta aberta"):
        controller.realizar_pedido(mesa_id=99, prato_id=1, quantidade=1)

def test_realizar_pedido_prato_inexistente(controller, setup_completo):
    """Testa falha ao pedir prato que não existe."""
    mesa_id = setup_completo["mesa"].id_mesa
    with pytest.raises(ValueError, match="Prato 999 não encontrado"):
        controller.realizar_pedido(mesa_id, prato_id=999, quantidade=1)

def test_fluxo_completo_pedido(controller, setup_completo):
    """Testa o ciclo de vida: Pedir -> Confirmar -> Pronto -> Entregar."""
    mesa_id = setup_completo["mesa"].id_mesa
    
    # 1. Realizar Pedido
    controller.realizar_pedido(mesa_id, 1, 1)
    
    # 2. Confirmar
    ped_conf = controller.confirmar_pedido(mesa_id)
    assert ped_conf.status == StatusPedido.EM_PREPARO
    
    # 3. Pronto
    ped_pronto = controller.marcar_pedido_pronto(mesa_id)
    assert ped_pronto.status == StatusPedido.PRONTO
    
    # 4. Entregar
    ped_entregue = controller.entregar_pedido(mesa_id)
    assert ped_entregue.status == StatusPedido.ENTREGUE

def test_confirmar_sem_pedido_aberto(controller, setup_completo):
    """Testa falha ao tentar confirmar quando não há nada para confirmar."""
    mesa_id = setup_completo["mesa"].id_mesa
    with pytest.raises(ValueError, match="Nenhum pedido ABERTO"):
        controller.confirmar_pedido(mesa_id)

def test_pronto_sem_pedido_em_preparo(controller, setup_completo):
    """Testa falha ao marcar pronto sem pedido em preparo."""
    mesa_id = setup_completo["mesa"].id_mesa
    # Cria pedido mas não confirma
    controller.realizar_pedido(mesa_id, 1, 1)
    
    with pytest.raises(ValueError, match="Nenhum pedido EM_PREPARO"):
        controller.marcar_pedido_pronto(mesa_id)

def test_conta_para_view(controller, setup_completo):
    """Testa a formatação dos dados para a view."""
    mesa_id = setup_completo["mesa"].id_mesa
    controller.realizar_pedido(mesa_id, 1, 2) # 2x Carbonara (55.50 cada)
    
    conta = setup_completo["conta"]
    dados = controller.conta_para_view(conta)
    
    assert dados["id_conta"] == conta.id_conta
    assert dados["total"] == 111.00
    assert len(dados["itens"]) == 1
    assert dados["itens"][0]["status"] == "Aberto (em anotação)" # ou check enum value