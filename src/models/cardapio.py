from typing import List, Optional
from models.prato import Prato

class Cardapio:

    def __init__(self):

        self._pratos: List[Prato] = []

    @property
    def pratos(self) -> List[Prato]:

        return self._pratos.copy()

    def adicionar_prato(self, prato: Prato):

        if not isinstance(prato, Prato):
            raise TypeError("Apenas objetos da classe Prato podem ser adicionados ao cardápio.")

        for p in self._pratos:
            if p.id_prato == prato.id_prato:
                print(f"Aviso: Prato com ID {prato.id_prato} ('{p.nome}') já existe e não foi adicionado.")
                return
        
        self._pratos.append(prato)
        print(f"Prato '{prato.nome}' adicionado ao cardápio.")

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