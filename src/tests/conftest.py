# tests/conftest.py
import pytest
import os
import sys

# Adiciona o diretório 'src' ao path para conseguir importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controllers.restaurante_controller import RestauranteController
from controllers.pedido_controller import PedidoController
from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController

@pytest.fixture
def sistema_limpo(tmp_path, monkeypatch):
    """
    Cria uma instância completa do sistema rodando em um diretório temporário.
    Isso garante que os testes NÃO sobrescrevam os arquivos .pkl reais.
    """
    # Muda o diretório de trabalho para uma pasta temporária criada pelo pytest
    monkeypatch.chdir(tmp_path)
    
    # Inicializa todos os controllers (eles vão criar .pkl novos e vazios na pasta temp)
    cliente_ctrl = ClienteController()
    # Passa a dependência para o FilaController
    fila_ctrl = FilaController(cliente_controller=cliente_ctrl)
    
    mesa_ctrl = MesaController()
    func_ctrl = FuncionarioController()
    cardapio_ctrl = CardapioController()
    conta_ctrl = ContaController()
    
    pedido_ctrl = PedidoController(
        conta_controller=conta_ctrl, 
        cardapio_controller=cardapio_ctrl
    )

    restaurante = RestauranteController(
        mesa_controller=mesa_ctrl,
        conta_controller=conta_ctrl,
        fila_controller=fila_ctrl,
        funcionario_controller=func_ctrl,
        cardapio_controller=cardapio_ctrl,
        cliente_controller=cliente_ctrl,
        pedido_controller=pedido_ctrl,
    )

    return {
        "restaurante": restaurante,
        "func": func_ctrl,
        "mesa": mesa_ctrl,
        "pedido": pedido_ctrl,
        "conta": conta_ctrl,
        "fila": fila_ctrl,
        "cardapio": cardapio_ctrl
    }