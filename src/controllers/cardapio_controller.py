from typing import Optional, Tuple
from models.cardapio import Cardapio
from models.prato import Prato

class CardapioController:
    def __init__(self):
        self._cardapio = Cardapio()
        self._setup_inicial()

    def _setup_inicial(self):
        pratos_iniciais = [
            (1, "Spaghetti alla Carbonara", 55.50, "Massa com ovos, queijo pecorino e pancetta."),
            (2, "Lasanha Bolonhesa", 62.00, "Massa em camadas com molho à bolonhesa e queijo."),
            (101, "Suco de Laranja", 12.00, "500ml, natural."),
            (102, "Água com Gás", 6.00, "300ml.")
        ]
        
        for id_p, nome_p, preco_p, desc_p in pratos_iniciais:
            try:
                prato = Prato(id_prato=id_p, nome=nome_p, preco=preco_p, descricao=desc_p)
                self._cardapio.adicionar_prato(prato)
            except (ValueError, TypeError) as e:
                print(f"[AVISO DE INICIALIZAÇÃO] Não foi possível adicionar o prato '{nome_p}': {e}")


    def adicionar_novo_prato(self, id_prato: int, nome: str, preco: float, descricao: str) -> Tuple[bool, str]:
        try:
            novo_prato = Prato(id_prato, nome, preco, descricao)
            self._cardapio.adicionar_prato(novo_prato)
            return True, f"Prato '{nome}' adicionado com sucesso."

        except (ValueError, TypeError) as e:
            return False, str(e)


    def buscar_prato_por_id(self, id_prato: int) -> Optional[Prato]:
        return self._cardapio.buscar_prato_por_id(id_prato)

    @property
    def cardapio(self) -> Cardapio:
        return self._cardapio