import FreeSimpleGUI as sg
from typing import Any, Optional, List

class GuiEquipeView:
    def __init__(self, funcionario_controller: Any):
        self._func_ctrl = funcionario_controller
        sg.theme("DarkTeal9") 

    def show_equipe_window(self) -> None:
        data = self._func_ctrl.listar_funcionarios_para_view_gui()
        cols = ["ID", "Nome", "Função", "Salário", "Status/Mesas", "Gorjetas"]
        
        tbl_equipe = sg.Table(
            values=data,
            headings=cols,
            key="-TBL_EQUIPE-",
            justification="left",
            auto_size_columns=False,
            col_widths=[5, 20, 10, 12, 15, 10],
            display_row_numbers=False,
            enable_events=True,
            num_rows=12,
            expand_x=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE
        )

        frame_inputs = sg.Frame("Dados do Funcionário (Novo ou Edição)", [
            [
                sg.Text("Nome:"), sg.Input(key="-NOME-", size=(25,1)),
                sg.Text("Salário:"), sg.Input(key="-SALARIO-", size=(10,1)),
            ],
            [
                sg.Text("Ações:", font=("Helvetica", 9, "bold")),
                sg.Button("Contratar Garçom", key="-BTN_ADD_GARCOM-"),
                sg.Button("Contratar Cozinheiro", key="-BTN_ADD_COZINHEIRO-"),
                sg.VSeparator(),
                sg.Button("Atualizar Dados", key="-BTN_UPDATE-", disabled=True, button_color="#f0ad4e"), 
            ]
        ], expand_x=True)

        layout = [
            [sg.Text("Gerenciamento de Equipe", font=("Helvetica", 16, "bold"))],
            [tbl_equipe],
            [frame_inputs],
            [
                sg.Button("🗑️ Demitir Selecionado", key="-BTN_DEMITIR-", button_color="#d9534f", disabled=True),
                sg.Push(), 
                sg.Button("Fechar", key="-BTN_FECHAR-")
            ],
            [sg.Text("", key="-STATUS-", size=(50,1), text_color="yellow")]
        ]

        window = sg.Window("Equipe", layout, modal=True, finalize=True)

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "-BTN_FECHAR-"):
                break

            try:
                if event == "-TBL_EQUIPE-":
                    selecao = values.get("-TBL_EQUIPE-")
                    
                    if selecao:
                        idx = selecao[0] 
                        current_data = self._func_ctrl.listar_funcionarios_para_view_gui()
                        
                        if idx < len(current_data):
                            row_data = current_data[idx]
                            
                            nome_atual = row_data[1]
                            salario_str = str(row_data[3]).replace("R$ ", "").strip()
                            
                            window["-NOME-"].update(nome_atual)
                            window["-SALARIO-"].update(salario_str)
                            window["-BTN_DEMITIR-"].update(disabled=False)
                            window["-BTN_UPDATE-"].update(disabled=False)
                        else:
                            window["-TBL_EQUIPE-"].update(values=current_data)
                    else:
                        window["-BTN_DEMITIR-"].update(disabled=True)
                        window["-BTN_UPDATE-"].update(disabled=True)
                        window["-NOME-"].update("")
                        window["-SALARIO-"].update("")

                elif event in ("-BTN_ADD_GARCOM-", "-BTN_ADD_COZINHEIRO-"):
                    nome = values["-NOME-"]
                    sal_str = values["-SALARIO-"]
                    
                    if not nome or not sal_str:
                        window["-STATUS-"].update("Preencha nome e salário!")
                        continue
                        
                    salario = float(str(sal_str).replace(",", "."))
                    
                    if event == "-BTN_ADD_GARCOM-":
                        self._func_ctrl.contratar_garcom(nome, salario)
                        msg = f"Garçom {nome} contratado."
                    else:
                        self._func_ctrl.contratar_cozinheiro(nome, salario)
                        msg = f"Cozinheiro {nome} contratado."
                    
                    window["-TBL_EQUIPE-"].update(values=self._func_ctrl.listar_funcionarios_para_view_gui())
                    window["-NOME-"].update("")
                    window["-SALARIO-"].update("")
                    window["-STATUS-"].update(msg, text_color="green")

                elif event == "-BTN_UPDATE-":
                    selecao = values.get("-TBL_EQUIPE-")
                    if not selecao: continue

                    current_data = self._func_ctrl.listar_funcionarios_para_view_gui()
                    idx = selecao[0]
                    
                    if idx < len(current_data):
                        id_func = current_data[idx][0]
                        
                        novo_nome = values["-NOME-"]
                        novo_salario_str = values["-SALARIO-"]

                        if not novo_nome or not novo_salario_str:
                             sg.popup_error("Nome e Salário não podem estar vazios.")
                             continue

                        novo_salario = float(str(novo_salario_str).replace(",", "."))
                        
                        self._func_ctrl.atualizar_nome(id_func, novo_nome)
                        self._func_ctrl.atualizar_salario(id_func, novo_salario)
                        
                        window["-STATUS-"].update(f"Funcionário {id_func} atualizado!", text_color="green")
                        window["-TBL_EQUIPE-"].update(values=self._func_ctrl.listar_funcionarios_para_view_gui())

                elif event == "-BTN_DEMITIR-":
                    selecao = values.get("-TBL_EQUIPE-")
                    if not selecao: continue
                    
                    idx = selecao[0]
                    current_data = self._func_ctrl.listar_funcionarios_para_view_gui()

                    if idx < len(current_data):
                        id_func = current_data[idx][0]
                        
                        func_removido = self._func_ctrl.demitir_funcionario(id_func)
                        
                        window["-TBL_EQUIPE-"].update(values=self._func_ctrl.listar_funcionarios_para_view_gui())
                        window["-BTN_DEMITIR-"].update(disabled=True)
                        window["-BTN_UPDATE-"].update(disabled=True)
                        window["-NOME-"].update("")
                        window["-SALARIO-"].update("")
                        window["-STATUS-"].update(f"{func_removido.nome} foi demitido.", text_color="red")

            except ValueError as ve:
                sg.popup_error(f"Erro de valor: {ve}")
            except Exception as e:
                sg.popup_error(f"Erro inesperado: {e}")

        window.close()