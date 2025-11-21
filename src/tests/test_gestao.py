# tests/test_gestao.py
import pytest
from models.status_enums import StatusMesa

def test_gestao_funcionarios(app):
    """Testa o ciclo de vida de um funcionário (CRUD)."""
    
    # 1. Contratar
    novo_garcom = app.contratar_garcom("TesteGarcom", 2000.0)
    assert novo_garcom.nome == "TesteGarcom"
    assert novo_garcom.id_funcionario > 0
    
    # Verificar se apareceu na lista
    equipe = app.listar_equipe()
    nomes = [f['nome'] for f in equipe]
    assert "TesteGarcom" in nomes

    # 2. Editar (Renomear e Salvar Salário)
    # Nota: O controller expõe métodos de atualizar via func_ctrl, mas o RestauranteController
    # que limpamos não tem wrappers diretos para isso, então acessamos o _func interno ou
    # usamos os métodos que criamos se estiverem expostos.
    # Vamos assumir acesso via _func para teste unitário profundo:
    app._func.atualizar_nome(novo_garcom.id_funcionario, "GarcomEditado")
    app._func.atualizar_salario(novo_garcom.id_funcionario, 2500.0)
    
    atualizado = app._func.encontrar_funcionario_por_id(novo_garcom.id_funcionario)
    assert atualizado.nome == "GarcomEditado"
    assert atualizado.salario_base == 2500.0

    # 3. Demitir
    app.demitir_funcionario(novo_garcom.id_funcionario)
    removido = app._func.encontrar_funcionario_por_id(novo_garcom.id_funcionario)
    assert removido is None

def test_gestao_mesas(app):
    """Testa adicionar, editar e remover mesas."""
    
    # 1. Adicionar Mesa Nova (ID 99)
    app.adicionar_mesa(99, 4)
    mesa = app._mesa.encontrar_mesa_por_numero(99)
    assert mesa is not None
    assert mesa.capacidade == 4

    # 2. Editar Capacidade
    app.atualizar_mesa(99, 8)
    mesa = app._mesa.encontrar_mesa_por_numero(99)
    assert mesa.capacidade == 8

    # 3. Remover Mesa
    app.remover_mesa(99)
    mesa = app._mesa.encontrar_mesa_por_numero(99)
    assert mesa is None

def test_validacao_remocao_mesa_ocupada(app):
    """Não deve permitir remover mesa se ela estiver ocupada."""
    # Ocupa a mesa 1 (que já vem no setup)
    app.receber_clientes(2) 
    
    # Tenta remover a mesa 1
    with pytest.raises(ValueError) as excinfo:
        app.remover_mesa(1) # Assumindo que mesa 1 foi a escolhida
    
    assert "não é possível remover" in str(excinfo.value).lower()