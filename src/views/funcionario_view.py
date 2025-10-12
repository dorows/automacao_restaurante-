from typing import List, Dict

class FuncionarioView:
    def exibir_funcionarios(self, funcionarios: List[Dict[str, object]]) -> None:
        print("\n--- EQUIPE DO RESTAURANTE ---")
        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
            return
        for f in funcionarios:
            print(f"#{f['id']:>2} | {f['papel']:<11} | {f['nome']:<20} | mesas:{f['mesas']}")
            print("-" * 45)

    def ok(self, msg: str) -> None: print(f"[OK] {msg}")
    def erro(self, msg: str) -> None: print(f"[ERRO] {msg}")
