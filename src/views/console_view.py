from typing import List
from models.mesa import Mesa
from models.fila_de_espera import FilaDeEspera
from models.conta import Conta
from models.cardapio import Cardapio
from models.funcionario import Funcionario

class ConsoleView:

    def exibir_mensagem(self, mensagem: str):
        print(mensagem)

    def exibir_cardapio(self, cardapio: Cardapio):
        print("\n--- CARDÁPIO ---")
        print(cardapio.exibir())
        print("----------------")
        
    def exibir_estado_do_restaurante(self, mesas: List[Mesa], fila: FilaDeEspera):
        print("\n" + "="*50)
        print("ESTADO ATUAL DO RESTAURANTE")
        print("="*50)

        print("\n--- MESAS ---")
        if not mesas:
            print("Nenhuma mesa cadastrada.")
        else:
            for mesa in mesas:
                print(str(mesa)) 

        print("\n--- FILA DE ESPERA ---")
        print(str(fila)) 
        print("="*50)

    def exibir_funcionarios(self, funcionarios: List[Funcionario]):
        print("\n--- EQUIPE DO RESTAURANTE ---")
        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
            return
            
        for func in funcionarios:
            print(func.exibir_dados())
            print("-" * 25)

    def exibir_extrato(self, conta: Conta):

        print("\n" + "*"*30)
        print(f"EXTRATO CONTA #{conta.id_conta}")
        print(f"Mesa: {conta.mesa.id_mesa} | Cliente: Grupo {conta.grupo_cliente.id_grupo}")
        print("*"*30)
        
        if not conta.pedidos:
            print("Nenhum item consumido.")
        else:
            for pedido in conta.pedidos:
                print(f" > Pedido ID: {pedido.id_pedido} ({pedido.status.value})")
                for item in pedido.itens:
                    print(f"   - {str(item)}")
        
        print("-"*30)
        print(f"TOTAL GERAL: R$ {conta.calcular_total():.2f}")
        print("*"*30)

    def obter_comando(self) -> tuple[str, list]:

        prompt = (
            "\nDigite um comando:\n"
            "  - chegada [n_pessoas]\n"
            "  - pedir [n_mesa] [id_prato] [qtd]\n"
            "  - confirmar [id_pedido]\n"
            "  - finalizar [n_mesa]\n"
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