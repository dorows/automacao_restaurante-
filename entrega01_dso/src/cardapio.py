from prato import Prato
from typing import Optional

class Cardapio:
    def __init__(self):
        self.__itens: dict[int, Prato] = {}

    def adicionar_prato(self, prato: Prato):
        if prato.id_prato in self.__itens:
            print(f"Aviso: Já existe um prato com o ID {prato.id_prato}. O item não foi adicionado.")
            return
        
        self.__itens[prato.id_prato] = prato
        print(f"Prato '{prato.nome}' adicionado ao cardápio.")

    def buscar_prato(self, id_prato: int) -> Optional[Prato]:
        return self.__itens.get(id_prato)

    def remover_prato(self, id_prato: int):
        if id_prato in self.__itens:
            prato_removido = self.__itens.pop(id_prato)
            print(f"Prato '{prato_removido.nome}' foi removido do cardápio.")
        else:
            print(f"Erro: Prato com ID {id_prato} não encontrado no cardápio.")

    def __str__(self) -> str:
        if not self.__itens:
            return "O cardápio está vazio."
        
        titulo = "--- CARDÁPIO ---\n"
        itens_str = "\n".join(str(prato) for prato in self.__itens.values())
        
        return titulo + itens_str