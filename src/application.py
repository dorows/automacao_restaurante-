# src/application.py
import FreeSimpleGUI as sg
from typing import Any, Dict, List, Optional, Tuple

# Controllers
from controllers.restaurante_controller import RestauranteController
from controllers.pedido_controller import PedidoController
from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController

# Views
from views.gui_main_view import GuiMainView
from views.gui_equipe_view import GuiEquipeView
from views.gui_stats_view import GuiStatsView
from views.gui_mesa_view import GuiMesaView
from views.gui_cardapio_view import GuiCardapioView
from views.gui_checkout_view import GuiCheckoutView # Nova View

from views.ui_theme import configure_global_ui

# --- Helpers de Fluxo (Movidos do antigo main.py) ---

def _get_selected_mesa_id(values: Dict[str, Any], mesas_cache: List[Dict[str, Any]]) -> Optional[int]:
    selecionadas = values.get("-TABELA_MESAS-")
    if not selecionadas:
        return None
    idx = selecionadas[0]
    if idx < 0 or idx >= len(mesas_cache):
        return None
    mesa = mesas_cache[idx]
    return int(mesa.get("id"))

def _get_selected_prato_id(values: Dict[str, Any], cardapio_cache: List[Dict[str, Any]]) -> Optional[int]:
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

    # Transforma para lista plana para tabela
    linhas_tabela: List[List[Any]] = []
    for item in conta_view.get("itens", []):
        pedido_id = item.get("pedido_id")
        status = item.get("status", "")
        for linha in item.get("linhas", []):
            linhas_tabela.append([pedido_id, status, linha])

    gui.update_pedidos(linhas_tabela)
    gui.update_conta_info(conta_view)

# --- Funções Principais de Construção e Execução ---

def build_app_gui() -> Dict[str, Any]:
    configure_global_ui() # Configura tema

    cliente_ctrl = ClienteController()
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

def run_gui(app_parts: Dict[str, Any]) -> None:
    # Desempacota
    restaurante: RestauranteController = app_parts["restaurante"]
    pedido_ctrl: PedidoController = app_parts["pedido_ctrl"]
    mesa_ctrl: MesaController = app_parts["mesa_ctrl"]
    conta_ctrl: ContaController = app_parts["conta_ctrl"]
    fila_ctrl: FilaController = app_parts["fila_ctrl"]
    func_ctrl: FuncionarioController = app_parts["func_ctrl"]
    cardapio_ctrl: CardapioController = app_parts["cardapio_ctrl"]
    gui: GuiMainView = app_parts["gui"]

    # Instancia janelas secundárias
    gui_equipe = GuiEquipeView(func_ctrl)
    gui_stats = GuiStatsView(restaurante)
    gui_mesa = GuiMesaView(restaurante, mesa_ctrl)
    gui_cardapio = GuiCardapioView(cardapio_ctrl)

    # Estado inicial
    mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
    mesa_id_selecionada: Optional[int] = None 
    gui.set_status("Sistema inicializado.")

    while True:
        event, values = gui.read()
        
        if event in (sg.WIN_CLOSED, "-BTN_SAIR-"):
            break

        try:
            if event == "-BTN_ATUALIZAR-":
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)

            elif event == "-TABELA_MESAS-":
                mesa_id_selecionada = _get_selected_mesa_id(values, mesas_cache)
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)
                            
            elif event == "-BTN_CHEGADA-":
                qtd_str = sg.popup_get_text("Número de pessoas no grupo:", title="Chegada de clientes")
                if qtd_str:
                    try:
                        qtd = int(qtd_str)
                        msg = restaurante.receber_clientes(qtd)
                        gui.set_status(msg)
                        mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
                    except ValueError:
                        gui.show_error("Número de pessoas inválido.")

            elif event == "-BTN_AUTO-":
                msgs_alocacao = restaurante.auto_alocar_grupos(greedy=True)
                gui.set_status(msgs_alocacao[0] if msgs_alocacao else "Nenhuma mesa livre encontrada para a fila.")
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)

            elif event == "-BTN_PEDIR-":
                if mesa_id_selecionada is None:
                    gui.show_error("Selecione uma mesa para fazer o pedido.")
                    continue
                prato_id = _get_selected_prato_id(values, cardapio_cache)
                if prato_id is None:
                    gui.show_error("Selecione um prato no cardápio.")
                    continue

                qtd_str = sg.popup_get_text("Quantidade:", title="Quantidade do prato")
                if qtd_str:
                    try:
                        qtd = int(qtd_str)
                        pedido_ctrl.realizar_pedido(mesa_id_selecionada, prato_id, qtd)
                        gui.set_status(f"Pedido registrado na mesa {mesa_id_selecionada}.")
                        _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)
                    except ValueError:
                        gui.show_error("Quantidade inválida.")

            elif event == "-BTN_CONFIRMAR-":
                if mesa_id_selecionada is None:
                    gui.show_error("Selecione uma mesa para confirmar o pedido.")
                    continue
                msg = restaurante.confirmar_pedido_na_cozinha(mesa_id_selecionada)
                gui.set_status(msg)
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)

            elif event == "-BTN_PRONTO-":
                if mesa_id_selecionada is None:
                    gui.show_error("Selecione uma mesa para marcar o pedido como pronto.")
                    continue
                msg = restaurante.marcar_pedido_pronto(mesa_id_selecionada)
                gui.set_status(msg)
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)

            elif event == "-BTN_ENTREGAR-":
                if mesa_id_selecionada is None:
                    gui.show_error("Selecione uma mesa para entregar o pedido.")
                    continue
                pedido_entregue = pedido_ctrl.entregar_pedido(mesa_id_selecionada)
                gui.set_status(f"Pedido #{pedido_entregue.id_pedido} entregue na mesa {mesa_id_selecionada}.")
                _atualizar_pedidos_da_mesa(gui, conta_ctrl, pedido_ctrl, mesa_id_selecionada)

            elif event == "-BTN_FINALIZAR-":
                if mesa_id_selecionada is None:
                    gui.show_error("Selecione uma mesa para finalizar o atendimento.")
                    continue

                conta = conta_ctrl.encontrar_conta_por_mesa(mesa_id_selecionada)
                if not conta:
                    gui.show_error(f"Não há conta aberta na mesa {mesa_id_selecionada}.")
                    continue

                # Transforma a conta para formato de View
                extrato_view = pedido_ctrl.conta_para_view(conta)

                # Chama a NOVA View de Checkout
                gorjeta, confirmado = GuiCheckoutView.abrir_janela_checkout(extrato_view)
                
                if not confirmado:
                    gui.set_status("Finalização cancelada pelo usuário.")
                    continue

                # Processa o pagamento no Controller
                extrato_final = restaurante.finalizar_atendimento(mesa_id_selecionada, gorjeta)

                total = float(extrato_final.get("total", 0.0))
                gui.show_info(
                    f"Conta #{extrato_final['id_conta']} fechada.\n"
                    f"Subtotal: R$ {total:.2f}\n"
                    f"Gorjeta: R$ {gorjeta:.2f}\n"
                    f"Total pago: R$ {total + gorjeta:.2f}"
                )

                mesa_id_selecionada = None
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
                gui.update_pedidos([])
                gui.update_conta_info(None)

            elif event == "-BTN_LIMPAR-":
                if mesa_id_selecionada is None:
                    gui.show_error("Selecione uma mesa para limpar.")
                    continue
                msg = restaurante.limpar_mesa(mesa_id_selecionada)
                gui.set_status(msg)
                mesa_id_selecionada = None
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
                
            elif event == "-BTN_EQUIPE-":
                gui_equipe.show_equipe_window() 
                gui.set_status("Gerenciamento de equipe finalizado.")

            elif event == "-BTN_MESAS-":   
                gui_mesa.show_mesa_window()
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)
                
            elif event == "-BTN_STATS-": 
                gui_stats.show_stats_window()
                
            elif event == "-BTN_MENU_ADMIN-": 
                gui_cardapio.show_cardapio_window()
                mesas_cache, cardapio_cache = _atualizar_dashboard(gui, mesa_ctrl, fila_ctrl, cardapio_ctrl)

        except Exception as e:
            import traceback
            traceback.print_exc()
            gui.show_error(f"Erro de Sistema: {e}")

    gui.close()