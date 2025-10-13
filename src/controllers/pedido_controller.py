from __future__ import annotations
from typing import List, Optional
from collections import Counter

from views.console_view import ConsoleView
from views.pedido_view import PedidoView
from views.conta_view import ContaView

from controllers.conta_controller import ContaController
from controllers.cardapio_controller import CardapioController

from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.prato import Prato
from models.mesa import Mesa
from models.garcom import Garcom
from models.grupo_cliente import GrupoCliente
from models.conta import Conta
from models.status_enums import StatusPedido

class PedidoController:
    def __init__(self,
                 console_v: ConsoleView,
                 pedido_v: PedidoView,
                 conta_v: ContaView,
                 conta_controller: ContaController,
                 cardapio_controller: CardapioController) -> None:
        self.console = console_v
        self.pedido_v = pedido_v
        self.conta_v = conta_v
        self._contas = conta_controller
        self._cardapio = cardapio_controller
        self._pedidos: List[Pedido] = []

    def _pedido_dict(self, p: Pedido) -> dict:
        linhas = [f"{it.quantidade}x {it.prato.nome} - R$ {it.calcular_subtotal():.2f}" for it in p.itens]
        return {
            "id_pedido": p.id_pedido,
            "mesa_id": p.mesa.id_mesa,
            "status": p.status.name if hasattr(p.status, "name") else str(p.status),
            "linhas": linhas,
            "subtotal": p.calcular_subtotal_pedido()
        }

    def _conta_dict(self, conta: Conta) -> dict:
        itens = []
        for ped in conta.pedidos:
            linhas = [f"{it.quantidade}x {it.prato.nome} - R$ {it.calcular_subtotal():.2f}" for it in ped.itens]
            itens.append({"pedido_id": ped.id_pedido,
                          "status": ped.status.name if hasattr(ped.status, "name") else str(ped.status),
                          "linhas": linhas})
        return {
            "id_conta": conta.id_conta,
            "mesa_id": conta.mesa.id_mesa,
            "cliente": f"Grupo {conta.grupo_cliente.id_grupo}",
            "itens": itens,
            "total": conta.calcular_total()
        }

    def _find_pedido_by_status(self, conta: Conta, status: StatusPedido) -> Optional[Pedido]:
        for p in reversed(conta.pedidos):
            if p.status == status:
                return p
        return None

    def encontrar_pedido_por_id(self, id_pedido: int) -> Optional[Pedido]:
        return next((p for p in self._pedidos if p.id_pedido == id_pedido), None)

    def criar_novo_pedido(self, mesa: Mesa, garcom: Garcom, grupo_cliente: GrupoCliente) -> Pedido:
        novo_pedido = Pedido(mesa=mesa, garcom=garcom, grupo_cliente=grupo_cliente)
        self._pedidos.append(novo_pedido)
        return novo_pedido

    def adicionar_item_a_conta(self, conta: Conta, prato: Prato, quantidade: int):
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


    def realizar_pedido_e_printar(self, mesa_id: int, prato_id: int, quantidade: int) -> None:
        try:
            conta = self._contas.encontrar_conta_por_mesa(mesa_id)
            if not conta:
                raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

            prato = self._cardapio.buscar_prato_por_id(prato_id)
            if not prato:
                raise ValueError(f"Prato {prato_id} não encontrado no cardápio.")

            self.adicionar_item_a_conta(conta, prato, quantidade)

            ped = self._find_pedido_by_status(conta, StatusPedido.ABERTO)
            if ped:
                self.pedido_v.exibir_pedido(self._pedido_dict(ped))
            self.conta_v.exibir_extrato(self._conta_dict(conta))

        except (ValueError, TypeError) as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def confirmar_e_printar(self, mesa_id: int) -> None:
        try:
            conta = self._contas.encontrar_conta_por_mesa(mesa_id)
            if not conta:
                raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

            ped = self._find_pedido_by_status(conta, StatusPedido.ABERTO)
            if not ped:
                self.console.print_lines(["[INFO] Nenhum pedido ABERTO para confirmar."])
                return
            ped.confirmar()
            ped.iniciar_preparo()
            
            self.pedido_v.exibir_pedido(self._pedido_dict(ped))
            self.console.print_lines([f"[OK] Pedido #{ped.id_pedido} confirmado e em preparo (Mesa {mesa_id})."])

        except ValueError as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def pronto_e_printar(self, mesa_id: int) -> None:
        try:
            conta = self._contas.encontrar_conta_por_mesa(mesa_id)
            if not conta:
                raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

            ped = self._find_pedido_by_status(conta, StatusPedido.EM_PREPARO)
            if not ped:
                self.console.print_lines(["[INFO] Nenhum pedido EM_PREPARO para marcar como PRONTO."])
                return
            
            ped.finalizar_preparo()
            self.pedido_v.exibir_pedido(self._pedido_dict(ped))
            self.console.print_lines([f"[OK] Pedido #{ped.id_pedido} marcado como PRONTO (Mesa {mesa_id})."])
        
        except ValueError as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def entregar_e_printar(self, mesa_id: int) -> None:
        try:
            conta = self._contas.encontrar_conta_por_mesa(mesa_id)
            if not conta:
                raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

            ped = self._find_pedido_by_status(conta, StatusPedido.PRONTO)
            if not ped:
                self.console.print_lines(["[INFO] Nenhum pedido PRONTO para ENTREGAR."])
                return
            
            ped.entregar_pedido()
            self.pedido_v.exibir_pedido(self._pedido_dict(ped))
            self.console.print_lines([f"[OK] Pedido #{ped.id_pedido} ENTREGUE (Mesa {mesa_id})."])
            
        except ValueError as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def get_estatisticas_pratos(self):

        contagem_pratos = Counter()
        for pedido in self._pedidos:
            for item in pedido.itens:
                contagem_pratos[item.prato] += item.quantidade
        return contagem_pratos