import FreeSimpleGUI as sg
from typing import Any, List
import datetime
from io import BytesIO

import matplotlib.pyplot as plt


class GuiStatsView:
    def __init__(self, restaurante_controller: Any):
        self._restaurante = restaurante_controller

        sg.theme("DarkBlue3")
        sg.set_options(font=("Segoe UI", 10))

    def show_stats_window(self) -> None:
        dados_prato = self._restaurante.ver_prato_mais_pedido()
        nome_prato = dados_prato.get("prato_nome", "N/A")
        qtd_prato = dados_prato.get("quantidade", 0)

        dados_garcons = self._restaurante.obter_dados_relatorio_equipe()

        valores_tabela: List[List[Any]] = []
        for g in dados_garcons:
            valores_tabela.append(
                [
                    g["id"],
                    g["nome"],
                    g["mesas"],
                    f"R$ {g['total_gorjetas']:.2f}",
                    f"R$ {g['media_por_mesa']:.2f}",
                ]
            )

        total_garcons = len(dados_garcons)
        total_mesas = sum(g["mesas"] for g in dados_garcons) if dados_garcons else 0
        total_gorjetas = (
            sum(g["total_gorjetas"] for g in dados_garcons) if dados_garcons else 0.0
        )

        layout_destaque_prato = [
            [
                sg.Text(
                    "Prato mais pedido",
                    font=("Segoe UI", 10, "bold"),
                    text_color="#A7C7FF",
                )
            ],
            [
                sg.Text(
                    nome_prato,
                    font=("Segoe UI", 16, "bold"),
                    text_color="gold",
                )
            ],
            [
                sg.Text(
                    f"Vendido {qtd_prato} vezes",
                    font=("Segoe UI", 10, "italic"),
                    text_color="#DDDDDD",
                )
            ],
        ]

        frame_destaque_prato = sg.Frame(
            "",
            [[sg.Column(layout_destaque_prato, element_justification="center")]],
            pad=(5, 5),
            relief=sg.RELIEF_RAISED,
            border_width=1,
        )

        # CARD: resumo da equipe 
        layout_resumo_equipe = [
            [
                sg.Text(
                    "Resumo da equipe",
                    font=("Segoe UI", 10, "bold"),
                    text_color="#A7C7FF",
                )
            ],
            [
                sg.Text(
                    f"Garçons ativos: {total_garcons}",
                    font=("Segoe UI", 10),
                )
            ],
            [
                sg.Text(
                    f"Mesas atendidas: {total_mesas}",
                    font=("Segoe UI", 10),
                )
            ],
            [
                sg.Text(
                    f"Total de gorjetas: R$ {total_gorjetas:.2f}",
                    font=("Segoe UI", 10),
                )
            ],
        ]

        frame_resumo_equipe = sg.Frame(
            "",
            [[sg.Column(layout_resumo_equipe, element_justification="left")]],
            pad=(5, 5),
            relief=sg.RELIEF_RAISED,
            border_width=1,
        )

        layout_cards_top = [
            [
                sg.Column(
                    [[frame_destaque_prato]],
                    expand_x=True,
                    pad=(0, 0),
                    justification="left",
                ),
                sg.Column(
                    [[frame_resumo_equipe]],
                    expand_x=True,
                    pad=(10, 0),
                    justification="right",
                ),
            ]
        ]

        cols = ["ID", "Garçom", "Mesas Atend.", "Total Gorjetas", "Média/Mesa"]
        tabela_relatorio = sg.Table(
            values=valores_tabela,
            headings=cols,
            auto_size_columns=False,
            col_widths=[5, 18, 12, 15, 12],
            justification="center",
            num_rows=min(len(valores_tabela), 10) if valores_tabela else 5,
            key="-TBL_RELATORIO-",
            expand_x=True,
            expand_y=True,
            alternating_row_color="#1B2838",
            enable_events=False,
            header_background_color="#005B96",
            header_text_color="white",
            row_height=22,
        )

        layout_relatorio = [
            [
                sg.Text(
                    "Ranking de desempenho (garçons)",
                    font=("Segoe UI", 12, "bold"),
                )
            ],
            [tabela_relatorio],
            [
                sg.Text(
                    "Ordenado por arrecadação de gorjetas",
                    font=("Segoe UI", 8),
                    text_color="gray",
                )
            ],
        ]

        frame_relatorio = sg.Frame(
            "Relatório da equipe",
            layout_relatorio,
            expand_x=True,
            expand_y=True,
            pad=(0, 5),
        )

        grafico_frame_layout = [
            [
                sg.Text(
                    "Pratos mais pedidos (gráfico)",
                    font=("Segoe UI", 12, "bold"),
                )
            ],
            [
                sg.Image(
                    key="-IMG_GRAFICO-",
                    size=(480, 320),
                    pad=(0, 5),
                )
            ],
            [
                sg.Button(
                    "Atualizar gráfico",
                    key="-BTN_GRAFICO_PRATOS-",
                    button_color=("white", "#005B96"),
                )
            ],
        ]

        frame_grafico = sg.Frame(
            "Visualização",
            grafico_frame_layout,
            expand_x=True,
            expand_y=True,
            pad=(10, 5),
        )

        layout = [
            [
                sg.Text(
                    "Central de Relatórios e Estatísticas",
                    font=("Segoe UI", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_cards_top, expand_x=True)],
            [sg.HorizontalSeparator()],
            [
                sg.Column(
                    [[frame_relatorio]],
                    expand_x=True,
                    expand_y=True,
                ),
                sg.VSeparator(),
                sg.Column(
                    [[frame_grafico]],
                    expand_x=True,
                    expand_y=True,
                ),
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Button(
                    "Exportar para TXT",
                    key="-BTN_EXPORTAR-",
                    button_color=("white", "#00897B"),
                ),
                sg.Push(),
                sg.Button(
                    "Fechar",
                    key="-BTN_FECHAR-",
                    button_color=("white", "#B71C1C"),
                ),
            ],
        ]

        window = sg.Window(
            "Central de Relatórios",
            layout,
            modal=True,
            finalize=True,
            resizable=True,
            size=(900, 550),
        )

        img_data_inicial = self._gerar_grafico_pratos()
        if img_data_inicial:
            window["-IMG_GRAFICO-"].update(data=img_data_inicial)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "-BTN_FECHAR-"):
                break

            if event == "-BTN_GRAFICO_PRATOS-":
                img_data = self._gerar_grafico_pratos()
                if img_data:
                    window["-IMG_GRAFICO-"].update(data=img_data)
                else:
                    sg.popup(
                        "Ainda não há dados suficientes para gerar o gráfico.",
                        title="Aviso",
                    )

            if event == "-BTN_EXPORTAR-":
                self._exportar_arquivo(dados_prato, dados_garcons)

        window.close()

    def _gerar_grafico_pratos(self) -> bytes:
        try:
            estatisticas = self._restaurante._pedido_controller.get_estatisticas_pratos()
        except AttributeError:
            return b""

        if not estatisticas:
            return b""

        nomes = [prato.nome for prato in estatisticas.keys()]
        quantidades = list(estatisticas.values())

        # Monta o gráfico
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(range(len(nomes)), quantidades)
        ax.set_xticks(range(len(nomes)))
        ax.set_xticklabels(nomes, rotation=45, ha="right")
        ax.set_ylabel("Quantidade vendida")
        ax.set_title("Pratos mais pedidos")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        plt.tight_layout()

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        return buf.read()

    def _exportar_arquivo(self, dados_prato: dict, dados_garcons: List[dict]) -> None:
        try:
            filename = (
                f"relatorio_restaurante_"
                f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 40 + "\n")
                f.write(
                    f"RELATÓRIO DE DESEMPENHO - {datetime.datetime.now()}\n"
                )
                f.write("=" * 40 + "\n\n")

                f.write("1. DESTAQUE DO CARDÁPIO\n")
                f.write(f"- Prato: {dados_prato.get('prato_nome')}\n")
                f.write(f"- Vendas: {dados_prato.get('quantidade')}\n\n")

                f.write("2. RANKING DE GARÇONS\n")
                f.write(
                    f"{'ID':<5} | {'NOME':<15} | {'MESAS':<6} | {'GORJETAS':<10}\n"
                )
                f.write("-" * 45 + "\n")

                for g in dados_garcons:
                    f.write(
                        f"{g['id']:<5} | {g['nome']:<15} | "
                        f"{g['mesas']:<6} | R$ {g['total_gorjetas']:.2f}\n"
                    )

                f.write("\n" + "=" * 40)

            sg.popup(
                f"Relatório salvo com sucesso!\nArquivo: {filename}",
                title="Sucesso",
            )

        except Exception as e:
            sg.popup_error(f"Erro ao salvar arquivo: {e}")
