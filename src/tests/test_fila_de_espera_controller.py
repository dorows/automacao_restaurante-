# src/tests/test_fila_de_espera_controller.py

import pytest
from controllers.fila_de_espera_controller import FilaController
from models.grupo_cliente import GrupoCliente

@pytest.fixture
def controller() -> FilaController:
    """Cria uma nova instância do FilaController para cada teste."""
    return FilaController()

@pytest.fixture
def g1() -> GrupoCliente:
    return GrupoCliente(id_grupo=1, numero_pessoas=2)

@pytest.fixture
def g2() -> GrupoCliente:
    return GrupoCliente(id_grupo=2, numero_pessoas=4)

@pytest.fixture
def g3() -> GrupoCliente:
    return GrupoCliente(id_grupo=3, numero_pessoas=3)

# --- Testes ---

def test_fila_vazia_inicial(controller):
    """Testa se a fila começa vazia."""
    assert controller.esta_vazia() is True
    assert len(controller.fila) == 0
    assert controller.listar() == []

def test_adicionar_grupo_sucesso(controller, g1):
    """Testa adicionar um grupo à fila."""
    controller.adicionar_grupo(g1)
    
    assert controller.esta_vazia() is False
    assert len(controller.fila) == 1
    assert controller.listar()[0] == g1

def test_adicionar_grupos_ordem(controller, g1, g2, g3):
    """Testa se a ordem de adição é mantida (FIFO)."""
    controller.adicionar_grupo(g1)
    controller.adicionar_grupo(g2)
    controller.adicionar_grupo(g3)
    
    lista = controller.listar()
    assert len(lista) == 3
    assert lista[0] == g1
    assert lista[1] == g2
    assert lista[2] == g3

def test_adicionar_grupo_duplicado(controller, g1):
    """Testa se levanta ValueError ao adicionar o mesmo grupo duas vezes."""
    controller.adicionar_grupo(g1)
    
    with pytest.raises(ValueError, match="já se encontra na fila"):
        controller.adicionar_grupo(g1)
        
    assert len(controller.fila) == 1

def test_adicionar_tipo_invalido(controller):
    """Testa se levanta TypeError ao adicionar algo que não é GrupoCliente."""
    with pytest.raises(TypeError, match="Apenas objetos da classe GrupoCliente"):
        controller.adicionar_grupo("Eu não sou um grupo")

def test_remover_grupo_sucesso(controller, g1, g2):
    """Testa a remoção de um grupo específico."""
    controller.adicionar_grupo(g1)
    controller.adicionar_grupo(g2)
    
    controller.remover(g1) # Remove o primeiro
    
    lista = controller.listar()
    assert len(lista) == 1
    assert lista[0] == g2

def test_remover_grupo_inexistente(controller, g1):
    """Testa se levanta ValueError ao remover um grupo que não está na fila."""
    with pytest.raises(ValueError, match="não foi encontrado na fila"):
        controller.remover(g1)

def test_chamar_proximo_grupo_sucesso(controller, g1, g2, g3):
    """Testa a lógica de chamar o próximo grupo que cabe."""
    controller.adicionar_grupo(g1) # 2 pessoas
    controller.adicionar_grupo(g2) # 4 pessoas
    controller.adicionar_grupo(g3) # 3 pessoas
    
    # Chama para uma mesa de 3 pessoas.
    # Deve pular g1 (porque g1 cabe) e chamar g1.
    grupo_chamado = controller.chamar_proximo_grupo(capacidade_disponivel=3)
    
    assert grupo_chamado == g1
    assert len(controller.fila) == 2
    assert controller.listar()[0] == g2 # g2 é o novo primeiro da fila

def test_chamar_proximo_grupo_pula_o_primeiro(controller, g1, g2, g3):
    """Testa que o 'chamar' pula um grupo grande se a capacidade for pequena."""
    controller.adicionar_grupo(g2) # 4 pessoas (primeiro na fila)
    controller.adicionar_grupo(g1) # 2 pessoas (segundo na fila)
    controller.adicionar_grupo(g3) # 3 pessoas (terceiro na fila)
    
    # Chama para uma mesa de 3 pessoas.
    # Deve pular g2 (4p > 3p) e chamar g1 (2p <= 3p).
    grupo_chamado = controller.chamar_proximo_grupo(capacidade_disponivel=3)
    
    assert grupo_chamado == g1
    assert len(controller.fila) == 2
    assert controller.listar()[0] == g2 # g2 continua na fila

def test_chamar_proximo_grupo_ninguem_cabe(controller, g2):
    """Testa se retorna None se ninguém na fila couber."""
    controller.adicionar_grupo(g2) # 4 pessoas
    
    grupo_chamado = controller.chamar_proximo_grupo(capacidade_disponivel=3)
    
    assert grupo_chamado is None
    assert len(controller.fila) == 1

def test_chamar_proximo_grupo_fila_vazia(controller):
    """Testa se retorna None se a fila estiver vazia."""
    grupo_chamado = controller.chamar_proximo_grupo(capacidade_disponivel=4)
    assert grupo_chamado is None

def test_chamar_proximo_capacidade_invalida(controller, g1):
    """Testa se o método interno trata capacidade inválida."""
    controller.adicionar_grupo(g1)
    # Não deve levantar exceção, apenas retornar None
    grupo_chamado = controller.chamar_proximo_grupo(capacidade_disponivel=0)
    assert grupo_chamado is None
    grupo_chamado = controller.chamar_proximo_grupo(capacidade_disponivel=-1)
    assert grupo_chamado is None

def test_listar_para_view(controller, g1, g2):
    """Testa se o dicionário formatado para a view está correto."""
    controller.adicionar_grupo(g1)
    controller.adicionar_grupo(g2)
    
    dados_view = controller.listar_para_view()
    
    assert isinstance(dados_view, list)
    assert len(dados_view) == 2
    
    g1_dict = dados_view[0]
    assert g1_dict["pos"] == 1
    assert g1_dict["nome"] == "Grupo 1"
    assert g1_dict["pessoas"] == 2
    
    g2_dict = dados_view[1]
    assert g2_dict["pos"] == 2
    assert g2_dict["nome"] == "Grupo 2"
    assert g2_dict["pessoas"] == 4