from typing import Optional, List, Dict, Any
from models.prato import Prato
from persistence.cardapio_dao import CardapioDAO 

class CardapioController:
    def __init__(self):
        self._cardapio_dao = CardapioDAO()

    @property
    def pratos(self) -> List[Prato]:
        return self._cardapio_dao.get_all()

    def adicionar_novo_prato(self, id_prato: int, nome: str, preco: float, descricao: str) -> Prato:
        if self._cardapio_dao.get(id_prato):
            raise ValueError(f"Já existe um prato cadastrado com o ID {id_prato}.")
        
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        
        novo_prato = Prato(id_prato, nome, preco, descricao)
        self._cardapio_dao.add(id_prato, novo_prato)
        return novo_prato


    def atualizar_prato(self, id_prato: int, nome: str, preco: float) -> None:
        prato = self.buscar_prato_por_id(id_prato)
        if not prato:
            raise ValueError(f"Prato {id_prato} não encontrado.")
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        prato.nome = nome
        prato.preco = float(preco)        
        self._cardapio_dao.update(id_prato, prato)

    def remover_prato(self, id_prato: int) -> None:
        prato = self.buscar_prato_por_id(id_prato)
        if not prato:
            raise ValueError(f"Prato {id_prato} não encontrado.")
            
        self._cardapio_dao.remove(id_prato)

    def buscar_prato_por_id(self, id_prato: int) -> Optional[Prato]:
        return self._cardapio_dao.get(id_prato)

    def listar_pratos_para_view(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        lista_ordenada = sorted(self.pratos, key=lambda p: p.id_prato)
        
        for p in lista_ordenada:
            out.append({
                "id": p.id_prato,
                "nome": p.nome,
                "preco": p.preco,
            })
        return out
    
    def get_dados_tabela(self) -> List[List[Any]]:
        lista_ordenada = sorted(self.pratos, key=lambda p: p.id_prato)
        return [[p.id_prato, p.nome, f"R$ {p.preco:.2f}"] for p in lista_ordenada]