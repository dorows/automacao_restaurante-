from typing import List
from models.funcionario import Funcionario

class FuncionarioView:
    def exibir_funcionarios(self, funcionarios: List[Funcionario]):
        print("\n--- EQUIPE DO RESTAURANTE ---")
        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
            return
            
        for func in funcionarios:
            print(func.exibir_dados())
            print("-" * 25)