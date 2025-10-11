from controllers.restaurante_controller import RestauranteController
from views.console_view import ConsoleView

if __name__ == "__main__":
    ConsoleView(RestauranteController()).loop()