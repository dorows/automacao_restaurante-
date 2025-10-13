from __future__ import annotations
from typing import List, TYPE_CHECKING
from .funcionario import Funcionario
from .pedido import Pedido
from .status_enums import StatusPedido

class Cozinheiro(Funcionario):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        super().__init__(id_funcionario, nome, salario_base)
        self._pedidos_em_preparo: List[Pedido] = []

    @property
    def pedidos_em_preparo(self) -> List[Pedido]:
        return self._pedidos_em_preparo.copy()

    def iniciar_preparo_pedido(self, pedido: Pedido) -> None: 
        if not isinstance(pedido, Pedido):
            raise TypeError("Apenas objetos da classe Pedido podem ser preparados.")
        
        if pedido in self._pedidos_em_preparo:
            raise ValueError(f"O Cozinheiro {self.nome} já está preparando o Pedido {pedido.id_pedido}.")

        if pedido.iniciar_preparo():
            self._pedidos_em_preparo.append(pedido)
        else:
            raise ValueError(f"Não foi possível iniciar o preparo do Pedido {pedido.id_pedido} (status atual: {pedido.status.value}).")

    def finalizar_preparo_pedido(self, pedido: Pedido) -> None: 
        if not isinstance(pedido, Pedido):
            raise TypeError("Apenas objetos da classe Pedido podem ser finalizados.")

        if pedido not in self._pedidos_em_preparo:
            raise ValueError(f"O Cozinheiro {self.nome} não está preparando o Pedido {pedido.id_pedido}.")

        if pedido.finalizar_preparo():
            self._pedidos_em_preparo.remove(pedido)
        else:
            raise ValueError(f"Não foi possível finalizar o preparo do Pedido {pedido.id_pedido} (status atual: {pedido.status.value}).")

    def calcular_pagamento(self) -> float: 
        return self._salario_base
    
    def exibir_dados(self) -> str: 
        info_base = super().exibir_dados()
        pedidos_str = ", ".join(str(p.id_pedido) for p in self._pedidos_em_preparo)
        info_pedidos = f"\nPedidos em Preparo: [{pedidos_str}]"
        return f"--- Cozinheiro ---\n{info_base}{info_pedidos}"