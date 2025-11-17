from __future__ import annotations
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .mesa import Mesa
from .funcionario import Funcionario

class Garcom(Funcionario):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        super().__init__(id_funcionario, nome, salario_base)
        self._gorjetas: float = 0.0
        self._mesas_atendidas: List[Mesa] = []

    @property
    def mesas_atendidas(self) -> List[Mesa]:
        return self._mesas_atendidas.copy()

    def adicionar_gorjeta(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O valor da gorjeta deve ser um número não negativo.")
        self._gorjetas += valor

    def adicionar_mesa(self, mesa: Mesa) -> None:
        from .mesa import Mesa 
        
        if not isinstance(mesa, Mesa):
            raise TypeError("Apenas objetos da classe Mesa podem ser adicionados.")
        
        if len(self._mesas_atendidas) >= 4:
            raise ValueError(f"O Garçom {self.__nome} já atingiu o limite de 4 mesas.")
            
        if mesa in self._mesas_atendidas:
            raise ValueError(f"O Garçom {self.__nome} já está atendendo a Mesa {mesa.id_mesa}.")

        self._mesas_atendidas.append(mesa)

    def remover_mesa(self, mesa: Mesa) -> None:
        from .mesa import Mesa

        if not isinstance(mesa, Mesa):
            raise TypeError("Apenas objetos da classe Mesa podem ser removidos.")

        if mesa not in self._mesas_atendidas:
            raise ValueError(f"O Garçom {self.__nome} não está atendendo a Mesa {mesa.id_mesa}.")
            
        self._mesas_atendidas.remove(mesa)

    def calcular_pagamento(self) -> float:
        return self.__salario_base + self._gorjetas

    def exibir_dados(self) -> str:
        info_base = super().exibir_dados()
        info_especifica = f"\nGorjetas: R${self._gorjetas:.2f}"
        
        mesas_str = ", ".join(str(m.id_mesa) for m in self._mesas_atendidas)
        info_mesas = f"\nMesas Atendidas: [{mesas_str}]"
        
        return f"--- Garçom ---\n{info_base}{info_especifica}{info_mesas}"