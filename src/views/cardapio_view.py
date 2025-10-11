from typing import Iterable
from models.cardapio import Cardapio
from models.prato import Prato

class CardapioView:
    def exibir_cardapio(self, cardapio: Cardapio):
        print("\n" + "="*25 + " CARDÁPIO " + "="*25)
        pratos: Iterable[Prato] = cardapio.pratos
        if not pratos:
            print("Nenhum prato cadastrado.")
        else:
            for prato in pratos:
                print(f"{prato.id_prato:>3} | {prato.nome:<30} R$ {prato.preco:>7.2f}")
        print("="*62)

    def exibir_mensagem_sucesso(self, mensagem: str): print(f"[OK] {mensagem}")
    def exibir_mensagem_erro(self, mensagem: str): print(f"[ERRO] {mensagem}")
