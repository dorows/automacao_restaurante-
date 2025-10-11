from typing import List, Optional

from .mesa_controller import MesaController
from .funcionario_controller import FuncionarioController
from .cardapio_controller import CardapioController
from .pedido_controller import PedidoController
from .conta_controller import ContaController
from .fila_de_espera_controller import FilaController
from .grupo_cliente_controller import ClienteController

from core.result import Result

from models.mesa import Mesa
from models.conta import Conta
from models.cardapio import Cardapio
from models.fila_de_espera import FilaDeEspera
from models.funcionario import Funcionario
from models.status_enums import StatusMesa

class RestauranteController:
    def __init__(self):
        # Sub-sistemas (cada um faz seu setup_inicial internamente, quando aplicável)
        self._mesa_controller = MesaController()
        self._funcionario_controller = FuncionarioController()
        self._cardapio_controller = CardapioController()
        self._pedido_controller = PedidoController()
        self._conta_controller = ContaController()
        self._fila_controller = FilaController()
        self._cliente_controller = ClienteController()

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

    # ---------- Casos de uso principais (invocados pela View) ----------
    def receber_clientes(self, numero_pessoas: int) -> Result:
        """
        Tenta sentar o grupo; se não houver mesa, coloca na fila.
        Sucesso:
          - message_key="grupo_alocado" com data={"grupo","mesa","garcom","conta"}
          - ou message_key="grupo_para_fila" com data={"grupo"}
        Erros:
          - error="grupo_invalido"
        """
        try:
            novo_grupo = self._cliente_controller.criar_grupo(numero_pessoas)
        except ValueError:
            return Result(status="invalid", error="grupo_invalido")

        mesa_livre = self._mesa_controller.encontrar_mesa_livre(novo_grupo.numero_pessoas)
        if mesa_livre:
            garcom = self._funcionario_controller.encontrar_garcom_disponivel()
            if garcom:
                # Se o garçom já estiver no limite, designar_garcom deve ser
                # idempotente/silencioso — a View pode informar depois se quiser.
                self._mesa_controller.designar_garcom(mesa_livre, garcom)

            # Ocupa mesa e abre conta
            self._mesa_controller.ocupar_mesa(mesa_livre.id_mesa, novo_grupo)
            conta = self._conta_controller.abrir_nova_conta(novo_grupo, mesa_livre)

            return Result(
                status="ok",
                data={"grupo": novo_grupo, "mesa": mesa_livre, "garcom": garcom, "conta": conta},
                message_key="grupo_alocado"
            )

        # Sem mesa: vai pra fila
        self._fila_controller.adicionar_grupo(novo_grupo)
        return Result(status="ok", data={"grupo": novo_grupo}, message_key="grupo_para_fila")

    def realizar_pedido(self, numero_mesa: int, id_prato: int, quantidade: int) -> Result:
        """
        Adiciona um item ao pedido aberto da mesa; cria pedido se não existir.
        Sucesso:
          - message_key="item_adicionado" com data={"conta","prato","quantidade"}
        Erros:
          - error="mesa_invalida" | "conta_nao_encontrada" | "prato_nao_encontrado" | "item_nao_adicionado"
        """
        mesa = self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)
        if not mesa or mesa.status != StatusMesa.OCUPADA:
            return Result(status="invalid", error="mesa_invalida")

        conta = self._conta_controller.encontrar_conta_por_mesa(numero_mesa)
        if not conta:
            return Result(status="not_found", error="conta_nao_encontrada")

        prato = self._cardapio_controller.buscar_prato_por_id(id_prato)
        if not prato:
            return Result(status="not_found", error="prato_nao_encontrado")

        ok = self._pedido_controller.adicionar_item_a_conta(conta, prato, quantidade)
        if not ok:
            return Result(status="invalid", error="item_nao_adicionado")

        return Result(status="ok", data={"conta": conta, "prato": prato, "quantidade": quantidade},
                      message_key="item_adicionado")

    def finalizar_atendimento(self, numero_mesa: int) -> Result:
        """
        Fecha a conta da mesa e libera a mesa (de acordo com a política do MesaController).
        Sucesso:
          - message_key="conta_fechada" com data={"conta","mesa"}
        Erros:
          - error="mesa_invalida" | "conta_nao_encontrada"
        """
        mesa = self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)
        if not mesa or mesa.status != StatusMesa.OCUPADA:
            return Result(status="invalid", error="mesa_invalida")

        conta = self._conta_controller.encontrar_conta_por_mesa(numero_mesa)
        if not conta:
            return Result(status="not_found", error="conta_nao_encontrada")

        self._conta_controller.fechar_conta(conta)

        # Observação: seu MesaController.liberar_mesa() atualmente chama limpar() em seguida.
        # Se quiser manter a mesa SUJA até limpar manualmente, separe as operações no MesaController.
        self._mesa_controller.liberar_mesa(numero_mesa)

        return Result(status="ok", data={"conta": conta, "mesa": mesa}, message_key="conta_fechada")

    def demitir_funcionario(self, id_funcionario: int) -> Result:
        """
        Encaminha a demissão para o FuncionarioController (que você já implementou).
        Sucesso:
          - message_key="func_demitido" com data={"id","nome","tipo"}
        Erros:
          - error="func_nao_encontrado" | "cozinheiro_com_pedidos_em_preparo" | outros
        """
        ok, func, err = self._funcionario_controller.demitir_funcionario(id_funcionario)
        if not ok:
            if err == "func_nao_encontrado":
                return Result(status="not_found", error=err)
            if err == "cozinheiro_com_pedidos_em_preparo":
                return Result(status="invalid", error=err)
            return Result(status="error", error=err or "erro_desconhecido")

        # Descobrir "tipo" para a View:
        tipo = func.__class__.__name__  # "Garcom", "Cozinheiro" ou "Funcionario"
        return Result(status="ok",
                      data={"id": func.id_funcionario, "nome": func.nome, "tipo": tipo},
                      message_key="func_demitido")

    # ---------- (Opcional) utilitários que a UI pode querer chamar ----------
    def encontrar_mesa(self, numero_mesa: int) -> Optional[Mesa]:
        return self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)

    def limpar_mesa(self, numero_mesa: int) -> Result:
        """
        Expõe uma limpeza manual da mesa (se sua UI de console tiver esse comando).
        """
        mesa = self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)
        if not mesa:
            return Result(status="not_found", error="mesa_invalida")

        ok = mesa.limpar()
        if not ok:
            return Result(status="invalid", error="mesa_nao_suja")

        return Result(status="ok", data={"mesa": mesa}, message_key="mesa_limpa")

    def cadastrar_mesa(self, id_mesa: int, capacidade: int):
        if capacidade <= 0:
            return Result(status="invalid", error="capacidade_invalida")
        if self._mesa_controller.encontrar_mesa_por_numero(id_mesa):
            return Result(status="conflict", error="mesa_ja_existe")
        mesa = self._mesa_controller.cadastrar_mesa(id_mesa, capacidade)
        return Result(status="ok", data={"mesa": mesa}, message_key="mesa_cadastrada")
