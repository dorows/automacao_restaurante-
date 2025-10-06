from typing import List, Optional
from .mesa_controller import MesaController
from .funcionario_controller import FuncionarioController
from .cardapio_controller import CardapioController
from .pedido_controller import PedidoController
from .conta_controller import ContaController
from .fila_de_espera_controller import FilaController
from .grupo_cliente_controller import ClienteController

from models import Mesa, Conta, Cardapio, FilaDeEspera, StatusMesa, Funcionario

class RestauranteController:

    def __init__(self):
        print("Iniciando o sistema do restaurante...")
        self._mesa_controller = MesaController()
        self._funcionario_controller = FuncionarioController()
        self._cardapio_controller = CardapioController()
        self._pedido_controller = PedidoController()
        self._conta_controller = ContaController()
        self._fila_controller = FilaController()
        self._cliente_controller = ClienteController()
        print("Sistema pronto.")

    @property
    def mesas(self) -> List[Mesa]:
        return self._mesa_controller.listar_mesas()

    @property
    def fila_de_espera(self) -> FilaDeEspera:
        return self._fila_controller.get_fila()

    @property
    def cardapio(self) -> Cardapio:
        return self._cardapio_controller.cardapio
        
    @property
    def funcionarios(self) -> List[Funcionario]:
        return self._funcionario_controller.listar_funcionarios()

    def receber_clientes(self, numero_pessoas: int) -> str:
        novo_grupo = self._cliente_controller.criar_grupo(numero_pessoas)
        mesa_livre = self._mesa_controller.encontrar_mesa_livre(novo_grupo.numero_pessoas)

        if mesa_livre:
            garcom = self._funcionario_controller.encontrar_garcom_disponivel()
            self._mesa_controller.designar_garcom(mesa_livre, garcom)
            self._mesa_controller.ocupar_mesa(mesa_livre.id_mesa, novo_grupo)
            self._conta_controller.abrir_nova_conta(novo_grupo, mesa_livre)
            return f"Bem-vindo! {novo_grupo} alocado na Mesa {mesa_livre.id_mesa}."
        else:
            self._fila_controller.adicionar_grupo(novo_grupo)
            return f"{novo_grupo} adicionado à fila de espera."

    def realizar_pedido(self, numero_mesa: int, id_prato: int, quantidade: int) -> str:
        mesa = self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)
        if not mesa or mesa.status != StatusMesa.OCUPADA:
             return f"Erro: Mesa {numero_mesa} não está ocupada ou não foi encontrada."
        
        conta = self._conta_controller.encontrar_conta_por_mesa(numero_mesa)
        if not conta:
             return f"Erro: Nenhuma conta ativa encontrada para a mesa {numero_mesa}."
        
        prato = self._cardapio_controller.buscar_prato_por_id(id_prato)
        if not prato:
             return f"Erro: Prato com ID {id_prato} não encontrado."
            
        sucesso = self._pedido_controller.adicionar_item_a_conta(conta, prato, quantidade)
        
        if sucesso:
            return f"Item '{prato.nome}' adicionado ao pedido da Mesa {numero_mesa}."
        else:
            return f"Falha ao adicionar item ao pedido da Mesa {numero_mesa}."
    def confirmar_e_enviar_pedido_para_cozinha(self, id_pedido: int) -> str:
        pedido = self._pedido_controller.encontrar_pedido_por_id(id_pedido)
        if not pedido:
            return f"Erro: Pedido com ID {id_pedido} não encontrado."

        if not pedido.confirmar():
            return f"Erro: Pedido {id_pedido} não pôde ser confirmado (status atual: {pedido.status.value})."

        cozinheiro = self._funcionario_controller.encontrar_cozinheiro_disponivel()
        if not cozinheiro:
            return "ALERTA: Pedido confirmado, mas nenhum cozinheiro está disponível no momento!"
        
        cozinheiro.iniciar_preparo_pedido(pedido)
        
        return f"Pedido {id_pedido} enviado para preparo com o Cozinheiro {cozinheiro.nome}."

    def finalizar_atendimento(self, numero_mesa: int) -> Optional[Conta]:
        mesa = self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)
        if not mesa or mesa.status != StatusMesa.OCUPADA:
            print(f"Aviso: Mesa {numero_mesa} não pode ser finalizada.")
            return None

        conta = self._conta_controller.encontrar_conta_por_mesa(numero_mesa)
        
        self._conta_controller.fechar_conta(conta)
        self._mesa_controller.liberar_mesa(numero_mesa)
        
        self._processar_fila()
        
        return conta

    def _processar_fila(self):
        print("\n[Controller] Verificando fila de espera para mesas livres...")
        if self._fila_controller.esta_vazia():
            return

        for mesa_livre in self.mesas:
            if mesa_livre.status == StatusMesa.LIVRE:
                grupo_da_fila = self._fila_controller.chamar_proximo_grupo(mesa_livre.capacidade)
                if grupo_da_fila:
                    print(f"[Controller] Encontrou {grupo_da_fila} na fila para a Mesa {mesa_livre.numero}.")
                    self.receber_clientes(grupo_da_fila.numero_pessoas)
                    continue