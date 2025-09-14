from funcionario import Funcionario

class Cozinheiro(Funcionario):
    def __init__(self, id_funcionario, nome, salario_base):
        super().__init__(id_funcionario, nome, salario_base)

    def calcular_pagamento(self):
        return self.salario_base
    
    def exibir_dados(self):
        info_base = super().exibir_dados()
        return f"--- Cozinheiro ---\n{info_base}"
    
    def atualizar_status_pedido(self):
        pass
    