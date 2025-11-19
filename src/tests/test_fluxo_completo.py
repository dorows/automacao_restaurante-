# tests/test_fluxo_completo.py
from models.status_enums import StatusMesa, StatusPedido

def test_ciclo_vida_cliente(sistema_limpo):
    """
    Simula: Chegada -> Mesa -> Pedido -> Cozinha -> Entrega -> Pagamento -> Limpeza
    """
    app = sistema_limpo["restaurante"]
    mesa_ctrl = sistema_limpo["mesa"]
    sys_pedido = sistema_limpo["pedido"]
    
    # 1. Setup: Usamos a equipe padrão (Carlos e Ana já vêm no sistema)
    # Não precisamos contratar novos, pois o DAO já inicia com eles.
    
    # Carlos é o Garçom ID 101
    # Ana é a Cozinheira ID 103

    # 2. Chegada do Cliente (Grupo de 2 pessoas)
    msg = app.receber_clientes(2)
    assert "ALOCADO" in msg
    
    # Descobre qual mesa foi ocupada
    mesa_ocupada = None
    for m in mesa_ctrl.listar_mesas():
        if m.status == StatusMesa.OCUPADA:
            mesa_ocupada = m
            break
    
    assert mesa_ocupada is not None
    assert mesa_ocupada.garcom_responsavel is not None
    
    # CORREÇÃO: O sistema prioriza o Carlos (ID 101), pois ele é o primeiro da lista
    assert mesa_ocupada.garcom_responsavel.nome == "Carlos"

    # 3. Fazer Pedido (Item 1 do cardápio)
    conta = sys_pedido.realizar_pedido(mesa_ocupada.id_mesa, 1, 2) # 2x Carbonara
    
    assert len(conta.pedidos) == 1
    assert conta.pedidos[0].status.value == "Aberto (em anotação)"

    # 4. Confirmar Pedido (Envia para cozinha)
    app.confirmar_pedido_na_cozinha(mesa_ocupada.id_mesa)
    
    # Precisamos encontrar a Ana (Cozinheira Padrão) para verificar
    cozinheira_ana = sistema_limpo["func"].encontrar_funcionario_por_id(103)
    
    # Verifica se caiu na lista da Ana
    assert len(cozinheira_ana.pedidos_em_preparo) == 1
    pedido = cozinheira_ana.pedidos_em_preparo[0]
    assert pedido.status.value == "Em Preparo"

    # 5. Cozinha termina
    app.marcar_pedido_pronto(mesa_ocupada.id_mesa)
    assert len(cozinheira_ana.pedidos_em_preparo) == 0
    assert pedido.status.value == "Pronto"

    # 6. Garçom entrega
    sys_pedido.entregar_pedido(mesa_ocupada.id_mesa)
    assert pedido.status.value == "Entregue"

    # 7. Finalizar Conta
    # Valor esperado: 2 * 55.50 (Carbonara) = 111.00
    # + Gorjeta de 10.00
    dados_conta = app.finalizar_atendimento(mesa_ocupada.id_mesa, gorjeta=10.0)
    
    assert dados_conta["total"] == 111.00
    
    # Verifica se a gorjeta foi para o Carlos
    garcom_carlos = mesa_ocupada.garcom_responsavel
    assert garcom_carlos.gorjetas == 10.00
    assert mesa_ocupada.status == StatusMesa.SUJA

    # 8. Limpar Mesa
    app.limpar_mesa(mesa_ocupada.id_mesa)
    
    assert mesa_ocupada.status == StatusMesa.LIVRE
    assert mesa_ocupada not in garcom_carlos.mesas_atendidas