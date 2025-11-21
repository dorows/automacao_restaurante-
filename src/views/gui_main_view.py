import FreeSimpleGUI as sg
from typing import List, Dict, Optional


class GuiMainView:
    def __init__(self) -> None:
        # Tema e fonte já vêm do configure_global_ui()
        self._mesas_data: List[Dict[str, object]] = []
        self._fila_data: List[Dict[str, object]] = []
        self._cardapio_data: List[Dict[str, object]] = []
        self._pedidos_data: List[List[object]] = []

        self._build_window()

    def _build_window(self) -> None:
        # Tabela de mesas
        tabela_mesas = sg.Table(
            values=[],
            headings=["Mesa", "Cap.", "Status", "Garçom"],
            key="-TABELA_MESAS-",
            justification="center",
            auto_size_columns=False,
            col_widths=[6, 6, 10, 18],
            display_row_numbers=False,
            enable_events=True,
            num_rows=7,
            expand_x=True,
            expand_y=True,
            alternating_row_color="#1E2933",
            header_background_color="#1976D2",
            header_text_color="white",
            row_height=24,
        )

        # Tabela de fila
        tabela_fila = sg.Table(
            values=[],
            headings=["Pos.", "Grupo", "Pessoas"],
            key="-TABELA_FILA-",
            justification="center",
            auto_size_columns=False,
            col_widths=[5, 14, 8],
            display_row_numbers=False,
            enable_events=False,
            num_rows=7,
            expand_x=True,
            expand_y=True,
            alternating_row_color="#1E2933",
            header_background_color="#1976D2",
            header_text_color="white",
            row_height=24,
        )

        # Tabela de cardápio
        tabela_cardapio = sg.Table(
            values=[],
            headings=["ID", "Nome", "Preço"],
            key="-TABELA_CARDAPIO-",
            justification="left",
            auto_size_columns=False,
            col_widths=[6, 26, 10],
            display_row_numbers=False,
            enable_events=True,
            num_rows=10,
            expand_x=True,
            expand_y=True,
            alternating_row_color="#1E2933",
            header_background_color="#1976D2",
            header_text_color="white",
            row_height=24,
        )

        # Tabela de pedidos da mesa
        tabela_pedidos = sg.Table(
            values=[],
            headings=["Pedido", "Status", "Item"],
            key="-TABELA_PEDIDOS-",
            justification="left",
            auto_size_columns=False,
            col_widths=[8, 10, 40],
            display_row_numbers=False,
            enable_events=False,
            num_rows=8,
            expand_x=True,
            expand_y=True,
            alternating_row_color="#1E2933",
            header_background_color="#1976D2",
            header_text_color="white",
            row_height=24,
        )

        header_row = [
            sg.Text(
                "🍽️  Automação de Restaurante",
                font=("Segoe UI", 20, "bold"),
            ),
            sg.Push(),
            sg.Button(
                "Mesas",
                key="-BTN_MESAS-",
                button_color=("white", "#455A64"),
                size=(9, 1),
            ),
            sg.Button(
                "Equipe",
                key="-BTN_EQUIPE-",
                button_color=("white", "#455A64"),
                size=(9, 1),
            ),
            sg.Button(
                "Cardápio",
                key="-BTN_MENU_ADMIN-",
                button_color=("white", "#00897B"),
                size=(9, 1),
            ),
            
            sg.Button(
                "Stats",
                key="-BTN_STATS-",
                button_color=("white", "#00897B"),
                size=(9, 1),
            ),
            sg.Button(
                "Sair",
                key="-BTN_SAIR-",
                button_color=("white", "#C62828"),
                size=(9, 1),
            ),
        ]

        frame_mesas = sg.Frame(
            "Mesas",
            [[tabela_mesas]],
            expand_x=True,
            expand_y=True,
            relief=sg.RELIEF_RAISED,
        )

        frame_fila = sg.Frame(
            "Fila de Espera",
            [[tabela_fila]],
            expand_x=True,
            expand_y=True,
            relief=sg.RELIEF_RAISED,
        )

        col_esquerda = sg.Column(
            [
                [frame_mesas],
                [frame_fila],
            ],
            expand_x=True,
            expand_y=True,
        )

        frame_cardapio = sg.Frame(
            "Cardápio",
            [[tabela_cardapio]],
            expand_x=True,
            expand_y=True,
            relief=sg.RELIEF_RAISED,
        )

        frame_conta = sg.Frame(
            "Conta da Mesa",
            [
                [
                    sg.Text(
                        "Nenhuma mesa selecionada.",
                        key="-CONTA_INFO-",
                        size=(60, 1),
                    )
                ],
                [tabela_pedidos],
            ],
            expand_x=True,
            expand_y=True,
            relief=sg.RELIEF_RAISED,
        )

        col_direita = sg.Column(
            [
                [frame_cardapio],
                [frame_conta],
            ],
            expand_x=True,
            expand_y=True,
        )

        actions_row = [
            sg.Button(
                "Chegada",
                key="-BTN_CHEGADA-",
                size=(10, 1),
            ),
            sg.Button(
                "Pedir",
                key="-BTN_PEDIR-",
                size=(10, 1),
            ),
            sg.Button(
                "Confirmar",
                key="-BTN_CONFIRMAR-",
                size=(10, 1),
                button_color=("white", "#00796B"),
            ),
            sg.Button(
                "Pronto",
                key="-BTN_PRONTO-",
                size=(10, 1),
            ),
            sg.Button(
                "Entregar",
                key="-BTN_ENTREGAR-",
                size=(10, 1),
            ),
            sg.Button(
                "Finalizar",
                key="-BTN_FINALIZAR-",
                size=(10, 1),
                button_color=("white", "#F9A825"),
            ),
            sg.Button(
                "Limpar Mesa",
                key="-BTN_LIMPAR-",
                size=(11, 1),
            ),
            sg.Button(
                "Auto Alocar",
                key="-BTN_AUTO-",
                size=(11, 1),
            ),
            sg.Button(
                "Atualizar",
                key="-BTN_ATUALIZAR-",
                size=(10, 1),
            ),
        ]

        status_row = [
            sg.Text(
                "",
                key="-STATUS-",
                size=(90, 1),
                text_color="#FFEB3B",
            )
        ]

        layout = [
            header_row,
            [sg.HorizontalSeparator()],
            [
                col_esquerda,
                sg.VSeparator(),
                col_direita,
            ],
            [sg.HorizontalSeparator()],
            [actions_row],
            [status_row],
        ]

        self.window = sg.Window(
            "Automação de Restaurante",
            layout,
            finalize=True,
            resizable=True,
            size=(1100, 650),
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
