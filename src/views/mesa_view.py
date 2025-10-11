from typing import List
from models.mesa import Mesa

class MesaView:
    def exibir_mesas(self, mesas: List[Mesa]):
        print("\n--- STATUS ATUAL DAS MESAS ---")
        if not mesas:
            print("Nenhuma mesa cadastrada no sistema.")
            return
        for mesa in mesas:
            print(str(mesa))
        print("-" * 28)

    def exibir_detalhes_mesa(self, mesa: Mesa):
        print(f"\n--- Detalhes da Mesa {mesa.id_mesa} ---")
        print(str(mesa))
        if mesa.conta:
            print(f"Conta associada: ID {mesa.conta.id_conta}")
        print("-" * 28)

    def exibir_mensagem_sucesso(self, mensagem: str): print(f"[OK] {mensagem}")
    def exibir_mensagem_erro(self, mensagem: str): print(f"[ERRO] {mensagem}")
