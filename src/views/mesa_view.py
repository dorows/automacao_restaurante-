from typing import List, Dict, Optional

class MesaView:
    def exibir_mesas(self, mesas: List[Dict[str, object]]) -> None:
        print("\n--- STATUS ATUAL DAS MESAS ---")
        if not mesas:
            print("Nenhuma mesa cadastrada no sistema.")
            return
        for m in mesas:
            gar = m.get("garcom") or "-"
            print(f"#{m['id']:>2} | cap:{m['cap']:<2} | {m['status']:<8} | garçom: {gar}")
        print("-" * 40)

    def exibir_detalhes_mesa(self, mesa: Dict[str, object]) -> None:
        print(f"\n--- Detalhes da Mesa {mesa['id']} ---")
        gar = mesa.get("garcom") or "-"
        conta = mesa.get("conta_id")
        conta_txt = f"Conta #{conta}" if conta else "Sem conta"
        print(f"cap:{mesa['cap']}  |  {mesa['status']}  |  garçom: {gar}  |  {conta_txt}")
        print("-" * 40)

    def ok(self, msg: str) -> None: print(f"[OK] {msg}")
    def erro(self, msg: str) -> None: print(f"[ERRO] {msg}")
