from __future__ import annotations
from typing import List, TYPE_CHECKING
from models.funcionario import Funcionario
from models.pedido import Pedido
from models.status_enums import StatusPedido

class Cozinheiro(Funcionario):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        super().__init__(id_funcionario, nome, salario_base)
        self._pedidos_em_preparo: List[Pedido] = []

    @property
    def pedidos_em_preparo(self) -> List[Pedido]:
        return self._pedidos_em_preparo.copy()

    def iniciar_preparo_pedido(self, pedido) -> bool:
        if pedido.iniciar_preparo():
            self._pedidos_em_preparo.append(pedido)
            return True
        return False

    def finalizar_preparo_pedido(self, pedido) -> bool:
        if pedido in self._pedidos_em_preparo and pedido.finalizar_preparo():
            self._pedidos_em_preparo.remove(pedido)
            return True
        return False

    def calcular_pagamento(self) -> float: 
        return self.salario_base
    
    def exibir_dados(self) -> str: 
        info_base = super().exibir_dados()
        pedidos_str = ", ".join(str(p.id_pedido) for p in self._pedidos_em_preparo)
        info_pedidos = f"\nPedidos em Preparo: [{pedidos_str}]"
        return f"--- Cozinheiro ---\n{info_base}{info_pedidos}"