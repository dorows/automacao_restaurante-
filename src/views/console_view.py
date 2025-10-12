from typing import List, Tuple, Dict

class ConsoleView:
    def print_lines(self, lines: List[str]) -> None:
        for ln in lines:
            print(ln)

    def clear(self) -> None:
        print("\033[2J\033[H", end="")

    def read_command(self) -> Tuple[str, List[str]]:
        raw = input("\n> ").strip()
        if not raw:
            return "", []
        parts = raw.split()
        return parts[0].lower(), parts[1:]

    def render_dashboard(self, dados: Dict[str, object]) -> None:
        print("\n--- Automação de Restaurante ---")
        # cabeçalho sucinto
        print(f"Mesas: {len(dados.get('mesas', []))}  |  "
              f"Fila: {len(dados.get('fila', []))}  |  "
              f"Garçons: {len(dados.get('garcons', []))}  |  "
              f"Pratos: {len(dados.get('cardapio', []))}")
    
    def _help_lines(self) -> List[str]:
        return [
            "",
            "Comandos disponíveis:",
            "  chegada <qtd>",
            "  pedir <mesa_id> <prato_id> <qtd>",
            "  confirmar <mesa_id>",
            "  pronto <mesa_id>",
            "  entregar <mesa_id>",
            "  finalizar <mesa_id>",
            "  limpar <mesa_id>",
            "  cardapio",
            "  equipe",
            "  contratar_garcom <nome> <salario>",
            "  contratar_cozinheiro <nome> <salario>",
            "  demitir <id_func>",
            "  adicionar_mesa <id> <capacidade>",
            "  ajuda | help | ?,"
            ""
        ]