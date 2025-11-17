from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, id_funcionario: int, nome: str, salario_base: float):
        if not isinstance(id_funcionario, int) or id_funcionario <= 0:
            raise ValueError("O ID do funcionário deve ser um número inteiro positivo.")
        self.__id_funcionario = id_funcionario
        self.__nome = nome
        self.__salario_base = salario_base
    
    @property
    def id_funcionario(self) -> int:
        return self.__id_funcionario

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome do funcionário não pode ser vazio.")
        self.__nome = novo_nome.strip().title()

    @property
    def salario_base(self) -> float:
        return self.__salario_base

    @salario_base.setter
    def salario_base(self, novo_salario: float):
        if not isinstance(novo_salario, (int, float)):
            raise TypeError("O salário base deve ser um valor numérico.")
        if novo_salario < 0:
            raise ValueError("O salário base não pode ser negativo.")
        self.__salario_base = float(novo_salario)

    def exibir_dados(self) -> str:
        info_base = (
            f"ID: {self.__id_funcionario}\n"
            f"Nome: {self.__nome}\n"
            f"Salário Base: R${self.__salario_base:.2f}"
        )
        return info_base
    
    @abstractmethod
    def calcular_pagamento(self) -> float:
        pass