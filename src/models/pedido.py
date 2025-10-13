from __future__ import annotations
from typing import List, TYPE_CHECKING
from datetime import datetime
from .item_pedido import ItemPedido
from .status_enums import StatusPedido

if TYPE_CHECKING:
    from .mesa import Mesa
    from .garcom import Garcom
    from .grupo_cliente import GrupoCliente

class Pedido:
    _proximo_id = 1

    def __init__(self, mesa: Mesa, garcom: Garcom, grupo_cliente: GrupoCliente):
        from .mesa import Mesa
        from .garcom import Garcom
        from .grupo_cliente import GrupoCliente

        if not isinstance(mesa, Mesa):
            raise TypeError("O pedido deve estar associado a um objeto Mesa válido.")
        if not isinstance(garcom, Garcom):
            raise TypeError("O pedido deve estar associado a um objeto Garcom válido.")
        if not isinstance(grupo_cliente, GrupoCliente):
            raise TypeError("O pedido deve estar associado a um objeto GrupoCliente válido.")

        self._id_pedido: int = Pedido._proximo_id
        self._mesa: Mesa = mesa
        self._garcom: Garcom = garcom
        self._grupo_cliente: grupo_cliente
        self._data_hora: datetime = datetime.now()
        self._status: StatusPedido = StatusPedido.ABERTO
        self._itens: List[ItemPedido] = []
        
        Pedido._proximo_id += 1

    @property
    def id_pedido(self) -> int: return self._id_pedido
    @property
    def mesa(self) -> Mesa: return self._mesa
    @property
    def status(self) -> StatusPedido: return self._status
    @property
    def itens(self) -> List[ItemPedido]: return self._itens.copy()

    def adicionar_item(self, item: ItemPedido) -> None:
        if not isinstance(item, ItemPedido):
            raise TypeError("Apenas um objeto ItemPedido pode ser adicionado.")
        if self.status != StatusPedido.ABERTO:
            raise ValueError(f"Não é possível adicionar itens ao Pedido {self.id_pedido}, pois seu status é '{self.status.value}'.")
        self._itens.append(item)

    def calcular_subtotal_pedido(self) -> float:
        return sum(item.calcular_subtotal() for item in self._itens)

    def confirmar(self) -> None:
        if self.status != StatusPedido.ABERTO:
            raise ValueError(f"Apenas um pedido 'Aberto' pode ser confirmado (status atual: '{self.status.value}').")
        if not self.itens:
            raise ValueError("Não é possível confirmar um pedido vazio.")
        self._status = StatusPedido.CONFIRMADO

    def iniciar_preparo(self) -> None:
        if self.status != StatusPedido.CONFIRMADO:
            raise ValueError(f"Apenas um pedido 'Confirmado' pode iniciar o preparo (status atual: '{self.status.value}').")
        self._status = StatusPedido.EM_PREPARO

    def finalizar_preparo(self) -> None:
        if self.status != StatusPedido.EM_PREPARO:
            raise ValueError(f"Apenas um pedido 'Em Preparo' pode ser finalizado (status atual: '{self.status.value}').")
        self._status = StatusPedido.PRONTO

    def entregar_pedido(self) -> None:
        if self.status != StatusPedido.PRONTO:
            raise ValueError(f"Apenas um pedido 'Pronto' pode ser entregue (status atual: '{self.status.value}').")
        self._status = StatusPedido.ENTREGUE

    def __str__(self) -> str:
        return (f"Pedido ID: {self.id_pedido} (Mesa: {self.mesa.id_mesa}) | "
                f"Status: {self.status.value} | "
                f"Total: R$ {self.calcular_subtotal_pedido():.2f}")