from prato import Prato

class ItemPedido:
    # representa um único item dentro de uma conta, como '2x Refrigerante'
    
    def __init__(self, prato: Prato, quantidade: int, observacao: str = ""):
        self.__prato = prato
        self.__quantidade = quantidade
        self.__observacao = observacao

    @property
    def prato(self) -> Prato:
        return self.__prato

    @property
    def quantidade(self) -> int:
        return self.__quantidade

    def calcular_subtotal(self) -> float:
        """Calcula o preço do prato multiplicado pela quantidade."""
        return self.prato.preco * self.quantidade

    def __str__(self) -> str:
        subtotal = self.calcular_subtotal()
        return f"{self.quantidade}x {self.prato.nome} - R$ {subtotal:.2f}"