from item_pedido import ItemPedido


class Pedido:

    _proximo_id = 1 # Variável de classe para gerar IDs únicos

    def __init__(self):
        self.__id_pedido = Pedido._proximo_id
        self.__itens: list[ItemPedido] = []
        Pedido._proximo_id += 1

    @property
    def id_pedido(self) -> int:
        return self.__id_pedido

    @property
    def itens(self) -> list[ItemPedido]:
        return self.__itens

    def adicionar_item(self, item: ItemPedido):
        self.__itens.append(item)

    def calcular_subtotal_pedido(self) -> float:
        subtotal = 0.0
        for item in self.__itens:
            subtotal += item.calcular_subtotal()
        return subtotal

    def __str__(self) -> str:
        return f"Pedido ID: {self.id_pedido} - Subtotal: R$ {self.calcular_subtotal_pedido():.2f}"