from typing import List
from models import Mesa, FilaDeEspera, Conta, Cardapio, Funcionario

class ConsoleView:
    def exibir_mensagem(self, mensagem: str):
        print(mensagem)

    def exibir_cardapio(self, cardapio: Cardapio):
        print("\n" + "="*25 + " CARDÁPIO " + "="*25)
        print(cardapio.exibir())
        print("="*62)
        
    def exibir_estado_do_restaurante(self, mesas: List[Mesa], fila: FilaDeEspera):
        print("\n" + "="*62)
        print("PAINEL DE CONTROLE DO RESTAURANTE".center(62))
        print("="*62)

        print("\n--- MESAS ---")
        if not mesas:
            print("Nenhuma mesa cadastrada no sistema.")
        else:
            for mesa in mesas:
                print(str(mesa))

        print("\n" + str(fila))
        print("="*62)

    def exibir_funcionarios(self, funcionarios: List[Funcionario]):
        print("\n--- PAINEL DA EQUIPE ---")
        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
            return
            
        for func in funcionarios:
            print(func.exibir_dados())
            print("-" * 25)

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

    def obter_comando(self) -> tuple[str, list]:
        prompt = (
            "\nDigite um comando:\n"
            "  - chegada [n_pessoas]\n"
            "  - pedir [n_mesa] [id_prato] [qtd]\n"
            "  - confirmar [id_pedido]\n"
            "  - pronto [id_pedido]\n"
            "  - finalizar [n_mesa]\n"
            "  - equipe\n"
            "  - cardapio\n"
            "  - sair\n"
            "> "
        )
        comando_raw = input(prompt)
        partes = comando_raw.strip().lower().split()
        
        if not partes:
            return "invalido", []
        
        acao = partes[0]
        args = partes[1:]
        
        return acao, args