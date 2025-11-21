# src/views/gui_checkout_view.py
import FreeSimpleGUI as sg
from typing import Dict, Any, List, Tuple

class GuiCheckoutView:
    """
    Classe responsável apenas por exibir a janela de checkout e retornar
    os valores de gorjeta e confirmação.
    """
    
    @staticmethod
    def abrir_janela_checkout(extrato: Dict[str, Any]) -> Tuple[float, bool]:
        mesa_id = extrato.get("mesa_id")
        cliente = extrato.get("cliente", "Cliente")
        subtotal = float(extrato.get("total", 0.0))

        # 10% sugerido de gorjeta
        sugerido = round(subtotal * 0.10, 2)
        gorjeta_inicial_str = f"{sugerido:.2f}"

        # Monta a tabela de itens
        tabela_itens: List[List[str]] = []
        for item in extrato.get("itens", []):
            pedido_id = item.get("pedido_id")
            status = item.get("status", "")
            for linha in item.get("linhas", []):
                tabela_itens.append([str(pedido_id), status, linha])

        headings = ["Pedido", "Status", "Item"]

        layout = [
            [sg.Text(f"Checkout - Mesa {mesa_id} - {cliente}", font=("Any", 14, "bold"))],
            [sg.Table(
                values=tabela_itens,
                headings=headings,
                key="-CHK_TABELA-",
                auto_size_columns=True,
                justification="left",
                expand_x=True,
                expand_y=True,
                num_rows=min(len(tabela_itens), 10) if tabela_itens else 5,
                enable_events=False,
            )],
            [sg.Text(f"Subtotal: R$ {subtotal:.2f}", key="-CHK_SUBTOTAL-")],
            [sg.Text(f"Sugerido 10%: R$ {sugerido:.2f}", key="-CHK_SUGERIDO-")],
            [
                sg.Text("Gorjeta:"),
                sg.Input(
                    gorjeta_inicial_str,
                    key="-CHK_GORJETA-",
                    size=(10, 1),
                    enable_events=True,
                ),
                sg.Text("R$"),
            ],
            [
                sg.Text("Total a pagar: R$ ", key="-CHK_TOTAL_LABEL-"),
                sg.Text(f"{subtotal + sugerido:.2f}", key="-CHK_TOTAL-"),
            ],
            [
                sg.Button("Confirmar", key="-CHK_CONFIRMAR-"),
                sg.Button("Cancelar", key="-CHK_CANCELAR-"),
            ],
        ]

        window = sg.Window(
            "Checkout da Conta",
            layout,
            modal=True,
            resizable=True,
            finalize=True,
        )

        gorjeta_valor = sugerido
        confirmado = False

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "-CHK_CANCELAR-"):
                confirmado = False
                break

            if event == "-CHK_GORJETA-":
                txt = values.get("-CHK_GORJETA-", "").strip()
                try:
                    if txt == "":
                        v = 0.0
                    else:
                        v = float(txt.replace(",", "."))
                except ValueError:
                    v = 0.0
                total_final = subtotal + v
                window["-CHK_TOTAL-"].update(f"{total_final:.2f}")

            elif event == "-CHK_CONFIRMAR-":
                txt = values.get("-CHK_GORJETA-", "").strip()
                try:
                    if txt == "":
                        gorjeta_valor = 0.0
                    else:
                        gorjeta_valor = float(txt.replace(",", "."))
                except ValueError:
                    sg.popup_error("Valor de gorjeta inválido.")
                    continue

                confirmado = True
                break

        window.close()
        return gorjeta_valor, confirmado