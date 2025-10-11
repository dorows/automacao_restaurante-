from typing import List, Optional
from models import (
    Pedido, ItemPedido, Prato, Mesa, Garcom, GrupoCliente, Conta, StatusPedido
)


class PedidoController:
    def __init__(self):
        self._pedidos = []

    def encontrar_pedido_por_id(self, id_pedido: int) -> Optional[Pedido]:
        return next((p for p in self._pedidos if p.id_pedido == id_pedido), None)

    def criar_novo_pedido(self, mesa: Mesa, garcom: Garcom, grupo_cliente: GrupoCliente) -> Pedido:
        novo_pedido = Pedido(mesa=mesa, garcom=garcom, grupo_cliente=grupo_cliente)
        self._pedidos.append(novo_pedido)
        return novo_pedido

    def adicionar_item_a_conta(self, conta: Conta, prato: Prato, quantidade: int) -> bool:
        if not conta.esta_aberta:
            return False
        if quantidade <= 0:
            return False

        pedido_alvo = next((p for p in conta.pedidos if p.status == StatusPedido.ABERTO), None)
        if not pedido_alvo:
            pedido_alvo = self.criar_novo_pedido(
                mesa=conta.mesa,
                garcom=conta.mesa.garcom_responsavel,
                grupo_cliente=conta.grupo_cliente
            )
            conta.adicionar_pedido(pedido_alvo)

        novo_item = ItemPedido(prato=prato, quantidade=quantidade)
        pedido_alvo.adicionar_item(novo_item)
        return True

    def confirmar_pedido(self, id_pedido: int) -> bool:
        p = self.encontrar_pedido_por_id(id_pedido)
        return p.confirmar() if p else False

    def iniciar_preparo(self, id_pedido: int) -> bool:
        p = self.encontrar_pedido_por_id(id_pedido)
        return p.iniciar_preparo() if p else False

    def marcar_pronto(self, id_pedido: int) -> bool:
        p = self.encontrar_pedido_por_id(id_pedido)
        return p.finalizar_preparo() if p else False
