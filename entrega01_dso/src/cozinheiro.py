from funcionario import Funcionario

class Cozinheiro(Funcionario):
    def __init__(self, id_funcionario: int , nome: str, salario_base: float):
        super().__init__(id_funcionario, nome, salario_base)

    def calcular_pagamento(self):
        return self.salario_base
    
    def exibir_dados(self):
        info_base = super().exibir_dados()
        return f"--- Cozinheiro ---\n{info_base}"
    
    # Futuro... por enquanto cozinheiro nao tem relacao direta com o pedido, porem no futuro ele tera, e isso vai trazer tempos de espera 
    # para cada prato sendo feito
    def atualizar_status_pedido(self):
        pass
    