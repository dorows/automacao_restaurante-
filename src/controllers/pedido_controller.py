# controllers/pedido_controller.py
from typing import List, Optional, Dict
from collections import Counter

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
                 conta_controller: ContaController,
                 cardapio_controller: CardapioController) -> None:
        self._contas = conta_controller
        self._cardapio = cardapio_controller
        self._pedidos: List[Pedido] = []


    def _pedido_dict(self, p: Pedido) -> dict:
        linhas = [f"{it.quantidade}x {it.prato.nome} - R$ {it.calcular_subtotal():.2f}" for it in p.itens]
        return {
            "id_pedido": p.id_pedido,
            "mesa_id": p.mesa.id_mesa,
            "status": p.status.value,            
            "linhas": linhas,
            "subtotal": p.calcular_subtotal_pedido()
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

    def adicionar_item_a_conta(self, conta: Conta, prato: Prato, quantidade: int) -> None:
        pedido_alvo = next((p for p in conta.pedidos if p.status == StatusPedido.ABERTO), None)
        if not pedido_alvo:

            if not conta.mesa.garcom_responsavel:
                raise ValueError(f"A Mesa {conta.mesa.id_mesa} não tem garçom designado.")

            pedido_alvo = self.criar_novo_pedido(
                mesa=conta.mesa,
                garcom=conta.mesa.garcom_responsavel,
                grupo_cliente=conta.grupo_cliente
            )
            conta.adicionar_pedido(pedido_alvo)
        
        novo_item = ItemPedido(prato=prato, quantidade=quantidade)
        pedido_alvo.adicionar_item(novo_item)


    def realizar_pedido(self, mesa_id: int, prato_id: int, quantidade: int) -> Conta:
        conta = self._contas.encontrar_conta_por_mesa(mesa_id)
        if not conta:
            raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

        prato = self._cardapio.buscar_prato_por_id(prato_id)
        if not prato:
            raise ValueError(f"Prato {prato_id} não encontrado no cardápio.")

        self.adicionar_item_a_conta(conta, prato, quantidade)
        
        return conta 

    def confirmar_pedido(self, mesa_id: int) -> Pedido:
        conta = self._contas.encontrar_conta_por_mesa(mesa_id)
        if not conta:
            raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

        ped = self._find_pedido_by_status(conta, StatusPedido.ABERTO)
        if not ped:
            raise ValueError("Nenhum pedido ABERTO para confirmar nesta mesa.")
        ped.confirmar() 
        return ped 
    

    def marcar_pedido_pronto(self, mesa_id: int) -> Pedido:
        conta = self._contas.encontrar_conta_por_mesa(mesa_id)
        if not conta:
            raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

        ped = self._find_pedido_by_status(conta, StatusPedido.EM_PREPARO)
        if not ped:
            raise ValueError("Nenhum pedido EM_PREPARO para marcar como PRONTO.")
        
        ped.finalizar_preparo()
        return ped

    def entregar_pedido(self, mesa_id: int) -> Pedido:
        conta = self._contas.encontrar_conta_por_mesa(mesa_id)
        if not conta:
            raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

        ped = self._find_pedido_by_status(conta, StatusPedido.PRONTO)
        if not ped:
            raise ValueError("Nenhum pedido PRONTO para ENTREGAR.")
        
        ped.entregar_pedido()
        return ped


    def get_estatisticas_pratos(self):
        contagem_pratos = Counter()
        for pedido in self._pedidos:
            for item in pedido.itens:
                contagem_pratos[item.prato] += item.quantidade
        return contagem_pratos
    
    def conta_para_view(self, conta: Conta) -> dict:
        itens = []
        for ped in conta.pedidos:
            linhas = [
                f"{it.quantidade}x {it.prato.nome} - R$ {it.calcular_subtotal():.2f}"
                for it in ped.itens
            ]
            itens.append({
                "pedido_id": ped.id_pedido,
                "status": ped.status.value,
                "linhas": linhas,
            })

        return {
            "id_conta": conta.id_conta,
            "mesa_id": conta.mesa.id_mesa,
            "cliente": f"Grupo {conta.grupo_cliente.id_grupo}",
            "itens": itens,
            "total": conta.calcular_total(),
        }
    
    def pedido_para_view(self, pedido: Pedido) -> dict:
        return self._pedido_dict(pedido)