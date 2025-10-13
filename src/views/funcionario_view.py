from typing import List, Dict

class FuncionarioView:
    def exibir_funcionarios(self, funcionarios: List[Dict[str, object]]) -> None:
        print("\n--- EQUIPE DO RESTAURANTE ---")
        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
            return
        
        for f in funcionarios:
            # Constrói a linha base
            linha = f"#{f['id']:>2} | {f['papel']:<11} | {f['nome']:<20} | salario: {f['salario']:>10}"
            
            # Se for um garçom, adiciona a informação da gorjeta e mesa
            if f.get('gorjetas') is not None:
                linha += f" | gorjetas: R$ {f['gorjetas']:.2f}"
                linha += f" | mesas:{f['mesas']}"
            
            else:
                linha += f" | pedidos:{f['pedidos']}"


            print(linha)
            print("-" * (len(linha) if 'gorjetas' in f and f['gorjetas'] is not None else 45))

    def ok(self, msg: str) -> None: 
        print(f"[OK] {msg}")
        
    def erro(self, msg: str) -> None: 
        print(f"[ERRO] {msg}")