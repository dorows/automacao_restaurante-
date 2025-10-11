from __future__ import annotations
from typing import List, TYPE_CHECKING
from datetime import datetime
from models.item_pedido import ItemPedido
from models.status_enums import StatusPedido

# Evita importação circular
if TYPE_CHECKING:
    from models.mesa import Mesa
    from models.garcom import Garcom
    from models.grupo_cliente import GrupoCliente

class Pedido:
    _proximo_id = 1

    def __init__(self, mesa: Mesa, garcom: Garcom, grupo_cliente: GrupoCliente):
        self._id_pedido: int = Pedido._proximo_id
        self._mesa: Mesa = mesa
        self._garcom: Garcom = garcom
        self._grupo_cliente: GrupoCliente = grupo_cliente
        self._data_hora: datetime = datetime.now()
        self._status: StatusPedido = StatusPedido.ABERTO
        self._itens: List[ItemPedido] = []
        
        Pedido._proximo_id += 1

    @property
    def id_pedido(self) -> int:
        return self._id_pedido

    @property
    def mesa(self) -> Mesa:
        return self._mesa
    
    @property
    def status(self) -> StatusPedido:
        return self._status

    @property
    def itens(self) -> List[ItemPedido]:
        return self._itens.copy()

    def adicionar_item(self, item: ItemPedido) -> bool:
        if self.status == StatusPedido.ABERTO:
            self._itens.append(item)
            return True
        return False

    def calcular_subtotal_pedido(self) -> float:
        return sum(item.calcular_subtotal() for item in self._itens)

    def confirmar(self) -> bool:
        if self.status == StatusPedido.ABERTO and self.itens:
            self._status = StatusPedido.CONFIRMADO
            return True
        return False

    def iniciar_preparo(self) -> bool:
        if self.status == StatusPedido.CONFIRMADO:
            self._status = StatusPedido.EM_PREPARO
            return True
        return False

    def finalizar_preparo(self) -> bool:
        if self.status == StatusPedido.EM_PREPARO:
            self._status = StatusPedido.PRONTO
            return True
        return False

    def entregar_pedido(self) -> bool:
        if self.status == StatusPedido.PRONTO:
            self._status = StatusPedido.ENTREGUE
            return True
        return False

    def __str__(self) -> str:
        return (f"Pedido ID: {self.id_pedido} (Mesa: {self.mesa.id_mesa}) | "
                f"Status: {self.status.value} | "
                f"Total: R$ {self.calcular_subtotal_pedido():.2f}")