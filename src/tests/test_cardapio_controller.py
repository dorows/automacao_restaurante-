

import pytest
from controllers.cardapio_controller import CardapioController
from models.prato import Prato

@pytest.fixture
def controller() -> CardapioController:
    """Cria uma nova instância do CardapioController para cada teste."""
    return CardapioController()

# --- Testes de Setup e Busca ---

def test_setup_inicial(controller):
    """Testa se o cardápio inicial é carregado corretamente."""
    pratos = controller.cardapio.pratos
    assert len(pratos) == 16 # 16 pratos no setup inicial
    
    # Testa o primeiro
    carbonara = controller.buscar_prato_por_id(1)
    assert carbonara is not None
    assert isinstance(carbonara, Prato)
    assert carbonara.nome == "Spaghetti Alla Carbonara" # Model capitaliza
    assert carbonara.preco == 55.50
    
    # Testa um do meio (bebida)
    agua = controller.buscar_prato_por_id(102)
    assert agua.nome == "Água Com Gás"
    
    # Testa o último (sobremesa)
    sorvete = controller.buscar_prato_por_id(203)
    assert sorvete.nome == "Sorvete (2 Bolas)"

def test_buscar_prato_por_id(controller):
    """Testa a busca por ID."""
    prato = controller.buscar_prato_por_id(2)
    assert prato is not None
    assert prato.nome == "Lasanha Bolonhesa"
    
    # Testa busca por ID inexistente
    prato_inexistente = controller.buscar_prato_por_id(999)
    assert prato_inexistente is None

# --- Testes de Adicionar Prato ---

def test_adicionar_novo_prato_sucesso(controller):
    """Testa a adição bem-sucedida de um novo prato."""
    novo_prato = controller.adicionar_novo_prato(
        id_prato=301,
        nome="Bife Ancho",
        preco=89.90,
        descricao="Corte nobre grelhado."
    )
    
    assert isinstance(novo_prato, Prato)
    assert len(controller.cardapio.pratos) == 17 # 16 + 1
    
    # Verifica se o prato foi realmente salvo e pode ser buscado
    prato_salvo = controller.buscar_prato_por_id(301)
    assert prato_salvo is not None
    assert prato_salvo.nome == "Bife Ancho"

def test_adicionar_prato_id_duplicado(controller):
    """Testa se levanta ValueError ao tentar adicionar ID duplicado."""
    # O ID 1 (Carbonara) já existe
    with pytest.raises(ValueError, match="Já existe um prato cadastrado com o ID 1"):
        controller.adicionar_novo_prato(
            id_prato=1,
            nome="Prato Duplicado",
            preco=10.0,
            descricao="Erro"
        )
    
    # Garante que não foi adicionado
    assert len(controller.cardapio.pratos) == 16

def test_adicionar_prato_id_invalido(controller):
    """Testa se o Model (via controller) barra IDs inválidos."""
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.adicionar_novo_prato(0, "Nome", 10.0, "Desc")
        
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.adicionar_novo_prato(-1, "Nome", 10.0, "Desc")

def test_adicionar_prato_preco_invalido(controller):
    """Testa se o Model (via controller) barra preços inválidos."""
    with pytest.raises(ValueError, match="não pode ser negativo"):
        controller.adicionar_novo_prato(301, "Nome", -10.0, "Desc")
        
    with pytest.raises(TypeError, match="valor numérico"):
        controller.adicionar_novo_prato(302, "Nome", "caro", "Desc")

def test_adicionar_prato_nome_invalido(controller):
    """Testa se o Model (via controller) barra nomes inválidos."""
    with pytest.raises(ValueError, match="não pode ser vazio"):
        controller.adicionar_novo_prato(301, "   ", 10.0, "Desc")

# --- Teste da View ---

def test_listar_pratos_para_view(controller):
    """Testa se o dicionário formatado para a view está correto."""
    
    # Criamos um controller "limpo" para não depender do setup
    ctrl_limpo = CardapioController()
    ctrl_limpo._cardapio._pratos = [] # Limpa a lista
    
    # Adiciona um prato de teste
    ctrl_limpo.adicionar_novo_prato(10, "Teste Prato", 12.34, "Desc")
    
    dados_view = ctrl_limpo.listar_pratos_para_view()
    
    assert isinstance(dados_view, list)
    assert len(dados_view) == 1
    
    prato_dict = dados_view[0]
    assert isinstance(prato_dict, dict)
    assert prato_dict["id"] == 10
    assert prato_dict["nome"] == "Teste Prato"
    assert prato_dict["preco"] == 12.34