# views/gui_cardapio_view.py
import FreeSimpleGUI as sg
from typing import Any

class GuiCardapioView:
    def __init__(self, cardapio_controller: Any):
        self._cardapio_ctrl = cardapio_controller
        sg.theme("DarkTeal9")

    def show_cardapio_window(self) -> None:
        def refresh_data():
            return self._cardapio_ctrl.get_dados_tabela()

        cols = ["ID", "Nome do Prato", "Preço"]
        
        tbl_cardapio = sg.Table(
            values=refresh_data(),
            headings=cols,
            key="-TBL_MENU-",
            justification="left",
            auto_size_columns=False,
            col_widths=[5, 30, 10],
            display_row_numbers=False,
            enable_events=True,
            num_rows=12,
            expand_x=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE
        )

        frame_inputs = sg.Frame("Editar / Adicionar Item", [
            [
                sg.Text("ID:", size=(3,1)), sg.Input(key="-ID-", size=(5,1)),
                sg.Text("Nome:"), sg.Input(key="-NOME-", size=(20,1), expand_x=True),
                sg.Text("Preço:"), sg.Input(key="-PRECO-", size=(8,1)),
            ],
            [
                sg.Text("Descrição (apenas p/ novos):"), 
                sg.Input(key="-DESC-", size=(30,1), expand_x=True)
            ],
            [
                sg.Button("➕ Adicionar Novo", key="-BTN_ADD-"),
                sg.Button("💾 Salvar Alteração", key="-BTN_EDIT-", disabled=True, button_color="#f0ad4e"),
                sg.Button("🗑️ Remover Item", key="-BTN_DEL-", button_color="#d9534f", disabled=True)
            ]
        ], expand_x=True)

        layout = [
            [sg.Text("Gerenciamento do Cardápio", font=("Helvetica", 14, "bold"))],
            [tbl_cardapio],
            [frame_inputs],
            [sg.Button("Fechar", key="-BTN_FECHAR-"), sg.Text("", key="-STATUS-", text_color="yellow")]
        ]

        window = sg.Window("Cardápio", layout, modal=True, finalize=True)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-BTN_FECHAR-"):
                break

            try:
                if event == "-TBL_MENU-":
                    selecao = values.get("-TBL_MENU-")
                    if selecao:
                        idx = selecao[0]
                        current_data = refresh_data()
                        
                        if idx < len(current_data):
                            row = current_data[idx] 
                            
                            window["-ID-"].update(row[0])
                            window["-ID-"].update(disabled=True) 
                            window["-NOME-"].update(row[1])
                            
                            preco_limpo = str(row[2]).replace("R$ ", "").replace(",", ".")
                            window["-PRECO-"].update(preco_limpo)
                            
                            window["-BTN_EDIT-"].update(disabled=False)
                            window["-BTN_DEL-"].update(disabled=False)
                            window["-BTN_ADD-"].update(disabled=True)
                    else:
                        window["-ID-"].update(disabled=False, value="")
                        window["-NOME-"].update("")
                        window["-PRECO-"].update("")
                        window["-DESC-"].update("")
                        window["-BTN_EDIT-"].update(disabled=True)
                        window["-BTN_DEL-"].update(disabled=True)
                        window["-BTN_ADD-"].update(disabled=False)

                elif event == "-BTN_ADD-":
                    id_p = int(values["-ID-"])
                    nome = values["-NOME-"]
                    preco = float(values["-PRECO-"].replace(",", "."))
                    desc = values["-DESC-"] or "Sem descrição"

                    self._cardapio_ctrl.adicionar_novo_prato(id_p, nome, preco, desc)
                    
                    window["-STATUS-"].update(f"Prato '{nome}' adicionado!", text_color="green")
                    window["-TBL_MENU-"].update(values=refresh_data())
                    
                    window["-ID-"].update("")
                    window["-NOME-"].update("")
                    window["-PRECO-"].update("")
                    window["-DESC-"].update("")

                elif event == "-BTN_EDIT-":
                    id_p = int(values["-ID-"]) 
                    nome = values["-NOME-"]
                    preco = float(values["-PRECO-"].replace(",", "."))
                    
                    self._cardapio_ctrl.atualizar_prato(id_p, nome, preco)
                    
                    window["-STATUS-"].update(f"Prato {id_p} atualizado.", text_color="green")
                    window["-TBL_MENU-"].update(values=refresh_data())
                    
                    window["-ID-"].update(disabled=False, value="")
                    window["-NOME-"].update("")
                    window["-PRECO-"].update("")
                    window["-BTN_EDIT-"].update(disabled=True)
                    window["-BTN_DEL-"].update(disabled=True)
                    window["-BTN_ADD-"].update(disabled=False)

                elif event == "-BTN_DEL-":
                    id_p = int(values["-ID-"])
                    self._cardapio_ctrl.remover_prato(id_p)
                    window["-STATUS-"].update(f"Prato {id_p} removido.", text_color="red")
                    window["-TBL_MENU-"].update(values=refresh_data())
                    window["-ID-"].update(disabled=False, value="")
                    window["-NOME-"].update("")
                    window["-PRECO-"].update("")
                    window["-BTN_EDIT-"].update(disabled=True)
                    window["-BTN_DEL-"].update(disabled=True)
                    window["-BTN_ADD-"].update(disabled=False)

            except ValueError as ve:
                sg.popup_error(f"Erro de valor (verifique ID e Preço): {ve}")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        window.close()