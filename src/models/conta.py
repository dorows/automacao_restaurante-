from __future__ import annotations
from typing import List, TYPE_CHECKING

#evitar importação circular
if TYPE_CHECKING:
    from models.grupo_cliente import GrupoCliente
    from models.pedido import Pedido
    from models.mesa import Mesa

class Conta:
    def __init__(self, id_conta: int, grupo_cliente: GrupoCliente, mesa: Mesa):
        print('debugando conta.py nova versão')
        self._id_conta: int = id_conta
        self._grupo_cliente: GrupoCliente = grupo_cliente
        self._mesa: Mesa = mesa  
        self._pedidos: List[Pedido] = []
        self._aberta: bool = True

    @property
    def id_conta(self) -> int:
        return self._id_conta
    
    @property
    def grupo_cliente(self) -> GrupoCliente:
        return self._grupo_cliente

    @property
    def mesa(self) -> Mesa:
        return self._mesa

    @property
    def pedidos(self) -> List[Pedido]:
        return self._pedidos.copy()

    @property
    def esta_aberta(self) -> bool:
        return self._aberta

    def adicionar_pedido(self, pedido: Pedido) -> bool:
        if self.esta_aberta:
            self._pedidos.append(pedido)
            return True
        return False

    def calcular_total(self) -> float: 
        return sum(pedido.calcular_subtotal_pedido() for pedido in self._pedidos)

    def fechar(self): 
        self._aberta = False