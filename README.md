Este projeto implementa um sistema de automação de restaurante com interface gráfica, seguindo uma arquitetura baseada em MVC com uma camada adicional de aplicação (Application Controller).

## Visão geral de funcionamento

O sistema cobre o ciclo completo de atendimento em um restaurante:

* Cadastro e gerenciamento de:

  * Mesas (capacidade, status, vínculo com grupo e garçom)
  * Funcionários (garçons e cozinheiros)
  * Grupos de clientes (fila de espera e mesas)
  * Cardápio (pratos)
* Controle de pedidos:

  * Criação de pedidos vinculados a uma mesa, garçom e grupo de clientes
  * Adição de itens ao pedido (prato, quantidade, observação)
  * Fluxo de status do pedido (aberto, em preparo, pronto, entregue)
* Controle de contas:

  * Abertura de conta por mesa e grupo de clientes
  * Associação de múltiplos pedidos a uma mesma conta
  * Cálculo do total da conta
  * Fechamento da conta com gorjeta
* Fila de espera:

  * Registro de grupos na fila
  * Alocação de grupos em mesas disponíveis
  * Modo de auto-alocação
* Estatísticas:

  * Prato mais vendido
  * Desempenho de garçons (mesas atendidas, gorjetas)
  * Geração de dados para gráficos (por exemplo, pratos mais pedidos)

A interface gráfica permite:

* Selecionar mesas, visualizar fila, cardápio e conteúdo da conta
* Registrar pedidos e avançar o status dos pedidos
* Finalizar atendimento com uma janela de checkout que exibe:

  * Extrato de itens consumidos
  * Subtotal
  * Gorjeta sugerida (10%)
  * Total final ajustável pela gorjeta inserida

Todos os dados relevantes (mesas, grupos, funcionários, cardápio, contas, pedidos, fila) são persistidos por meio de DAOs, de forma que o estado do restaurante é preservado entre execuções.

## Padrão arquitetural adotado

O projeto segue uma arquitetura baseada em MVC, organizada em quatro camadas conceituais:

### Model

Responsável pelos objetos de domínio e regras locais:

* Mesas, contas, pedidos, itens de pedido, pratos, grupos de clientes, funcionários, fila de espera, enums de status, exceções.
* Implementa invariantes e operações diretamente relacionadas ao domínio (por exemplo, adicionar item a pedido, calcular subtotal, fechar conta).
* Não conhece interface gráfica nem detalhes de persistência (os modelos não importam GUI).

### Persistence / DAO

Camada de acesso a dados, isolada:

* Um DAO para cada agregação relevante (mesas, contas, pedidos, cardápio, funcionários, grupos, fila).
* Cada DAO:

  * Carrega os dados em memória ao inicializar.
  * Mantém um cache de objetos de domínio.
  * Atualiza o armazenamento em disco a cada operação de escrita.
* Controllers usam DAOs para ler e salvar estado, mantendo os modelos puros.

### Controller

Camada de lógica de negócio e coordenação de domínio:

* Controllers tratam casos de uso:

  * MesaController: cadastro e gestão de mesas.
  * FuncionarioController: cadastro e gestão de funcionários.
  * ClienteController: cadastro de grupos de clientes.
  * FilaController: gestão da fila de espera.
  * CardapioController: gestão dos pratos.
  * ContaController: abertura, atualização e fechamento de contas.
  * PedidoController: fluxo completo de pedidos.
  * RestauranteController: orquestra casos de uso de alto nível combinando os demais controllers.
* Controllers:

  * Lidam com validações e regras de negócio.
  * Chamam DAOs para persistir alterações.
  * Retornam dados em formatos simples (dicts/listas) para serem usados pela camada de aplicação e pelas views.
* Controllers não importam nem utilizam FreeSimpleGUI.
* Controllers não interagem diretamente com a interface gráfica.

### View

Camada de apresentação (GUI):

* Implementada com FreeSimpleGUI.
* Responsável apenas por:

  * Definir o layout das janelas.
  * Exibir dados já processados (tipicamente dicts/listas).
  * Capturar eventos e inputs do usuário.
* Exemplos de views:

  * GuiMainView: tela principal, exibe mesas, fila, cardápio e conta da mesa.
  * GuiMesaView: gerenciamento de mesas.
  * GuiEquipeView: gerenciamento de equipe.
  * GuiStatsView: exibição de estatísticas e gráficos.
  * GuiCardapioView: gerenciamento de cardápio.
  * checkout_view: janela de checkout/extrato para fechamento da conta.
* Views não chamam diretamente métodos dos controllers nem manipulam modelos. Todo ganho de dados e ações vem pela camada de aplicação.

Para rodar basta seguir os passos:
```bash
1-
python -m venv .venv

2-
source .venv/Scripts/activate # Windows
source .venv/bin/activate # Linux/Mac

3-
pip install -r requirements.txt

4-
python src/main.py
```
