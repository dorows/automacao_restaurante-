from typing import List, Dict

class PedidoView:
    def exibir_pedido(self, pedido: Dict[str, object]) -> None:
        print("\n" + "-"*45)
        print(f"Pedido #{pedido['id_pedido']} | Mesa {pedido['mesa_id']} | {pedido['status']}")
        if not pedido.get("linhas"):
            print("Sem itens.")
        else:
            for ln in pedido["linhas"]:
                print(f" - {ln}")
        print(f"Subtotal: R$ {pedido['subtotal']:.2f}")
        print("-"*45)

    def exibir_lista_pedidos(self, pedidos: List[Dict[str, object]]) -> None:
        if not pedidos:
            print("\nNenhum pedido cadastrado.")
            return
        for p in pedidos:
            self.exibir_pedido(p)

    def ok(self, msg: str) -> None: print(f"[OK] {msg}")
    def erro(self, msg: str) -> None: print(f"[ERRO] {msg}")
