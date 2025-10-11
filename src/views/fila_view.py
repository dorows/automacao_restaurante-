from models.fila_de_espera import FilaDeEspera
from models.grupo_cliente import GrupoCliente

class FilaView:
    def exibir_fila(self, fila):
        print("\n--- FILA DE ESPERA ---")
        if len(fila) == 0:
            print("A fila de espera está vazia.")
            return
        for pos, grupo in enumerate(fila, start=1):
            print(f"{pos:02d}. Grupo {grupo.id_grupo} - {grupo.numero_pessoas} pessoas")

    def exibir_chamada(self, grupo: GrupoCliente | None):
        if grupo:
            print(f"Chamando {grupo}")
        else:
            print("Nenhum grupo adequado disponível para a capacidade informada.")

    def exibir_mensagem_sucesso(self, mensagem: str): print(f"[OK] {mensagem}")
    def exibir_mensagem_erro(self, mensagem: str): print(f"[ERRO] {mensagem}")
