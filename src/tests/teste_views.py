import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.pedido_view import PedidoView
from views.funcionario_view import FuncionarioView

from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController
from controllers.pedido_controller import PedidoController
from controllers.restaurante_controller import RestauranteController


def criar_sistema():
    # Views
    console = ConsoleView()
    mesa_v = MesaView()
    fila_v = FilaView()
    conta_v = ContaView()
    cardapio_v = CardapioView()
    pedido_v = PedidoView()
    func_v = FuncionarioView()

    # Controllers de domínio
    mesa_c = MesaController()
    conta_c = ContaController()
    fila_c = FilaController()
    func_c = FuncionarioController()
    cardapio_c = CardapioController()
    cliente_c = ClienteController()

    # PedidoController depende de conta_controller e cardapio_controller + views
    pedido_c = PedidoController(
        console_v=console,
        pedido_v=pedido_v,
        conta_v=conta_v,
        conta_controller=conta_c,
        cardapio_controller=cardapio_c,
    )

    # RestauranteController é o orquestrador
    restaurante = RestauranteController(
        console_v=console,
        mesa_v=mesa_v,
        fila_v=fila_v,
        conta_v=conta_v,
        cardapio_v=cardapio_v,
        func_v=func_v,
        pedido_v=pedido_v,
        mesa_controller=mesa_c,
        conta_controller=conta_c,
        fila_controller=fila_c,
        funcionario_controller=func_c,
        cardapio_controller=cardapio_c,
        cliente_controller=cliente_c,
        pedido_controller=pedido_c,
    )

    return {
        "console": console,
        "mesa_v": mesa_v,
        "fila_v": fila_v,
        "conta_v": conta_v,
        "cardapio_v": cardapio_v,
        "pedido_v": pedido_v,
        "func_v": func_v,
        "mesa_c": mesa_c,
        "conta_c": conta_c,
        "fila_c": fila_c,
        "func_c": func_c,
        "cardapio_c": cardapio_c,
        "cliente_c": cliente_c,
        "pedido_c": pedido_c,
        "restaurante": restaurante,
    }


def testar_mesas_para_view(mesa_c: MesaController):
    print("\n=== TESTE: MesaController.listar_mesas_para_view ===")
    mesas_view = mesa_c.listar_mesas_para_view()
    for m in mesas_view:
        print(m)
    assert isinstance(mesas_view, list)
    assert all(isinstance(m, dict) for m in mesas_view)
    assert all({"id", "cap", "status", "garcom"} <= set(m.keys()) for m in mesas_view)


def testar_fila_para_view(fila_c: FilaController, cliente_c: ClienteController):
    print("\n=== TESTE: FilaController.listar_para_view ===")
    # No começo deve estar vazia
    print("Fila inicial:", fila_c.listar_para_view())

    # Cria dois grupos e adiciona na fila
    g1, _ = cliente_c.criar_grupo(2)
    g2, _ = cliente_c.criar_grupo(4)
    ok1, msg1 = fila_c.adicionar_grupo(g1)
    ok2, msg2 = fila_c.adicionar_grupo(g2)
    print(msg1)
    print(msg2)

    fila_view = fila_c.listar_para_view()
    for item in fila_view:
        print(item)

    assert len(fila_view) == 2
    assert fila_view[0]["pessoas"] == 2
    assert fila_view[1]["pessoas"] == 4


def testar_garcons_para_view(func_c: FuncionarioController):
    print("\n=== TESTE: FuncionarioController.listar_garcons_para_view ===")
    garcons_view = func_c.listar_garcons_para_view()
    for g in garcons_view:
        print(g)
    assert isinstance(garcons_view, list)
    assert all("id" in g and "nome" in g and "mesas" in g for g in garcons_view)


def testar_cardapio_para_view(cardapio_c: CardapioController):
    print("\n=== TESTE: CardapioController.listar_pratos_para_view ===")
    pratos_view = cardapio_c.listar_pratos_para_view()
    for p in pratos_view:
        print(p)
    assert isinstance(pratos_view, list)
    assert all("id" in p and "nome" in p and "preco" in p for p in pratos_view)
    assert len(pratos_view) > 0  # cardápio inicial não deve estar vazio


def testar_conta_para_view(
    mesa_c: MesaController,
    conta_c: ContaController,
    cardapio_c: CardapioController,
    func_c: FuncionarioController,
    cliente_c: ClienteController,
    pedido_c: PedidoController,
):
    print("\n=== TESTE: PedidoController.conta_para_view ===")

    # 1) Criar grupo e ocupar uma mesa
    grupo, msg_grupo = cliente_c.criar_grupo(3)
    print(msg_grupo)

    mesa = mesa_c.encontrar_mesa_por_numero(1)
    if mesa is None:
        raise RuntimeError("Mesa 1 não encontrada no setup inicial")

    mesa.ocupar(grupo)

    # 2) Designar garçom para a mesa
    garcom = func_c.encontrar_garcom_disponivel()
    if garcom is None:
        raise RuntimeError("Nenhum garçom disponível no setup inicial")

    ok_g, msg_g = mesa_c.designar_garcom(mesa, garcom)
    print(msg_g)

    # 3) Abrir conta para o grupo/mesa
    conta, msg_conta = conta_c.abrir_nova_conta(grupo, mesa)
    print(msg_conta)
    if conta is None:
        raise RuntimeError("Falha ao abrir conta para teste")

    # 4) Adicionar um item de pedido na conta
    prato = cardapio_c.buscar_prato_por_id(1)
    if prato is None:
        raise RuntimeError("Prato 1 não encontrado no cardápio")

    pedido_c.adicionar_item_a_conta(conta, prato, quantidade=2)

    # 5) Gerar o dict para view a partir da conta
    conta_view = pedido_c.conta_para_view(conta)
    print("Conta para view:")
    print(conta_view)

    assert conta_view["id_conta"] == conta.id_conta
    assert conta_view["mesa_id"] == mesa.id_mesa
    assert conta_view["cliente"].startswith("Grupo ")
    assert conta_view["total"] > 0
    assert len(conta_view["itens"]) == 1  # deve haver um pedido
    assert len(conta_view["itens"][0]["linhas"]) == 1  # um item lançado


def testar_print_dashboard(restaurante: RestauranteController):
    print("\n=== TESTE: RestauranteController.print_dashboard ===")
    # Se os métodos *para_view* estiverem ok, esse método deve rodar sem exception
    restaurante.print_dashboard()
    print("print_dashboard executado com sucesso.")


def rodar_todos_os_testes():
    deps = criar_sistema()

    testar_mesas_para_view(deps["mesa_c"])
    testar_fila_para_view(deps["fila_c"], deps["cliente_c"])
    testar_garcons_para_view(deps["func_c"])
    testar_cardapio_para_view(deps["cardapio_c"])
    testar_conta_para_view(
        mesa_c=deps["mesa_c"],
        conta_c=deps["conta_c"],
        cardapio_c=deps["cardapio_c"],
        func_c=deps["func_c"],
        cliente_c=deps["cliente_c"],
        pedido_c=deps["pedido_c"],
    )
    testar_print_dashboard(deps["restaurante"])

    print("\n=== TODOS OS TESTES TERMINARAM SEM ERROS ===")


if __name__ == "__main__":
    rodar_todos_os_testes()
