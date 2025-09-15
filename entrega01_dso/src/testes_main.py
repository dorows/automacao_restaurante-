from mesa import Mesa
from grupo_cliente import GrupoCliente
from garcom import Garcom
from cozinheiro import Cozinheiro
from fila_de_espera import FilaDeEspera


if __name__ == "__main__":
    
    print('TESTE DE MESAS')
    mesa_teste = Mesa(10, 4)
    grupo1 = GrupoCliente(441,3)
    grupo_grande = GrupoCliente(442,5)
    
    print(mesa_teste)

    print("\nTentando ocupar a mesa com grupo pequeno...")
    if mesa_teste.ocupar(grupo1):
        print("deu certo como esperado.")
    else:
        print("falhou.")
    print(mesa_teste)

    # Liberando a mesa
    print("\nliberando a mesa")
    mesa_teste.liberar()
    print(mesa_teste)

    # Limpando a mesa
    print("\nlimpando a mesa...")
    mesa_teste.limpar()
    print(mesa_teste)
    
    print("\ntentando ocupar a mesa com grupo grande...")
    if mesa_teste.ocupar(grupo_grande):
        print("Deu certo")
    else:
        print("falhou, como esperado")
    print(mesa_teste) 
    

    print('\nTESTES DOS FUNCIONARIOS\n')

    garcom_ana = Garcom(101, "Ana", 1600.0)
    garcom_ana.adicionar_gorjeta(75.50)
    
    cozinheiro_joao = Cozinheiro(201, "João", 2200.0)
    
    print("Exibindo dados dos funcionários:")
    print(garcom_ana.exibir_dados())
    print(cozinheiro_joao.exibir_dados())

    print("\nCalculando pagamentos:")
    print(f"Pagamento da Ana: R${garcom_ana.calcular_pagamento():.2f}")
    print(f"Pagamento do João: R${cozinheiro_joao.calcular_pagamento():.2f}")

    print('\nTESTES DA FILA DE ESPERA\n')



    fila = FilaDeEspera()
    print(fila)
    print(f"Tamanho inicial da fila: {len(fila)}")

    grupo_A = GrupoCliente(id_grupo=1, numero_pessoas=4)
    grupo_B = GrupoCliente(id_grupo=2, numero_pessoas=6)
    grupo_C = GrupoCliente(id_grupo=3, numero_pessoas=2)

    fila.adicionar_grupo(grupo_A)
    fila.adicionar_grupo(grupo_B)
    fila.adicionar_grupo(grupo_C)

    print("\nEstado atual da fila:")
    print(fila)
    print(f"Tamanho atual da fila: {len(fila)}")
    print("-" * 30)

    print("\n--- TESTE Chamando o primeiro da fila para uma mesa grande (6 lugares) ---")
    mesa_grande_capacidade = 6
    grupo_chamado = fila.chamar_proximo_grupo(mesa_grande_capacidade)
    
    if grupo_chamado:
        print(f"Grupo chamado: {grupo_chamado}")
        print("Resultado esperado: Grupo A (4 pessoas), pois foi o primeiro a chegar e cabe na mesa.")
    else:
        print("Nenhum grupo foi chamado.")
        
    print("\nEstado da fila após a chamada:")
    print(fila)
    print(f"Tamanho da fila: {len(fila)}")
    print("-" * 30)

    print("\n--- TESTE Chamando para uma mesa PEQUENA  ---")
    print("O sistema deve pular o Grupo 2 e chamar o Grupo 3 (2 pessoas).")

    mesa_pequena_capacidade = 2
    grupo_chamado = fila.chamar_proximo_grupo(mesa_pequena_capacidade)

    if grupo_chamado:
        print(f"Grupo chamado: {grupo_chamado}")
        print("Resultado esperado: Grupo 3 (2 pessoas).")
    else:
        print("Nenhum grupo foi chamado.")

    print("\nEstado da fila após a chamada:")
    print(fila)
    print(f"Tamanho da fila: {len(fila)}")
    print("-" * 30)

    print("\n--- TESTE Tentando chamar para uma mesa minúscula ---")
    print("O único grupo na fila é o Grupo 2 (6 pessoas), que não cabe.")

    mesa_minuscula_capacidade = 1
    grupo_chamado = fila.chamar_proximo_grupo(mesa_minuscula_capacidade)

    if grupo_chamado:
        print(f"Grupo chamado: {grupo_chamado}")
    else:
        print("Nenhum grupo foi chamado, como esperado.")

    print("\nEstado da fila após a tentativa de chamada:")
    print(fila) 
    print(f"Tamanho da fila: {len(fila)}")
    print("-" * 30)

    print("\n--- TESTE Esvaziando o último item da fila ---")
    mesa_enorme_capacidade = 10
    grupo_chamado = fila.chamar_proximo_grupo(mesa_enorme_capacidade)
    
    print(f"Grupo chamado: {grupo_chamado}")
    print("\nEstado final da fila:")
    print(fila)
    print(f"Tamanho final da fila: {len(fila)}")
    print("-" * 30)