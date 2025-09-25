from typing import Optional
from models.cardapio import Cardapio
from models.prato import Prato

class CardapioController:
    def __init__(self):
        self._cardapio = Cardapio()
        self._setup_inicial()

    def _setup_inicial(self):
        prato1 = Prato(id_prato=1, nome="Spaghetti alla Carbonara", preco=55.50, descricao="Massa com ovos, queijo pecorino e pancetta.")
        prato2 = Prato(id_prato=2, nome="Lasanha Bolonhesa", preco=62.00, descricao="Massa em camadas com molho à bolonhesa e queijo.")
        prato3 = Prato(id_prato=101, nome="Suco de Laranja", preco=12.00, descricao="500ml, natural.")
        prato4 = Prato(id_prato=102, nome="Água com Gás", preco=6.00, descricao="300ml.")

        self._cardapio.adicionar_prato(prato1)
        self._cardapio.adicionar_prato(prato2)
        self._cardapio.adicionar_prato(prato3)
        self._cardapio.adicionar_prato(prato4)

    def buscar_prato_por_id(self, id_prato: int) -> Optional[Prato]:

        return self._cardapio.buscar_prato_por_id(id_prato)

    @property
    def cardapio(self) -> Cardapio:
        return self._cardapio