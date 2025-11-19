# tests/test_regras_negocio.py
import pytest
from models.excecoes import GarcomNoLimiteError, GrupoNaoCabeNaMesaError
from models.status_enums import StatusMesa

def test_limite_mesas_garcom(sistema_limpo):
    """Teste: Um garçom não pode atender mais de 4 mesas."""
    restaurante = sistema_limpo["restaurante"]
    func_ctrl = sistema_limpo["func"]
    mesa_ctrl = sistema_limpo["mesa"]

    # 1. Contrata um garçom
    garcom = restaurante.contratar_garcom("Jonas Teste", 1500.0)
    
    # 2. Cria 5 mesas novas
    for i in range(10, 15):
        mesa_ctrl.cadastrar_mesa(i, 4)

    # 3. Tenta atribuir 5 mesas ao mesmo garçom
    mesas = [mesa_ctrl.encontrar_mesa_por_numero(i) for i in range(10, 15)]
    
    # As primeiras 4 devem funcionar
    for m in mesas[:4]:
        mesa_ctrl.designar_garcom(m, garcom)
    
    assert len(garcom.mesas_atendidas) == 4

    # 4. A 5ª deve lançar a exceção customizada
    with pytest.raises(GarcomNoLimiteError):
        mesa_ctrl.designar_garcom(mesas[4], garcom)

def test_grupo_maior_que_capacidade(sistema_limpo):
    """Teste: Não pode colocar grupo de 6 pessoas em mesa de 2."""
    restaurante = sistema_limpo["restaurante"]
    cliente_ctrl = sistema_limpo["restaurante"]._cliente # Acesso direto para teste
    mesa_ctrl = sistema_limpo["mesa"]

    # Mesa 2 tem capacidade 2 (definido no setup inicial padrão)
    mesa_pequena = mesa_ctrl.encontrar_mesa_por_numero(2)
    
    # Grupo de 6 pessoas
    grupo_grande = cliente_ctrl.criar_grupo(6)

    with pytest.raises(GrupoNaoCabeNaMesaError):
        mesa_ctrl.ocupar_mesa(mesa_pequena.id_mesa, grupo_grande)