from typing import Dict, List

class ContaView:
    def exibir_extrato(self, conta: Dict[str, object]) -> None:
        print("\n" + "*"*35)
        print(f"EXTRATO CONTA #{conta['id_conta']}".center(35))
        print(f"Mesa: {conta['mesa_id']} | Cliente: {conta['cliente']}".center(35))
        print("*"*35)

        itens = conta.get("itens", [])
        if not itens:
            print("Nenhum item consumido.")
        else:
            for ped in itens:
                print(f" > Pedido ID: {ped['pedido_id']} ({ped['status']})")
                for ln in ped.get("linhas", []):
                    print(f"   - {ln}")

        print("-"*35)
        print(f"TOTAL GERAL: R$ {conta['total']:.2f}".center(35))
        print("*"*35)

    def ok(self, msg: str) -> None: print(f"[OK] {msg}")
    def erro(self, msg: str) -> None: print(f"[ERRO] {msg}")
