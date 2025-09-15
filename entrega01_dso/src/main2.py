# Importa todas as classes necessárias do projeto
from cardapio import Cardapio
from prato import Prato
from mesa import Mesa
from fila_de_espera import FilaDeEspera
from grupo_cliente import GrupoCliente
from pedido import Pedido
from item_pedido import ItemPedido
from status_enums import StatusMesa

def configurar_restaurante():
    """Cria e configura os objetos iniciais do restaurante."""
    print("--- Configurando o Restaurante ---")
    
    # Criar cardápio e pratos
    cardapio = Cardapio()
    cardapio.adicionar_prato(Prato(1, "Pizza Margherita", 55.00, "Queijo, tomate e manjericão"))
    cardapio.adicionar_prato(Prato(2, "Spaghetti Carbonara", 48.00, "Massa com ovos, queijo, bacon e pimenta"))
    cardapio.adicionar_prato(Prato(3, "Refrigerante", 7.00, "Lata 350ml"))
    cardapio.adicionar_prato(Prato(4, "Pudim", 15.00, "Pudim de leite condensado"))
    print(cardapio)
    
    # Criar mesas
    mesas = [
        Mesa(id_mesa=1, capacidade=2),
        Mesa(id_mesa=2, capacidade=2),
        Mesa(id_mesa=3, capacidade=4),
        Mesa(id_mesa=4, capacidade=6)
    ]
    print("\n--- Mesas Disponíveis ---")
    for mesa in mesas:
        print(mesa)

    # Criar fila de espera
    fila = FilaDeEspera()
    
    return cardapio, mesas, fila

def simular_chegada_clientes(fila: FilaDeEspera):
    """Cria grupos de clientes e os adiciona à fila."""
    print("\n--- Clientes Chegando ---")
    grupos = [
        GrupoCliente(id_grupo=1, numero_pessoas=2), # Cabe na mesa 1 ou 2
        GrupoCliente(id_grupo=2, numero_pessoas=5), # Cabe na mesa 4
        GrupoCliente(id_grupo=3, numero_pessoas=4), # Cabe na mesa 3
        GrupoCliente(id_grupo=4, numero_pessoas=2)  # Ficará na fila
    ]
    for grupo in grupos:
        fila.adicionar_grupo(grupo)
    
    print(f"\n{fila}")

def alocar_clientes(fila: FilaDeEspera, mesas: list[Mesa]):
    """Tenta alocar clientes da fila para mesas livres."""
    print("\n--- Alocando Clientes nas Mesas ---")
    for mesa in mesas:
        if mesa.status == StatusMesa.LIVRE:
            # Procura o primeiro grupo na fila que cabe na mesa
            grupo_para_sentar = fila.chamar_proximo_grupo(mesa.capacidade)
            if grupo_para_sentar:
                mesa.ocupar(grupo_para_sentar)
            else:
                print(f"Nenhum grupo na fila cabe na Mesa {mesa.id_mesa} (capacidade {mesa.capacidade}).")
    
    print("\n--- Status Atual das Mesas e Fila ---")
    for mesa in mesas:
        print(mesa)
    print(f"\n{fila}")

def simular_pedidos(mesa_ocupada: Mesa, cardapio: Cardapio):
    """Simula um grupo fazendo múltiplos pedidos."""
    if not mesa_ocupada.conta:
        print("ERRO: A mesa selecionada não tem uma conta aberta.")
        return

    print(f"\n--- Simulando Pedidos para a Mesa {mesa_ocupada.id_mesa} ---")
    
    # Pedido 1: Pratos principais e bebidas
    pedido1 = Pedido()
    prato_pizza = cardapio.buscar_prato(1)
    prato_refri = cardapio.buscar_prato(3)

    if prato_pizza and prato_refri:
        pedido1.adicionar_item(ItemPedido(prato_pizza, 1))
        pedido1.adicionar_item(ItemPedido(prato_refri, 2))
        mesa_ocupada.conta.adicionar_pedido(pedido1)

    # Pedido 2: Sobremesa
    pedido2 = Pedido()
    prato_pudim = cardapio.buscar_prato(4)
    if prato_pudim:
        pedido2.adicionar_item(ItemPedido(prato_pudim, 2))
        mesa_ocupada.conta.adicionar_pedido(pedido2)


def simular_saida_cliente(mesa_a_liberar: Mesa):
    """Simula o pagamento e a saída de um grupo."""
    if not mesa_a_liberar.conta:
        print("ERRO: A mesa selecionada não está ocupada.")
        return
        
    print(f"\n--- Fechando a Conta da Mesa {mesa_a_liberar.id_mesa} ---")
    
    # Fechar a conta e obter o extrato
    extrato = mesa_a_liberar.conta.fechar_conta()
    print(extrato)
    
    # Liberar e limpar a mesa
    mesa_a_liberar.liberar()
    print(f"Status da mesa após liberar: {mesa_a_liberar.status.value}")
    mesa_a_liberar.limpar()
    print(f"Status da mesa após limpar: {mesa_a_liberar.status.value}")


if __name__ == "__main__":
    # 1. Iniciar o ambiente
    cardapio_restaurante, mesas_restaurante, fila_de_espera = configurar_restaurante()
    
    # 2. Simular a chegada dos clientes
    simular_chegada_clientes(fila_de_espera)
    
    # 3. Alocar clientes nas mesas
    alocar_clientes(fila_de_espera, mesas_restaurante)
    
    # 4. Simular um grupo específico (da mesa 3) fazendo pedidos
    # (Vamos assumir que o grupo 3 sentou na mesa 3)
    mesa_para_pedido = mesas_restaurante[2] 
    simular_pedidos(mesa_para_pedido, cardapio_restaurante)
    
    # 5. Simular a saída e pagamento desse mesmo grupo
    simular_saida_cliente(mesa_para_pedido)
    
    # 6. Tentar alocar o grupo que sobrou na fila
    print("\n--- Nova Rodada de Alocação ---")
    alocar_clientes(fila_de_espera, mesas_restaurante)