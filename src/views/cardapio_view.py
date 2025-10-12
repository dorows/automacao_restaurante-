from typing import List, Dict

class CardapioView:
    def exibir_cardapio(self, pratos: List[Dict[str, object]]) -> None:
        """
        pratos: [{ "id":int, "nome":str, "preco":float }]
        """
        print("\n" + "="*25 + " CARDÁPIO " + "="*25)
        if not pratos:
            print("Nenhum prato cadastrado.")
        else:
            for p in pratos:
                print(f"{p['id']:>3} | {p['nome']:<30} R$ {p['preco']:>7.2f}")
        print("="*62)

    def ok(self, msg: str) -> None: print(f"[OK] {msg}")
    def erro(self, msg: str) -> None: print(f"[ERRO] {msg}")
