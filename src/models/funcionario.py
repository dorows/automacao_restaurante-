from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        if not isinstance(id_funcionario, int) or id_funcionario <= 0:
            raise ValueError("O ID do funcionário deve ser um número inteiro positivo.")
        self._id_funcionario = id_funcionario
        self.nome = nome
        self.salario_base = salario_base
    
    @property
    def id_funcionario(self) -> int:
        return self._id_funcionario

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome do funcionário não pode ser vazio.")
        self._nome = novo_nome.strip().title()

    @property
    def salario_base(self) -> float:
        return self._salario_base

    @salario_base.setter
    def salario_base(self, novo_salario: float):
        if not isinstance(novo_salario, (int, float)):
            raise TypeError("O salário base deve ser um valor numérico.")
        if novo_salario < 0:
            raise ValueError("O salário base não pode ser negativo.")
        self._salario_base = float(novo_salario)

    def exibir_dados(self) -> str:
        info_base = (
            f"ID: {self._id_funcionario}\n"
            f"Nome: {self._nome}\n"
            f"Salário Base: R${self._salario_base:.2f}"
        )
        return info_base
    
    @abstractmethod
    def calcular_pagamento(self) -> float:
        pass