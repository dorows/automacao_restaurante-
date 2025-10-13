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
            try:
                self.console.print_lines(self.console._help_lines())
                self.restaurante.auto_alocar_e_printar(greedy=False)
                self.restaurante.print_dashboard()
                
                acao, args = self.console.read_command()
                
                if acao == "sair":
                    self.console.print_lines(["Obrigado por usar o sistema. Até logo!"])
                    break

                self._dispatch(acao, args)
            
            except Exception as e:
                self.console.print_lines([f"[ERRO FATAL NO LOOP PRINCIPAL] {e}"])


    def _dispatch(self, acao: str, args: List[str]) -> None:

        try:
            if acao == "chegada":
                if len(args) != 1: raise ValueError("requer 1 argumento: <qtd_pessoas>")
                qtd = int(args[0])
                self.restaurante.receber_clientes_e_printar(qtd)

            elif acao == "pedir":
                if len(args) != 3: raise ValueError("requer 3 argumentos: <mesa_id> <prato_id> <qtd>")
                mesa_id, prato_id, qtd = map(int, args)
                self.pedidos.realizar_pedido_e_printar(mesa_id, prato_id, qtd)

            elif acao == "confirmar":
                if len(args) != 1: raise ValueError("requer 1 argumento: <mesa_id>")
                mesa_id = int(args[0])
                self.pedidos.confirmar_e_printar(mesa_id)

            elif acao == "pronto":
                if len(args) != 1: raise ValueError("requer 1 argumento: <mesa_id>")
                mesa_id = int(args[0])
                self.pedidos.pronto_e_printar(mesa_id)

            elif acao == "entregar":
                if len(args) != 1: raise ValueError("requer 1 argumento: <mesa_id>")
                mesa_id = int(args[0])
                self.pedidos.entregar_e_printar(mesa_id)

            elif acao == "finalizar":
                if len(args) < 1:
                    raise ValueError("requer pelo menos 1 argumento: <mesa_id>")
                
                mesa_id = int(args[0])
                gorjeta = float(args[1]) if len(args) > 1 else 0.0
                
                self.restaurante.finalizar_atendimento_e_printar(mesa_id, gorjeta)

            elif acao == "limpar":
                if len(args) != 1: raise ValueError("requer 1 argumento: <mesa_id>")
                mesa_id = int(args[0])
                self.restaurante.limpar_mesa_e_printar(mesa_id)

            elif acao == "cardapio":
                dados_do_cardapio = self.restaurante.get_cardapio_data()
                self.cardapio_v.exibir_cardapio(dados_do_cardapio)

            elif acao == "equipe":
                self.restaurante.listar_equipe_e_printar()

            elif acao == "contratar_garcom":
                if len(args) != 2: raise ValueError("requer 2 argumentos: <nome> <salario>")
                nome = args[0]
                salario = float(args[1])
                self.restaurante.contratar_garcom_e_printar(nome, salario)

            elif acao == "contratar_cozinheiro":
                if len(args) != 2: raise ValueError("requer 2 argumentos: <nome> <salario>")
                nome = args[0]
                salario = float(args[1])
                self.restaurante.contratar_cozinheiro_e_printar(nome, salario)

            elif acao == "demitir":
                if len(args) != 1: raise ValueError("requer 1 argumento: <id_func>")
                id_func = int(args[0])
                self.restaurante.demitir_funcionario_e_printar(id_func)
            
            elif acao == "stats": 
                self.restaurante.ver_prato_mais_pedido_e_printar()

            elif acao == "adicionar_mesa":
                if len(args) != 2: raise ValueError("requer 2 argumentos: <id_mesa> <capacidade>")
                id_mesa, capacidade = map(int, args)
                self.restaurante.adicionar_mesa_e_printar(id_mesa, capacidade)

            elif acao in ("ajuda", "help", "?"):
                self.console.print_lines(self.console._help_lines())

            elif acao == "": 
                pass 
            
            else:
                self.console.print_lines([f"Comando '{acao}' inválido."])

        except (ValueError, IndexError) as e:
            self.console.print_lines([f"[ERRO DE COMANDO] {e}"])
        except Exception as e:
            self.console.print_lines([f"[ERRO INESPERADO NO SISTEMA] {e}"])