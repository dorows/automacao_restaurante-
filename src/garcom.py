from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mesa import Mesa
from funcionario import Funcionario

class Garcom(Funcionario):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        super().__init__(id_funcionario, nome, salario_base)
        self._gorjetas: float = 0.0
        self.__mesas_atendidas: list[Mesa] = []

    @property
    def mesas_atendidas(self) -> list[Mesa]:
        return self.__mesas_atendidas.copy()

    def adicionar_mesa(self, mesa: Mesa) -> bool:
        if len(self.__mesas_atendidas) < 4:
            self.__mesas_atendidas.append(mesa)
            return True
        else:
            print(f"Aviso: O garçom {self.nome} já atingiu o limite de 4 mesas.")
            return False

    def remover_mesa(self, mesa: Mesa):
        # Remove uma mesa da responsabilidade do garçom.
        if mesa in self.__mesas_atendidas:
            self.__mesas_atendidas.remove(mesa)

    def calcular_pagamento(self) -> float:
        return self._salario_base + self._gorjetas

    def exibir_dados(self) -> str:
        info_base = super().exibir_dados()
        info_especifica = f"\nGorjetas: R${self._gorjetas:.2f}"
        
        mesas_str = ", ".join(str(m.id_mesa) for m in self.__mesas_atendidas)
        info_mesas = f"\nMesas Atendidas: [{mesas_str}]"
        
        return f"--- Garçom ---\n{info_base}{info_especifica}{info_mesas}"