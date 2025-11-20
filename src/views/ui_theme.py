# ui_theme.py
import FreeSimpleGUI as sg

def configure_global_ui():
    # Tema base (escuro, neutro)
    sg.theme("DarkGrey13")

    # Estilos padrão para todos os elementos
    sg.set_options(
        font=("Segoe UI", 11),
        element_padding=(4, 4),
        button_color=("white", "#1976D2"),
        input_elements_background_color="#1E2933",
        text_element_background_color=sg.theme_background_color(),
        text_color="white",
    )
