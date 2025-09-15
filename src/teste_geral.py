# Este script deve estar DENTRO da pasta 'src' para funcionar corretamente.

# Importa todas as classes necessárias dos arquivos vizinhos
from status_enums import StatusMesa, StatusGrupoCliente
from funcionario import Funcionario
from garcom import Garcom
from cozinheiro import Cozinheiro
from prato import Prato
from cardapio import Cardapio
from item_pedido import ItemPedido
from pedido import Pedido
from grupo_cliente import GrupoCliente
from conta import Conta
from fila_de_espera import FilaDeEspera
from mesa import Mesa

def run_simulation():
    """
    Executa uma simulação completa do restaurante, testando todas as funcionalidades.
    """
    
    # --- FASE 1: CONFIGURAÇÃO INICIAL DO RESTAURANTE ---
    print(" BEM-VINDO À SIMULAÇÃO GERAL DO RESTAURANTE ".center(80, "="))
    
    # 1.1: Criar Cardápio
    cardapio = Cardapio()
    cardapio.adicionar_prato(Prato(1, "Pizza Margherita", 55.00, "Queijo, tomate e manjericão"))
    cardapio.adicionar_prato(Prato(2, "Spaghetti Carbonara", 48.00, "Massa com ovos, queijo, bacon e pimenta"))
    cardapio.adicionar_prato(Prato(3, "Refrigerante", 7.00, "Lata 350ml"))
    cardapio.adicionar_prato(Prato(4, "Pudim", 15.00, "Pudim de leite condensado"))
    print(cardapio)

    # 1.2: Criar Equipe
    joao = Garcom(101, "João", 1800.0)
    pedro = Garcom(102, "Pedro", 1800.0)
    
    # 1.3: Criar Mesas
    mesas = [Mesa(id_mesa=i, capacidade=4) for i in range(1, 9)]

    # 1.4: Criar Fila de Espera
    fila = FilaDeEspera()

    # --- FASE 2: DEFINIÇÃO DAS SEÇÕES FIXAS DOS GARÇONS ---
    print("\n" + " DEFININDO SEÇÕES DOS GARÇONS ".center(80, "-"))
    mesas_joao = [m for m in mesas if 1 <= m.id_mesa <= 4]
    mesas_pedro = [m for m in mesas if 5 <= m.id_mesa <= 8]
    
    for mesa in mesas_joao:
        joao.adicionar_mesa(mesa)
        mesa.garcom_responsavel = joao
    print(f"Seção do garçom {joao.nome} definida para as mesas 1 a 4.")
    
    for mesa in mesas_pedro:
        pedro.adicionar_mesa(mesa)
        mesa.garcom_responsavel = pedro
    print(f"Seção do garçom {pedro.nome} definida para as mesas 5 a 8.")
    
    # --- FASE 3: CHEGADA DOS CLIENTES E ALOCAÇÃO ---
    print("\n" + " CHEGADA DE CLIENTES ".center(80, "-"))
    fila.adicionar_grupo(GrupoCliente(1, 4))
    fila.adicionar_grupo(GrupoCliente(2, 2))
    fila.adicionar_grupo(GrupoCliente(3, 3))
    print(fila)

    print("\n" + " ALOCANDO GRUPOS NAS MESAS ".center(80, "-"))
    for mesa in mesas:
        if mesa.status == StatusMesa.LIVRE:
            grupo_a_sentar = fila.chamar_proximo_grupo(mesa.capacidade)
            if grupo_a_sentar:
                mesa.ocupar(grupo_a_sentar)
            else:
                print("Não há mais grupos na fila que possam ser alocados.")
                break 
    
    print("\n--- Status atual das Mesas e Fila ---")
    for mesa in mesas: print(mesa)
    print(fila)

    # --- FASE 4: SIMULAÇÃO DE PEDIDOS (NA MESA 1) ---
    print("\n" + " SIMULANDO PEDIDOS NA MESA 01 ".center(80, "-"))
    mesa_alvo = mesas[0] # Pega a Mesa 1
    
    if mesa_alvo.conta:
        # Primeiro pedido (pratos principais e bebidas)
        pedido_1 = Pedido()
        pedido_1.adicionar_item(ItemPedido(cardapio.buscar_prato(1), 2)) # 2 Pizzas
        pedido_1.adicionar_item(ItemPedido(cardapio.buscar_prato(3), 4)) # 4 Refris
        mesa_alvo.conta.adicionar_pedido(pedido_1)
        
        # Segundo pedido (sobremesa)
        pedido_2 = Pedido()
        pedido_2.adicionar_item(ItemPedido(cardapio.buscar_prato(4), 4)) # 4 Pudins
        mesa_alvo.conta.adicionar_pedido(pedido_2)
    else:
        print(f"ERRO: Mesa {mesa_alvo.id_mesa} não está ocupada para receber pedidos.")

    # --- FASE 5: SAÍDA DO GRUPO E LIMPEZA DA MESA ---
    print("\n" + " SIMULANDO SAÍDA DO GRUPO DA MESA 01 ".center(80, "-"))
    if mesa_alvo.status == StatusMesa.OCUPADA:
        mesa_alvo.liberar()  # Este método agora imprime o extrato e fecha a conta
        mesa_alvo.limpar()
    
    print("\n--- Status das Mesas após saída ---")
    for mesa in mesas: print(mesa)

    # --- FASE 6: NOVA CHEGADA E REALOCAÇÃO ---
    print("\n" + " NOVA CHEGADA E REALOCAÇÃO ".center(80, "-"))
    fila.adicionar_grupo(GrupoCliente(4, 3))
    print(fila)

    # Tenta alocar o novo grupo na mesa que vagou (Mesa 1)
    if mesa_alvo.status == StatusMesa.LIVRE:
        grupo_novo = fila.chamar_proximo_grupo(mesa_alvo.capacidade)
        if grupo_novo:
            mesa_alvo.ocupar(grupo_novo)
    
    # --- FASE 7: RELATÓRIO FINAL ---
    print("\n" + " ESTADO FINAL DO RESTAURANTE ".center(80, "="))
    print("\n--- Status final das Mesas ---")
    for mesa in mesas: print(mesa)
    print(fila)
    print("\n--- Status final da Equipe ---")
    print(joao.exibir_dados())
    print(pedro.exibir_dados())

if __name__ == "__main__":
    run_simulation()