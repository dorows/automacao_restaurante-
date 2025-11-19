from typing import Optional, List, Dict
from models.prato import Prato
from persistence.cardapio_dao import CardapioDAO

class CardapioController:
    def __init__(self):
        # A lista de pratos não fica mais aqui. O DAO gerencia isso.
        self._cardapio_dao = CardapioDAO()
        # O setup inicial foi movido para o DAO.

    @property
    def pratos(self) -> List[Prato]:
        return list(self._cardapio_dao.get_all())

    def adicionar_novo_prato(self, id_prato: int, nome: str, preco: float, descricao: str) -> Prato:
        if self._cardapio_dao.get(id_prato):
            raise ValueError(f"Já existe um prato cadastrado com o ID {id_prato}.")
        novo_prato = Prato(id_prato, nome, preco, descricao)
        self._cardapio_dao.add(id_prato, novo_prato)
        
        return novo_prato

    def buscar_prato_por_id(self, id_prato: int) -> Optional[Prato]:
        return self._cardapio_dao.get(id_prato)

    def listar_pratos_para_view(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for p in self.pratos:
            out.append({
                "id": p.id_prato,
                "nome": p.nome,
                "preco": p.preco,
            })
        return out