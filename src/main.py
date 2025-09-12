from mesa import Mesa
from grupo_cliente import GrupoCliente

if __name__ == "__main__":
    
    # Criando os objetos
    mesa_teste = Mesa(10, 4)
    grupo1 = GrupoCliente(3)
    grupo_grande = GrupoCliente(5)
    
    print(mesa_teste)

    #  Tentando ocupar com um grupo que cabe 
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
    
    # 5. Tentando ocupar com um grupo que NÃO cabe (deve falhar)
    print("\ntentando ocupar a mesa com grupo grande...")
    if mesa_teste.ocupar(grupo_grande):
        print("Deu certo")
    else:
        print("falhou, como esperado")
    print(mesa_teste) 
