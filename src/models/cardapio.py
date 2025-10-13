from typing import List, Optional
from .prato import Prato  # Usando import relativo

class Cardapio:

    def __init__(self):
        self._pratos: List[Prato] = []

    @property
    def pratos(self) -> List[Prato]:
        return self._pratos.copy()

    def adicionar_prato(self, prato: Prato) -> None:
        if not isinstance(prato, Prato):
            raise TypeError("Apenas objetos da classe Prato podem ser adicionados.")
        
        if any(p.id_prato == prato.id_prato for p in self._pratos):
            raise ValueError(f"Já existe um prato cadastrado com o ID {prato.id_prato}.")
        
        self._pratos.append(prato)

    def buscar_prato_por_id(self, id_prato: int) -> Optional[Prato]:

        for prato in self._pratos:
            if prato.id_prato == id_prato:
                return prato
        return None

    def exibir(self) -> str:
        if not self._pratos:
            return "O cardápio está vazio."

        titulo = "--- CARDÁPIO ---\n"
        lista_de_pratos = "\n".join(str(prato) for prato in self._pratos)    
        return titulo + lista_de_pratos