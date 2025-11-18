import pytest
from controllers.grupo_cliente_controller import ClienteController
from models.grupo_cliente import GrupoCliente

@pytest.fixture
def controller() -> ClienteController:
    """Cria uma nova instância do ClienteController para cada teste."""
    return ClienteController()

# --- Testes ---

def test_criar_grupo_sucesso(controller):
    """Testa a criação bem-sucedida de um grupo."""
    grupo = controller.criar_grupo(numero_pessoas=4)
    
    assert isinstance(grupo, GrupoCliente)
    assert grupo.id_grupo == 1
    assert grupo.numero_pessoas == 4
    
    # Verifica se foi adicionado à lista interna
    lista = controller.listar_grupos()
    assert len(lista) == 1
    assert lista[0] == grupo

def test_criar_grupos_ids_incrementais(controller):
    """Testa se os IDs dos grupos são únicos e incrementais."""
    grupo1 = controller.criar_grupo(2)
    grupo2 = controller.criar_grupo(3)
    grupo3 = controller.criar_grupo(1)
    
    assert grupo1.id_grupo == 1
    assert grupo2.id_grupo == 2
    assert grupo3.id_grupo == 3
    
    lista = controller.listar_grupos()
    assert len(lista) == 3

def test_criar_grupo_pessoas_invalidas(controller):
    """Testa se levanta ValueError para número de pessoas 0 ou negativo."""
    
    # O Model 'GrupoCliente' é quem gera essa exceção
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.criar_grupo(numero_pessoas=0)
        
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.criar_grupo(numero_pessoas=-2)
        
    # Garante que nenhum grupo foi criado
    assert len(controller.listar_grupos()) == 0

def test_criar_grupo_tipo_invalido(controller):
    """Testa se levanta ValueError para tipo inválido de 'numero_pessoas'."""
    # O construtor do GrupoCliente verifica 'isinstance(..., int)'
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.criar_grupo(numero_pessoas="duas") # Passa string
        
    with pytest.raises(ValueError, match="inteiro positivo"):
        controller.criar_grupo(numero_pessoas=2.5) # Passa float
        
    # Garante que nenhum grupo foi criado
    assert len(controller.listar_grupos()) == 0