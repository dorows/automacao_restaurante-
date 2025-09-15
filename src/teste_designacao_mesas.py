# Importa as classes que vamos manipular diretamente
from garcom import Garcom
from mesa import Mesa

# --- 1. SETUP INICIAL (O que antes era feito pelo Restaurante) ---

print("--- Criando a equipe e o ambiente ---")
# Criar os garçons
joao = Garcom(1, "João", 1800.0)
pedro = Garcom(2, "Pedro", 1800.0)

# Criar a lista de mesas
todas_as_mesas = []
for i in range(1, 9):
    todas_as_mesas.append(Mesa(id_mesa=i, capacidade=4))

print("Equipe e mesas criadas.")

# --- 2. LÓGICA DE NEGÓCIO (O que antes era feito por um método do Restaurante) ---

print("\n--- Definindo as seções fixas dos garçons ---")
# Definir as seções EXATAMENTE como você descreveu
mesas_do_joao = [m for m in todas_as_mesas if 1 <= m.id_mesa <= 4]
mesas_do_pedro = [m for m in todas_as_mesas if 5 <= m.id_mesa <= 8]

# Ligando João às suas mesas
for mesa in mesas_do_joao:
    sucesso = joao.adicionar_mesa(mesa)
    if sucesso:
        mesa.garcom_responsavel = joao
print(f"Seção do {joao.nome} definida.")

# Ligando Pedro às suas mesas
for mesa in mesas_do_pedro:
    sucesso = pedro.adicionar_mesa(mesa)
    if sucesso:
        mesa.garcom_responsavel = pedro
print(f"Seção do {pedro.nome} definida.")


# --- 3. VERIFICAÇÃO (Exibindo o resultado final) ---

print("\n--- Status Final ---")
print("\nGarçons e suas seções:")
print(joao.exibir_dados())
print(pedro.exibir_dados())

print("\nMesas e seus garçons responsáveis:")
for mesa in todas_as_mesas:
    print(mesa)