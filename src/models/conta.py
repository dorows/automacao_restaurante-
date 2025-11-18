from __future__ import annotations
from typing import List, TYPE_CHECKING
from models.excecoes import ContaJaFechadaError
if TYPE_CHECKING:
    from .grupo_cliente import GrupoCliente
    from .pedido import Pedido
    from .mesa import Mesa

class Conta:
    def __init__(self, id_conta: int, grupo_cliente: GrupoCliente, mesa: Mesa):
        from .grupo_cliente import GrupoCliente
        from .mesa import Mesa

        if not isinstance(id_conta, int) or id_conta <= 0:
            raise ValueError("O ID da conta deve ser um número inteiro positivo.")
        if not isinstance(grupo_cliente, GrupoCliente):
            raise TypeError("O argumento 'grupo_cliente' deve ser um objeto da classe GrupoCliente.")
        if not isinstance(mesa, Mesa):
            raise TypeError("O argumento 'mesa' deve ser um objeto da classe Mesa.")

        self._id_conta: int = id_conta
        self._grupo_cliente: GrupoCliente = grupo_cliente
        self._mesa: Mesa = mesa
        self._pedidos: List[Pedido] = []
        self._aberta: bool = True

    @property
    def id_conta(self) -> int: return self._id_conta
    @property
    def grupo_cliente(self) -> GrupoCliente: return self._grupo_cliente
    @property
    def mesa(self) -> Mesa: return self._mesa
    @property
    def pedidos(self) -> List[Pedido]: return self._pedidos.copy()
    @property
    def esta_aberta(self) -> bool: return self._aberta

    def adicionar_pedido(self, pedido: Pedido) -> None:
        from .pedido import Pedido

        if not isinstance(pedido, Pedido):
            raise TypeError("Apenas objetos da classe Pedido podem ser adicionados à conta.")
        if not self.esta_aberta:
            raise ContaJaFechadaError(f"Não é possível adicionar pedidos à conta {self.id_conta}, pois ela está fechada.")
        
        self._pedidos.append(pedido)

    def calcular_total(self) -> float: 
        return sum(p.calcular_subtotal_pedido() for p in self._pedidos)

    def fechar(self) -> None:
        if not self.esta_aberta:
            raise ContaJaFechadaError(f"A conta {self.id_conta} já se encontra fechada.")
        self._aberta = False