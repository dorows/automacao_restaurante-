from models.conta import Conta

class ContaView:
    def exibir_extrato(self, conta: Conta):
        print("\n" + "*"*35)
        print(f"EXTRATO CONTA #{conta.id_conta}".center(35))
        print(f"Mesa: {conta.mesa.id_mesa} | Cliente: {conta.grupo_cliente}".center(35))
        print("*"*35)

        if not conta.pedidos:
            print("Nenhum item consumido.")
        else:
            for pedido in conta.pedidos:
                print(f" > Pedido ID: {pedido.id_pedido} ({pedido.status.value})")
                for item in pedido.itens:
                    print(f"   - {str(item)}")

        print("-"*35)
        print(f"TOTAL GERAL: R$ {conta.calcular_total():.2f}".center(35))
        print("*"*35)

    def exibir_mensagem_sucesso(self, mensagem: str): print(f"[OK] {mensagem}")
    def exibir_mensagem_erro(self, mensagem: str): print(f"[ERRO] {mensagem}")
