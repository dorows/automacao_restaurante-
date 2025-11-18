# src/tests/test_restaurante_integration.py

import pytest
# IMPORTANTE: Você precisará garantir que 'build_app' de main.py
# esteja acessível (ex: importando-a se main.py for importável).
# Assumiremos que ela foi importada como 'build_app' para este teste.
from main import build_app 

from models.status_enums import StatusMesa, StatusPedido
from models.garcom import Garcom
from models.mesa import Mesa

# --- Fixture ---

@pytest.fixture
def restaurante_app():
    """Cria e retorna o AppController completo com todas as dependências."""
    app_controller = build_app()
    
    # Para facilitar os asserts, criamos referências diretas
    return {
        "app": app_controller,
        "restaurante": app_controller.restaurante,
        "mesa_ctrl": app_controller.restaurante._mesa,
        "conta_ctrl": app_controller.restaurante._conta,
        "fila_ctrl": app_controller.restaurante._fila,
        "func_ctrl": app_controller.restaurante._func,
        "pedido_ctrl": app_controller.pedidos,
        "garcom_carlos": app_controller.restaurante._func.encontrar_funcionario_por_id(101) # Garçom inicial
    }

# --- Teste de Fluxo de Atendimento Completo ---

def test_fluxo_atendimento_e_fechamento(restaurante_app, capsys):
    """
    Simula o fluxo completo: Chegada -> Pedido -> Fechamento -> Limpeza -> Novo Alocamento.
    
    capfix é usado para capturar a saída do console, pois os métodos
    do RestauranteController ainda chamam print().
    """
    app = restaurante_app["app"]
    restaurante = restaurante_app["restaurante"]
    mesa_ctrl = restaurante_app["mesa_ctrl"]
    conta_ctrl = restaurante_app["conta_ctrl"]
    fila_ctrl = restaurante_app["fila_ctrl"]
    pedido_ctrl = restaurante_app["pedido_ctrl"]
    garcom_carlos = restaurante_app["garcom_carlos"]
    
    # --- Passo 1: Receber Clientes (Grupo 1) ---
    
    # Recebe 3 pessoas. Mesa 1 (4p) é a melhor opção livre.
    restaurante.receber_clientes_e_printar(3)
    
    mesa1 = mesa_ctrl.encontrar_mesa_por_numero(1)
    conta1 = conta_ctrl.encontrar_conta_por_mesa(1)
    
    # Verifica estado inicial
    assert mesa1.status == StatusMesa.OCUPADA
    assert mesa1.garcom_responsavel == garcom_carlos
    assert conta1 is not None
    assert conta1.id_conta == 1
    assert fila_ctrl.esta_vazia() is True
    assert len(garcom_carlos.mesas_atendidas) == 1
    
    # --- Passo 2: Receber Clientes (Grupo 2) e Enviar para Fila ---
    
    # Recebe um grupo grande (7 pessoas). Nenhuma mesa cabe.
    restaurante.receber_clientes_e_printar(7) 
    
    # Verifica se o grupo foi para a fila
    assert fila_ctrl.esta_vazia() is False
    assert fila_ctrl.listar()[0].numero_pessoas == 7
    
    # --- Passo 3: Realizar Pedido e Progredir Status ---
    
    # Pedir: Carbonara (ID 1, R$ 55.50) * 2 e Suco (ID 101, R$ 12.00) * 1
    app.pedidos.realizar_pedido(mesa_id=1, prato_id=1, quantidade=2)
    app.pedidos.realizar_pedido(mesa_id=1, prato_id=101, quantidade=1)
    
    # Confirmação do Pedido
    app.pedidos.confirmar_pedido(mesa_id=1)
    pedido1 = conta1.pedidos[0]
    
    assert len(conta1.pedidos) == 1
    assert pedido1.status == StatusPedido.EM_PREPARO
    
    # Total esperado: (55.50 * 2) + (12.00 * 1) = 111.00 + 12.00 = R$ 123.00
    assert conta1.calcular_total() == 123.00
    
    # --- Passo 4: Finalizar o Atendimento ---
    
    # Marca como Pronto e Entregue (para que a conta não fique com pedidos pendentes)
    app.pedidos.marcar_pedido_pronto(mesa_id=1)
    app.pedidos.entregar_pedido(mesa_id=1)
    
    # Finaliza com gorjeta de R$ 10.00
    restaurante.finalizar_atendimento_e_printar(mesa_id=1, gorjeta=10.00)
    
    # Verifica estado após finalização
    assert conta1.esta_aberta is False
    assert mesa1.status == StatusMesa.SUJA
    assert garcom_carlos.gorjetas == 10.00
    
    # --- Passo 5: Limpar a Mesa e Alocar o Grupo da Fila ---
    
    # Limpa a mesa 1 (deve acionar o auto_alocamento)
    restaurante.limpar_mesa_e_printar(mesa_id=1)
    
    # Verifica estado final
    mesa1_limpa = mesa_ctrl.encontrar_mesa_por_numero(1)
    
    # Mesa 1 deve estar LIVRE e sem garçom (mesa.limpar() reseta o garçom)
    assert mesa1_limpa.status == StatusMesa.LIVRE
    assert mesa1_limpa.garcom_responsavel is None
    
    # O Grupo 2 (7 pessoas) não deve ter sido alocado, pois a Mesa 1 (4p) não cabe.
    assert fila_ctrl.esta_vazia() is False
    assert fila_ctrl.listar()[0].numero_pessoas == 7
    
    # --- Passo 6: Adicionar Mesa Grande e Alocar o Grupo da Fila ---
    
    # Adiciona uma mesa grande (capacidade 8)
    restaurante.adicionar_mesa_e_printar(id_mesa=9, capacidade=8)
    mesa9 = mesa_ctrl.encontrar_mesa_por_numero(9)
    
    # A fila deve ter sido esvaziada por auto_alocamento
    assert fila_ctrl.esta_vazia() is True
    
    # Verifica se o Grupo 2 (7p) foi para a Mesa 9 (8p)
    assert mesa9.status == StatusMesa.OCUPADA
    assert mesa9.grupo_cliente.numero_pessoas == 7
    assert mesa9.garcom_responsavel.id_funcionario in [101, 102] # Algum garçom foi designado
    
    # Verifica se o ID do grupo foi ajustado
    grupo_na_mesa = mesa9.grupo_cliente
    assert grupo_na_mesa.status.name == "SENTADO"