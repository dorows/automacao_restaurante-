# tests/test_fluxo_restaurante.py
from models.status_enums import StatusPedido, StatusMesa

def test_fluxo_completo_atendimento(app):
    """
    Teste End-to-End: Chegada -> Pedido -> Cozinha -> Pagamento -> Relatório.
    """
    # 1. Cliente Chega
    msg = app.receber_clientes(2)
    assert "ALOCADO" in msg
    
    # Identificar mesa (assumindo Mesa 2 ou 3 que são pequenas)
    mesa_id = 0
    for m in app._mesa.listar_mesas():
        if m.status == StatusMesa.OCUPADA:
            mesa_id = m.id_mesa
            break
    assert mesa_id > 0

    # 2. Fazer Pedido (Item 1 do cardápio)
    app._pedido_controller.realizar_pedido(mesa_id, 1, 2) # 2x Item 1
    
    # 3. Confirmar e Cozinha
    msg_conf = app.confirmar_pedido_na_cozinha(mesa_id)
    assert "confirmado" in msg_conf.lower()
    
    # Verificar se o cozinheiro recebeu
    cozinheiro = app._func.encontrar_cozinheiro_disponivel() # Retorna quem tem menos pedidos (ou seja, quem pegou)
    assert len(cozinheiro.pedidos_em_preparo) > 0 or len(app._func.listar_funcionarios()[2].pedidos_em_preparo) > 0

    # 4. Pronto e Entregar
    app.marcar_pedido_pronto(mesa_id)
    # Entregar
    app._pedido_controller.entregar_pedido(mesa_id)
    
    # 5. Finalizar e Pagar
    dados = app.finalizar_atendimento(mesa_id, gorjeta=15.0)
    assert dados['total'] > 0
    
    # 6. Verificar Relatório (Stats)
    stats_garcom = app.obter_dados_relatorio_equipe()
    # Deve haver algum garçom com gorjeta > 0
    assert any(g['total_gorjetas'] > 0 for g in stats_garcom)

def test_logica_fila_e_auto_alocacao(app):
    """
    Testa: Lotação -> Fila -> Liberação -> Auto Alocar.
    """
    # 1. Lota o restaurante (Setup tem 4 mesas: caps 4, 2, 2, 6)
    # Vamos ocupar todas
    app.receber_clientes(4) # Ocupa Mesa 1
    app.receber_clientes(2) # Ocupa Mesa 2
    app.receber_clientes(2) # Ocupa Mesa 3
    app.receber_clientes(6) # Ocupa Mesa 4
    
    # Verifica se todas estão ocupadas
    mesas_livres = [m for m in app._mesa.listar_mesas() if m.status == StatusMesa.LIVRE]
    assert len(mesas_livres) == 0

    # 2. Tenta colocar mais um grupo (Deve ir para FILA)
    msg_fila = app.receber_clientes(2)
    assert "FILA" in msg_fila
    
    # Verifica controller de fila
    assert len(app._fila.listar()) == 1

    # 3. Libera uma mesa (Mesa 2, cap 2)
    # Finaliza atendimento da Mesa 2
    app.finalizar_atendimento(2)
    # Limpa a mesa (agora ela fica LIVRE, mas vazia)
    app.limpar_mesa(2)
    
    mesa_2 = app._mesa.encontrar_mesa_por_numero(2)
    assert mesa_2.status == StatusMesa.LIVRE
    assert mesa_2.grupo_cliente is None

    # 4. Executa Auto Alocar
    msgs = app.auto_alocar_grupos(greedy=True)
    
    # 5. Verifica se o grupo da fila foi para a mesa
    assert len(msgs) > 0
    assert "ALOCADO" in msgs[0]
    assert len(app._fila.listar()) == 0 # Fila vazia
    
    mesa_2_pos = app._mesa.encontrar_mesa_por_numero(2)
    assert mesa_2_pos.status == StatusMesa.OCUPADA # Agora tem gente