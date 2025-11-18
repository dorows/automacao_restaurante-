from controllers.app_controller import AppController
from controllers.restaurante_controller import RestauranteController
from controllers.pedido_controller import PedidoController
from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController

from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.pedido_view import PedidoView
from views.funcionario_view import FuncionarioView


def build_app() -> AppController:
    console_v = ConsoleView()
    mesa_v = MesaView()
    fila_v = FilaView()
    conta_v = ContaView()
    cardapio_v = CardapioView()
    pedido_v = PedidoView()
    func_v = FuncionarioView()

    mesa_ctrl = MesaController()
    conta_ctrl = ContaController()
    fila_ctrl = FilaController()
    func_ctrl = FuncionarioController()
    cardapio_ctrl = CardapioController()
    cliente_ctrl = ClienteController()

    pedido_ctrl = PedidoController(
        conta_controller=conta_ctrl,
        cardapio_controller=cardapio_ctrl,
    )

    restaurante_ctrl = RestauranteController(
        console_v=console_v,
        mesa_v=mesa_v,
        fila_v=fila_v,
        conta_v=conta_v,
        cardapio_v=cardapio_v,
        func_v=func_v,
        pedido_v=pedido_v,
        mesa_controller=mesa_ctrl,
        conta_controller=conta_ctrl,
        fila_controller=fila_ctrl,
        funcionario_controller=func_ctrl,
        cardapio_controller=cardapio_ctrl,
        cliente_controller=cliente_ctrl,
        pedido_controller=pedido_ctrl 
    )

    app = AppController(
        console=console_v,
        mesa_v=mesa_v,
        fila_v=fila_v,
        conta_v=conta_v,
        cardapio_v=cardapio_v,
        pedido_v=pedido_v,
        func_v=func_v,
        restaurante=restaurante_ctrl,
        pedidos=pedido_ctrl,
    )
    return app


def main() -> None:
    app = build_app()
    try:
        app.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
