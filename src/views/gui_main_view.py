import FreeSimpleGUI as sg
from typing import List, Dict, Optional


class GuiMainView:
    def __init__(self) -> None:
        sg.theme("DarkBlue3")

        self._mesas_data: List[Dict[str, object]] = []
        self._fila_data: List[Dict[str, object]] = []
        self._cardapio_data: List[Dict[str, object]] = []
        self._pedidos_data: List[List[object]] = []

        self._build_window()

    def _build_window(self) -> None:
        tabela_mesas = sg.Table(
            values=[],
            headings=["Mesa", "Cap.", "Status", "Garçom"],
            key="-TABELA_MESAS-",
            justification="center",
            auto_size_columns=True,
            display_row_numbers=False,
            enable_events=True,
            num_rows=5,
            expand_x=True,
            expand_y=True,
        )

        tabela_fila = sg.Table(
            values=[],
            headings=["Pos.", "Grupo", "Pessoas"],
            key="-TABELA_FILA-",
            justification="center",
            auto_size_columns=True,
            display_row_numbers=False,
            enable_events=False,
            num_rows=5,
            expand_x=True,
            expand_y=True,
        )

        tabela_cardapio = sg.Table(
            values=[],
            headings=["ID", "Nome", "Preço"],
            key="-TABELA_CARDAPIO-",
            justification="left",
            auto_size_columns=True,
            display_row_numbers=False,
            enable_events=True,
            num_rows=6,
            expand_x=True,
            expand_y=True,
        )

        tabela_pedidos = sg.Table(
            values=[],
            headings=["Pedido", "Status", "Item"],
            key="-TABELA_PEDIDOS-",
            justification="left",
            auto_size_columns=True,
            display_row_numbers=False,
            enable_events=False,
            num_rows=8,
            expand_x=True,
            expand_y=True,
        )

        layout = [
            [sg.Text(
                "Automação de Restaurante - MVC + FreeSimpleGUI",
                font=("Arial", 18, "bold")
            )],
            [
                sg.Frame(
                    "Mesas",
                    [[tabela_mesas]],
                    expand_x=True,
                    expand_y=True,
                ),
                sg.Frame(
                    "Fila de Espera",
                    [[tabela_fila]],
                    expand_x=True,
                    expand_y=True,
                ),
            ],
            [
                sg.Frame(
                    "Cardápio",
                    [[tabela_cardapio]],
                    expand_x=True,
                    expand_y=True,
                )
            ],
            [
                sg.Frame(
                    "Pedidos da Mesa Selecionada",
                    [
                        [sg.Text(
                            "Nenhuma mesa selecionada.",
                            key="-CONTA_INFO-",
                            size=(60, 1)
                        )],
                        [tabela_pedidos],
                    ],
                    expand_x=True,
                    expand_y=True,
                )
            ],
            [
                sg.Button("Chegada", key="-BTN_CHEGADA-"),
                sg.Button("Pedir", key="-BTN_PEDIR-"),
                sg.Button("Confirmar", key="-BTN_CONFIRMAR-"),
                sg.Button("Pronto", key="-BTN_PRONTO-"),
                sg.Button("Entregar", key="-BTN_ENTREGAR-"),
                sg.Button("Finalizar", key="-BTN_FINALIZAR-"),
                sg.Button("Limpar Mesa", key="-BTN_LIMPAR-"),
                sg.Button("Auto Alocar", key="-BTN_AUTO-"),
                sg.Button("Atualizar", key="-BTN_ATUALIZAR-"),
                sg.Button("Sair", key="-BTN_SAIR-"),
            ],
            [
                sg.Text("", key="-STATUS-", size=(80, 1))
            ],
        ]

        self.window = sg.Window(
            "Restaurante MVC - GUI",
            layout,
            finalize=True,
            resizable=True,
        )

    def read(self):
        return self.window.read()

    def close(self) -> None:
        self.window.close()

    def update_mesas(self, mesas: List[Dict[str, object]]) -> None:
        self._mesas_data = mesas or []
        valores = [
            [
                m.get("id", ""),
                m.get("cap", ""),
                m.get("status", ""),
                m.get("garcom", "") or "",
            ]
            for m in self._mesas_data
        ]
        self.window["-TABELA_MESAS-"].update(values=valores)

    def update_fila(self, fila: List[Dict[str, object]]) -> None:
        self._fila_data = fila or []
        valores = [
            [
                f.get("pos", ""),
                f.get("nome", ""),
                f.get("pessoas", ""),
            ]
            for f in self._fila_data
        ]
        self.window["-TABELA_FILA-"].update(values=valores)

    def update_cardapio(self, pratos: List[Dict[str, object]]) -> None:
        self._cardapio_data = pratos or []
        valores = [
            [
                p.get("id", ""),
                p.get("nome", ""),
                f"R$ {p.get('preco', 0.0):.2f}",
            ]
            for p in self._cardapio_data
        ]
        self.window["-TABELA_CARDAPIO-"].update(values=valores)

    def update_pedidos(self, linhas: List[List[object]]) -> None:
        self._pedidos_data = linhas or []
        self.window["-TABELA_PEDIDOS-"].update(values=self._pedidos_data)

    def update_conta_info(self, conta: Optional[Dict[str, object]]) -> None:
        if not conta:
            texto = "Nenhuma conta ativa para a mesa selecionada."
        else:
            mesa_id = conta.get("mesa_id", "?")
            cliente = conta.get("cliente", "Cliente desconhecido")
            total = conta.get("total", 0.0)
            texto = f"Mesa {mesa_id} - {cliente} | Total: R$ {total:.2f}"
        self.window["-CONTA_INFO-"].update(texto)

    def set_status(self, msg: str) -> None:
        self.window["-STATUS-"].update(msg)

    def show_info(self, msg: str) -> None:
        self.set_status(msg)
        sg.popup_ok(msg, title="Informação")

    def show_error(self, msg: str) -> None:
        self.set_status(msg)
        sg.popup_error(msg, title="Erro")
