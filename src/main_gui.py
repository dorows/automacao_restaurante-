from typing import Any, Dict, List, Optional, Tuple

import FreeSimpleGUI as sg

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

from views.gui_main_view import GuiMainView


def build_app_gui() -> Dict[str, Any]:
    # Controllers de domínio
    mesa_ctrl = MesaController()
    conta_ctrl = ContaController()
    fila_ctrl = FilaController()
    func_ctrl = FuncionarioController()
    cardapio_ctrl = CardapioController()
    cliente_ctrl = ClienteController()
    pedido_ctrl = PedidoController(conta_ctrl, cardapio_ctrl)

    # Views de console ainda são usadas pelo RestauranteController
    console_v = ConsoleView()
    mesa_v = MesaView()
    fila_v = FilaView()
    conta_v = ContaView()
    cardapio_v = CardapioView()
    pedido_v = PedidoView()
    func_v = FuncionarioView()

    restaurante = RestauranteController(
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
        pedido_controller=pedido_ctrl,
    )

    gui_view = GuiMainView()

    return {
        "restaurante": restaurante,
        "pedido_ctrl": pedido_ctrl,
        "mesa_ctrl": mesa_ctrl,
        "conta_ctrl": conta_ctrl,
        "fila_ctrl": fila_ctrl,
        "func_ctrl": func_ctrl,
        "cardapio_ctrl": cardapio_ctrl,
        "gui": gui_view,
    }


def _get_selected_mesa_id(values: Dict[str, Any],
                          mesas_cache: List[Dict[str, Any]]) -> Optional[int]:
    selecionadas = values.get("-TABELA_MESAS-")
    if not selecionadas:
        return None
    idx = selecionadas[0]
    if idx < 0 or idx >= len(mesas_cache):
        return None
    mesa = mesas_cache[idx]
    return int(mesa.get("id"))


def _get_selected_prato_id(values: Dict[str, Any],
                           cardapio_cache: List[Dict[str, Any]]) -> Optional[int]:
    selecionadas = values.get("-TABELA_CARDAPIO-")
    if not selecionadas:
        return None
    idx = selecionadas[0]
    if idx < 0 or idx >= len(cardapio_cache):
        return None
    prato = cardapio_cache[idx]
    return int(prato.get("id"))


def _atualizar_dashboard(
    gui: GuiMainView,
    mesa_ctrl: MesaController,
    fila_ctrl: FilaController,
    cardapio_ctrl: CardapioController,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    mesas = mesa_ctrl.listar_mesas_para_view()
    fila = fila_ctrl.listar_para_view()
    cardapio = cardapio_ctrl.listar_pratos_para_view()

    gui.update_mesas(mesas)
    gui.update_fila(fila)
    gui.update_cardapio(cardapio)
    gui.update_pedidos([])
    gui.update_conta_info(None)
    gui.set_status("Dashboard atualizado.")

    return mesas, cardapio


def _atualizar_pedidos_da_mesa(
    gui: GuiMainView,
    conta_ctrl: ContaController,
    pedido_ctrl: PedidoController,
    mesa_id: Optional[int],
) -> None:
    if mesa_id is None:
        gui.update_pedidos([])
        gui.update_conta_info(None)
        return

    conta = conta_ctrl.encontrar_conta_por_mesa(mesa_id)
    if not conta:
        gui.update_pedidos([])
        gui.update_conta_info(None)
        return

    conta_view = pedido_ctrl.conta_para_view(conta)

    linhas_tabela: List[List[Any]] = []
    for item in conta_view.get("itens", []):
        pedido_id = item.get("pedido_id")
        status = item.get("status", "")
        for linha in item.get("linhas", []):
            linhas_tabela.append([pedido_id, status, linha])

    gui.update_pedidos(linhas_tabela)
    gui.update_conta_info(conta_view)


def run_gui(app_parts: Dict[str, Any]) -> None:
    restaurante: RestauranteController = app_parts["restaurante"]
    pedido_ctrl: PedidoController = app_parts["pedido_ctrl"]
    mesa_ctrl: MesaController = app_parts["mesa_ctrl"]
    conta_ctrl: ContaController = app_parts["conta_ctrl"]
    fila_ctrl: FilaController = app_parts["fila_ctrl"]
    func_ctrl: FuncionarioController = app_parts["func_ctrl"]
    cardapio_ctrl: CardapioController = app_parts["cardapio_ctrl"]
    gui: GuiMainView = app_parts["gui"]

    mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

    while True:
        event, values = gui.read()
        if event in (sg.WIN_CLOSED, "-BTN_SAIR-"):
            break

        try:
            if event == "-BTN_ATUALIZAR-":
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

            elif event == "-TABELA_MESAS-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id)

            elif event == "-BTN_CHEGADA-":
                qtd_str = sg.popup_get_text("Número de pessoas no grupo:", title="Chegada de clientes")
                if qtd_str:
                    try:
                        qtd = int(qtd_str)
                    except ValueError:
                        gui.show_error("Quantidade inválida.")
                    else:
                        restaurante.receber_clientes_e_printar(qtd)
                        gui.set_status(f"Grupo de {qtd} pessoas processado.")
                        mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

            elif event == "-BTN_AUTO-":
                restaurante.auto_alocar_e_printar(greedy=True)
                gui.set_status("Auto-alocação da fila executada.")
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

            elif event == "-BTN_PEDIR-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                if mesa_id is None:
                    gui.show_error("Selecione uma mesa para fazer o pedido.")
                else:
                    prato_id = _get_selected_prato_id(values, cardapio_cache)
                    if prato_id is None:
                        gui.show_error("Selecione um prato no cardápio.")
                    else:
                        qtd_str = sg.popup_get_text("Quantidade:", title="Quantidade do prato")
                        if qtd_str:
                            try:
                                qtd = int(qtd_str)
                            except ValueError:
                                gui.show_error("Quantidade inválida.")
                            else:
                                conta = pedido_ctrl.realizar_pedido(mesa_id, prato_id, qtd)
                                _ = pedido_ctrl.conta_para_view(conta)
                                gui.set_status(f"Pedido registrado na mesa {mesa_id}.")
                                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id)

            elif event == "-BTN_CONFIRMAR-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                if mesa_id is None:
                    gui.show_error("Selecione uma mesa para confirmar o pedido.")
                else:
                    restaurante.confirmar_pedido_e_alocar_cozinheiro(mesa_id)
                    gui.set_status(f"Pedido da mesa {mesa_id} confirmado.")
                    _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id)

            elif event == "-BTN_PRONTO-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                if mesa_id is None:
                    gui.show_error("Selecione uma mesa para marcar o pedido como pronto.")
                else:
                    restaurante.marcar_pedido_pronto_e_printar(mesa_id)
                    gui.set_status(f"Pedido da mesa {mesa_id} marcado como pronto.")
                    _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id)

            elif event == "-BTN_ENTREGAR-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                if mesa_id is None:
                    gui.show_error("Selecione uma mesa para entregar o pedido.")
                else:
                    pedido_entregue = pedido_ctrl.entregar_pedido(mesa_id)
                    gui.set_status(f"Pedido #{pedido_entregue.id_pedido} entregue na mesa {mesa_id}.")
                    _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id)

            elif event == "-BTN_FINALIZAR-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                if mesa_id is None:
                    gui.show_error("Selecione uma mesa para finalizar o atendimento.")
                else:
                    gorjeta_str = sg.popup_get_text(
                        "Valor da gorjeta (opcional, deixe em branco para 0):",
                        title="Gorjeta"
                    )
                    gorjeta = 0.0
                    if gorjeta_str:
                        try:
                            gorjeta = float(gorjeta_str.replace(",", "."))
                        except ValueError:
                            gui.show_error("Valor de gorjeta inválido.")
                            gorjeta = None
                    if gorjeta is not None:
                        restaurante.finalizar_atendimento_e_printar(mesa_id, gorjeta)
                        gui.set_status(f"Atendimento da mesa {mesa_id} finalizado.")
                        mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

            elif event == "-BTN_LIMPAR-":
                mesa_id = _get_selected_mesa_id(values, mesas_cache)
                if mesa_id is None:
                    gui.show_error("Selecione uma mesa para limpar.")
                else:
                    restaurante.limpar_mesa_e_printar(mesa_id)
                    gui.set_status(f"Mesa {mesa_id} limpa.")
                    mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

        except Exception as e:
            gui.show_error(str(e))

    gui.close()


def main() -> None:
    app_parts = build_app_gui()
    run_gui(app_parts)


if __name__ == "__main__":
    main()
