from funcionario import Funcionario

class Garcom(Funcionario):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        super().__init__(id_funcionario, nome, salario_base)
        self._gorjetas: float = 0.0

    def adicionar_gorjeta(self, valor: float):
        if valor > 0:
            self._gorjetas += valor

    def calcular_pagamento(self) -> float:
        return self._salario_base + self._gorjetas

    def exibir_dados(self) -> str:
        info_base = super().exibir_dados()
        info_especifica = f"\nGorjetas: R${self._gorjetas:.2f}"
        return f"--- Garçom ---\n{info_base}{info_especifica}"