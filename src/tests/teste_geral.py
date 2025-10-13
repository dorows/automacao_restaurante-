

import sys
import os
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.app_controller import AppController
from controllers.restaurante_controller import RestauranteController
from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController
from controllers.pedido_controller import PedidoController

from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.pedido_view import PedidoView
from views.funcionario_view import FuncionarioView

def run_command(app: AppController, command: str):
    print("\n" + "-"*60)
    print(f"# EXECUTANDO COMANDO: '{command}'")
    print("-"*60)
    
    parts = command.strip().lower().split()
    acao = parts[0]
    args = parts[1:]
    app._dispatch(acao, args)
    input("Pressione Enter para continuar...")

def teste_completo():


    console_v = ConsoleView()
    mesa_v = MesaView()
    fila_v = FilaView()
    conta_v = ContaView()
    cardapio_v = CardapioView()
    pedido_v = PedidoView()
    func_v = FuncionarioView()

    # Instanciando todos os Controladores especialistas
    mesa_c = MesaController()
    conta_c = ContaController()
    fila_c = FilaController()
    func_c = FuncionarioController()
    cardapio_c = CardapioController()
    cliente_c = ClienteController()

    # O PedidoController depende de outros controladores
    pedido_c = PedidoController(console_v, pedido_v, conta_v, conta_c, cardapio_c)

    restaurante_c = RestauranteController(
        console_v=console_v,
        mesa_v=mesa_v,
        fila_v=fila_v,
        conta_v=conta_v,
        cardapio_v=cardapio_v,
        func_v=func_v,
        pedido_v=pedido_v, # <-- Argumento de View que estava em falta
        mesa_controller=mesa_c,
        conta_controller=conta_c,
        fila_controller=fila_c,
        funcionario_controller=func_c,
        cardapio_controller=cardapio_c,
        cliente_controller=cliente_c,
        pedido_controller=pedido_c # <-- Argumento de Controller que estava em falta
    )

    # O AppController orquestra tudo
    app = AppController(console_v, mesa_v, fila_v, conta_v, cardapio_v, pedido_v, func_v,
                        restaurante_c, pedido_c)

    # --- INÍCIO DA SIMULAÇÃO ---
    
    app.restaurante.print_dashboard()

    # Testando casos de exceção de contratação
    run_command(app, "contratar_garcom g 1000") # Nome muito curto, pode ser inválido dependendo da regra
    run_command(app, "contratar_cozinheiro ChefeLegal -500") # Salário negativo

    # Testando gestão da equipe
    run_command(app, "equipe")
    run_command(app, "contratar_cozinheiro David 2500.0")
    run_command(app, "demitir 999") # ID de funcionário inexistente

    # Testando gestão de mesas
    run_command(app, "adicionar_mesa 5 8")
    run_command(app, "adicionar_mesa 5 4") # ID de mesa duplicado

    # Testando fluxo de clientes
    run_command(app, "chegada 4")       # Grupo 1, senta na Mesa 1 (4 lugares)
    run_command(app, "chegada 2")       # Grupo 2, senta na Mesa 2 (2 lugares)
    run_command(app, "chegada 7")       # Grupo 3, vai para a fila
    run_command(app, "chegada 2")       # Grupo 4, vai para a fila

    app.restaurante.print_dashboard()

    # Testando fluxo de pedidos e exceções
    run_command(app, "pedir 1 1 2")     # Mesa 1 pede 2 Carbonaras
    run_command(app, "pedir 1 101 4")   # Mesa 1 pede 4 Sucos
    run_command(app, "pedir 99 1 1")    # Mesa inexistente
    run_command(app, "pedir 1 999 1")   # Prato inexistente
    run_command(app, "pedir 2 102 2")   # Mesa 2 pede 2 Águas

    # Testando fluxo da cozinha
    run_command(app, "confirmar 1")     # Confirma pedido da Mesa 1
    run_command(app, "confirmar 1")     # Tenta confirmar o mesmo pedido de novo (deve dar erro/aviso)
    run_command(app, "equipe")          # Deve mostrar o Cozinheiro Ana com pedidos
    run_command(app, "pronto 1")        # Cozinheiro termina o pedido da Mesa 1
    run_command(app, "entregar 1")      # Garçom entrega o pedido da Mesa 1

    run_command(app, "limpar 1")        # Tenta limpar uma mesa ocupada (deve falhar)
    run_command(app, "finalizar 1 5.50")# Finaliza Mesa 1 com R$ 5.50 de gorjeta
    
    app.restaurante.print_dashboard()
    
    run_command(app, "limpar 1")        # Limpa a Mesa 1, que estava suja
                                        # O sistema deve auto-alocar o Grupo 4 (2 pessoas) na Mesa 1 (4 lugares)

    # Testando demissão com restrições
    run_command(app, "pedir 2 1 1")
    run_command(app, "confirmar 2")
    run_command(app, "demitir 103")     # Tenta demitir a Cozinheira Ana com um pedido em preparo (deve falhar)
    
    # Finalizando o resto
    run_command(app, "finalizar 2")
    run_command(app, "finalizar 4")
    
    console_v.print_lines(["\n>>> SIMULAÇÃO CONCLUÍDA <<<"])


if __name__ == "__main__":
    teste_completo()