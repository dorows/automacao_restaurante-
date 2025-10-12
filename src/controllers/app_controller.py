from typing import List
from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.pedido_view import PedidoView
from views.funcionario_view import FuncionarioView
from controllers.restaurante_controller import RestauranteController
from controllers.pedido_controller import PedidoController

class AppController:
    """
    Controlador principal do aplicativo.
    Mantém o loop: ajuda -> autoaloca -> painel -> comando -> despacha.
    """
    def __init__(self,
                 console: ConsoleView,
                 mesa_v: MesaView,
                 fila_v: FilaView,
                 conta_v: ContaView,
                 cardapio_v: CardapioView,
                 pedido_v: PedidoView,
                 func_v: FuncionarioView,
                 restaurante: RestauranteController,
                 pedidos: PedidoController) -> None:
        self.console = console
        self.mesa_v = mesa_v
        self.fila_v = fila_v
        self.conta_v = conta_v
        self.cardapio_v = cardapio_v
        self.pedido_v = pedido_v
        self.func_v = func_v
        self.restaurante = restaurante
        self.pedidos = pedidos

    def run(self) -> None:
        while True:
            # 0) imprime sempre os comandos no início do ciclo (silencioso fora do loop)
            self.console.print_lines(self.console._help_lines())

            # 1) autoalocação no começo do loop
            self.restaurante.auto_alocar_e_printar(greedy=False)

            # 2) dashboard
            self.restaurante.print_dashboard()

            # 3) comando
            acao, args = self.console.read_command()
            self._dispatch(acao, args)

    def _dispatch(self, acao: str, args: List[str]) -> None:
        try:
            if acao == "chegada":
                qtd = int(args[0]) if args else 0
                self.restaurante.receber_clientes_e_printar(qtd)

            elif acao == "pedir":
                mesa_id, prato_id, qtd = map(int, args[:3])
                self.pedidos.realizar_pedido_e_printar(mesa_id, prato_id, qtd)

            elif acao == "confirmar":
                mesa_id = int(args[0])
                self.pedidos.confirmar_e_printar(mesa_id)

            elif acao == "pronto":
                mesa_id = int(args[0])
                self.pedidos.pronto_e_printar(mesa_id)

            elif acao == "entregar":
                mesa_id = int(args[0])
                self.pedidos.entregar_e_printar(mesa_id)

            elif acao == "finalizar":
                mesa_id = int(args[0])
                self.restaurante.finalizar_atendimento_e_printar(mesa_id)

            elif acao == "limpar":
                mesa_id = int(args[0])
                self.restaurante.limpar_mesa_e_printar(mesa_id)

            elif acao == "cardapio":
                self.restaurante.listar_cardapio_e_printar()

            elif acao == "equipe":
                self.restaurante.listar_equipe_e_printar()

            elif acao == "contratar_garcom":
                nome = args[0]
                salario = float(args[1])
                self.restaurante.contratar_garcom_e_printar(nome, salario)

            elif acao == "contratar_cozinheiro":
                nome = args[0]
                salario = float(args[1])
                self.restaurante.contratar_cozinheiro_e_printar(nome, salario)

            elif acao == "demitir":
                id_func = int(args[0])
                self.restaurante.demitir_funcionario_e_printar(id_func)

            elif acao == "adicionar_mesa":
                id_mesa = int(args[0])
                capacidade = int(args[1])
                self.restaurante.adicionar_mesa_e_printar(id_mesa, capacidade)

            elif acao in ("ajuda", "help", "?"):
                self.console.print_lines(self._help_lines())

            else:
                self.console.print_lines(["Comando inválido."])

        except (IndexError, ValueError):
            self.console.print_lines(["Parâmetros inválidos."])
