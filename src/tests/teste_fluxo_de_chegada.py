# tests/test_fluxo_chegada.py

# --- BLOCO DE CÓDIGO PARA CORRIGIR O IMPORT ---
# Adicione estas 4 linhas no TOPO do seu arquivo de teste.
import sys
import os
# A linha abaixo adiciona a pasta 'src' ao caminho de busca do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------------------------

# Agora, o import abaixo vai funcionar, pois o Python sabe onde encontrar a pasta "controllers"
from controllers.restaurante_controller import RestauranteController

def testar_chegada_e_alocacao():
    """
    Um teste simples e focado para validar o workflow de chegada de clientes.
    """
    print("--- INICIANDO TESTE DE FLUXO DE CHEGADA ---")
    
    # 1. Setup: Criamos o controller
    controller = RestauranteController()
    
    print("\n[Cenário 1] Chegada de um grupo de 3 pessoas (deve ocupar a mesa 1 de 4 lugares)")
    
    # 2. Ação: Chamamos o método que queremos testar
    resultado = controller.receber_clientes(numero_pessoas=3)
    print(f"Resultado: {resultado}")
    
    # 3. Verificação: Conferimos o estado do sistema
    # (Acessando diretamente através do controller para verificação)
    mesa1 = controller._mesa_controller.encontrar_mesa_por_numero(1)
    
    print(f"Status da Mesa 1: {mesa1.status.value}")
    if mesa1.conta:
        print(f"Conta criada para a mesa: ID {mesa1.conta.id_conta}")
    else:
        print("ERRO: Nenhuma conta foi criada para a mesa!")
        
    print("\n--- TESTE DE FLUXO DE CHEGADA CONCLUÍDO ---")


# Ponto de entrada para rodar este teste específico
if __name__ == "__main__":
    testar_chegada_e_alocacao()