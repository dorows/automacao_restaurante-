from typing import List
from models.pedido import Pedido
from models.item_pedido import ItemPedido

class PedidoView:
    def exibir_pedido(self, pedido: Pedido):
        print("\n" + "-"*45)
        print(f"Pedido #{pedido.id_pedido} | Mesa {pedido.mesa.id_mesa} | {pedido.status.value}")
        if not pedido.itens:
            print("Sem itens.")
        else:
            for item in pedido.itens:  # type: ItemPedido
                print(f" - {item}")
        print(f"Subtotal: R$ {pedido.calcular_subtotal_pedido():.2f}")
        print("-"*45)

    def exibir_lista_pedidos(self, pedidos: List[Pedido]):
        if not pedidos:
            print("\nNenhum pedido cadastrado.")
            return
        for p in pedidos:
            self.exibir_pedido(p)

    def exibir_mensagem_sucesso(self, mensagem: str): print(f"[OK] {mensagem}")
    def exibir_mensagem_erro(self, mensagem: str): print(f"[ERRO] {mensagem}")
