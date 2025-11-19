import FreeSimpleGUI as sg
from typing import Any

class GuiMesaView:
    def __init__(self, restaurante_controller: Any, mesa_controller: Any):
        self._restaurante = restaurante_controller
        self._mesa_ctrl = mesa_controller
        sg.theme("DarkTeal9")

    def show_mesa_window(self) -> None:

        cols = ["ID Mesa", "Capacidade", "Status"]
        
        def get_data():
            mesas = self._mesa_ctrl.listar_mesas()

            mesas.sort(key=lambda m: m.id_mesa)
            return [[m.id_mesa, m.capacidade, m.status.value] for m in mesas]

        tbl_mesas = sg.Table(
            values=get_data(), headings=cols, key="-TBL_MESAS-",
            justification="center", auto_size_columns=False, col_widths=[10, 10, 15],
            display_row_numbers=False, enable_events=True, num_rows=10, expand_x=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE
        )

        layout = [
            [sg.Text("Gestão do Layout (Mesas)", font=("Helvetica", 14, "bold"))],
            [tbl_mesas],
            [sg.Frame("Editar / Criar", [
                [
                    sg.Text("ID Mesa:"), sg.Input(key="-ID-", size=(5,1)),
                    sg.Text("Capacidade:"), sg.Input(key="-CAP-", size=(5,1)),
                ],
                [
                    sg.Button("Adicionar Nova", key="-BTN_ADD-"),
                    sg.Button("Salvar Edição", key="-BTN_EDIT-", disabled=True),
                    sg.Button("Remover Selecionada", key="-BTN_DEL-", button_color="#d9534f", disabled=True)
                ]
            ])],
            [sg.Button("Fechar", key="-BTN_FECHAR-"), sg.Text("", key="-STATUS-", text_color="yellow")]
        ]

        window = sg.Window("Gerenciar Mesas", layout, modal=True, finalize=True)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-BTN_FECHAR-"):
                break

            try:

                if event == "-TBL_MESAS-":
                    selecao = values.get("-TBL_MESAS-")
                    
                    if selecao:
                        row_idx = selecao[0]
                        
                        current_data = get_data()
                        
                        if row_idx < len(current_data):
                            row_data = current_data[row_idx]
                            
                            window["-ID-"].update(row_data[0])
                            window["-CAP-"].update(row_data[1])
                            
                            window["-BTN_EDIT-"].update(disabled=False)
                            window["-BTN_DEL-"].update(disabled=False)
                            window["-BTN_ADD-"].update(disabled=True) 
                            window["-ID-"].update(disabled=True)
                        else:
                            window["-TBL_MESAS-"].update(values=get_data())
                            
                    else:
                        window["-BTN_EDIT-"].update(disabled=True)
                        window["-BTN_DEL-"].update(disabled=True)
                        window["-BTN_ADD-"].update(disabled=False)
                        window["-ID-"].update(disabled=False, value="")
                        window["-CAP-"].update(value="")


                elif event == "-BTN_ADD-":
                    id_mesa = int(values["-ID-"])
                    cap = int(values["-CAP-"])
                    self._restaurante.adicionar_mesa(id_mesa, cap)
                    window["-STATUS-"].update(f"Mesa {id_mesa} criada.")
                    window["-TBL_MESAS-"].update(values=get_data())
                    # Limpa inputs
                    window["-ID-"].update("")
                    window["-CAP-"].update("")


                elif event == "-BTN_EDIT-":
                    id_mesa = int(values["-ID-"]) 
                    cap = int(values["-CAP-"])
                    msg = self._restaurante.atualizar_mesa(id_mesa, cap)
                    window["-STATUS-"].update(msg)
                    window["-TBL_MESAS-"].update(values=get_data())
                    

                    window["-ID-"].update(disabled=False, value="")
                    window["-CAP-"].update("")
                    window["-BTN_EDIT-"].update(disabled=True)
                    window["-BTN_DEL-"].update(disabled=True)
                    window["-BTN_ADD-"].update(disabled=False)


                elif event == "-BTN_DEL-":
                    id_mesa = int(values["-ID-"])
                    msg = self._restaurante.remover_mesa(id_mesa)
                    window["-STATUS-"].update(msg)
                    window["-TBL_MESAS-"].update(values=get_data())
                    

                    window["-ID-"].update(disabled=False, value="")
                    window["-CAP-"].update("")
                    window["-BTN_EDIT-"].update(disabled=True)
                    window["-BTN_DEL-"].update(disabled=True)
                    window["-BTN_ADD-"].update(disabled=False)

            except ValueError as ve:
                sg.popup_error(f"Erro de valor: {ve}")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        window.close()