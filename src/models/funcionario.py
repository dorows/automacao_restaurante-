from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, id_funcionario:int, nome:str, salario_base:float):
        if isinstance (id_funcionario, int):
            self._id_funcionario = id_funcionario
        if isinstance (nome, str):
            self._nome = nome
        if isinstance (salario_base, float):
            self._salario_base = salario_base
    
    @property
    def id_funcionario(self) -> int:
        return self._id_funcionario

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str):
        self._nome = novo_nome.strip().title()

    @property
    def salario_base(self) -> float:
        return self._salario_base

    @salario_base.setter
    def salario_base(self, novo_salario: float):
        self._salario_base = novo_salario

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