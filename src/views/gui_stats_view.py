# views/gui_stats_view.py

import FreeSimpleGUI as sg
from typing import Any, List
import datetime

class GuiStatsView:
    def __init__(self, restaurante_controller: Any):
        self._restaurante = restaurante_controller
        sg.theme("DarkBlue3")

    def show_stats_window(self) -> None:
        dados_prato = self._restaurante.ver_prato_mais_pedido()
        nome_prato = dados_prato.get("prato_nome", "N/A")
        qtd_prato = dados_prato.get("quantidade", 0)

        dados_garcons = self._restaurante.obter_dados_relatorio_equipe()

        valores_tabela = []
        for g in dados_garcons:
            valores_tabela.append([
                g['id'],
                g['nome'],
                g['mesas'],
                f"R$ {g['total_gorjetas']:.2f}",
                f"R$ {g['media_por_mesa']:.2f}"
            ])


        layout_destaque = [
            [sg.Text("Prato Mais Popular:", font=("Arial", 10, "bold"))],
            [sg.Text(f"{nome_prato}", font=("Helvetica", 16, "bold"), text_color="gold")],
            [sg.Text(f"Vendido {qtd_prato} vezes", font=("Arial", 10, "italic"))]
        ]

        # Área da Tabela (Relatório)
        cols = ["ID", "Garçom", "Mesas Atend.", "Total Gorjetas", "Média/Mesa"]
        tabela_relatorio = sg.Table(
            values=valores_tabela,
            headings=cols,
            auto_size_columns=False,
            col_widths=[5, 15, 12, 15, 12],
            justification="center",
            num_rows=8,
            key="-TBL_RELATORIO-",
            expand_x=True
        )

        layout_relatorio = [
            [sg.Text("Ranking de Desempenho (Garçons)", font=("Arial", 12, "bold"))],
            [tabela_relatorio],
            [sg.Text("Ordenado por arrecadação de gorjetas", font=("Arial", 8), text_color="gray")]
        ]

        layout = [
            [sg.Text("Relatórios e Estatísticas", font=("Arial", 18, "bold"), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_destaque, element_justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Frame("Relatório da Equipe", layout_relatorio, expand_x=True)],
            [sg.HorizontalSeparator()],
            [
                sg.Button("Exportar para TXT", key="-BTN_EXPORTAR-"),
                sg.Push(),
                sg.Button("Fechar", key="-BTN_FECHAR-")
            ]
        ]

        window = sg.Window("Central de Relatórios", layout, modal=True, finalize=True, size=(600, 500))

        while True:
            event, _ = window.read()
            
            if event in (sg.WIN_CLOSED, "-BTN_FECHAR-"):
                break

            if event == "-BTN_EXPORTAR-":
                self._exportar_arquivo(dados_prato, dados_garcons)

        window.close()

    def _exportar_arquivo(self, dados_prato: dict, dados_garcons: List[dict]) -> None:
        try:
            filename = f"relatorio_restaurante_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("="*40 + "\n")
                f.write(f"RELATÓRIO DE DESEMPENHO - {datetime.datetime.now()}\n")
                f.write("="*40 + "\n\n")
                
                f.write("1. DESTAQUE DO CARDÁPIO\n")
                f.write(f"- Prato: {dados_prato.get('prato_nome')}\n")
                f.write(f"- Vendas: {dados_prato.get('quantidade')}\n\n")
                
                f.write("2. RANKING DE GARÇONS\n")
                f.write(f"{'ID':<5} | {'NOME':<15} | {'MESAS':<6} | {'GORJETAS':<10}\n")
                f.write("-" * 45 + "\n")
                
                for g in dados_garcons:
                    f.write(f"{g['id']:<5} | {g['nome']:<15} | {g['mesas']:<6} | R$ {g['total_gorjetas']:.2f}\n")
                
                f.write("\n" + "="*40)
            
            sg.popup(f"Relatório salvo com sucesso!\nArquivo: {filename}", title="Sucesso")
            
        except Exception as e:
            sg.popup_error(f"Erro ao salvar arquivo: {e}")