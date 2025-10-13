from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .prato import Prato

class ItemPedido:    
    def __init__(self, prato: Prato, quantidade: int, observacao: str = ""):
        from .prato import Prato

        if not isinstance(prato, Prato):
            raise TypeError("O item do pedido deve estar associado a um objeto Prato válido.")
        
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("A quantidade de um item deve ser um número inteiro positivo.")

        if not isinstance(observacao, str):
            raise TypeError("A observação deve ser um texto (string).")
            
        self._prato: Prato = prato
        self._quantidade: int = quantidade
        self._observacao: str = observacao.strip() 

    @property
    def prato(self) -> Prato:
        return self._prato

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @property
    def observacao(self) -> str:
        return self._observacao

    def calcular_subtotal(self) -> float:
        return self.prato.preco * self.quantidade

    def __str__(self) -> str:
        obs = f" (Obs: {self.observacao})" if self.observacao else ""
        return (f"{self.quantidade}x {self.prato.nome} - "
                f"R$ {self.calcular_subtotal():.2f}{obs}")