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

    # Casos de uso principais (invocados pela View)
    def receber_clientes(self, numero_pessoas: int) -> Result:
        try:
            novo_grupo = self._cliente_controller.criar_grupo(numero_pessoas)
        except ValueError:
            return Result(status="invalid", error="grupo_invalido")

        mesa_livre = self._mesa_controller.encontrar_mesa_livre(novo_grupo.numero_pessoas)
        if mesa_livre:
            garcom = self._funcionario_controller.encontrar_garcom_disponivel()
            if garcom:
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
        mesa = self._mesa_controller.encontrar_mesa_por_numero(numero_mesa)
        if not mesa or mesa.status != StatusMesa.OCUPADA:
            return Result(status="invalid", error="mesa_invalida")

        conta = self._conta_controller.encontrar_conta_por_mesa(numero_mesa)
        if not conta:
            return Result(status="not_found", error="conta_nao_encontrada")

        self._conta_controller.fechar_conta(conta)

        self._mesa_controller.liberar_mesa(numero_mesa)

        return Result(status="ok", data={"conta": conta, "mesa": mesa}, message_key="conta_fechada")

    def demitir_funcionario(self, id_funcionario: int) -> Result:
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

    def confirmar_pedido(self, id_pedido: int) -> Result:
        p = self._pedido_controller.encontrar_pedido_por_id(id_pedido)
        if not p:
            return Result(status="not_found", error="pedido_nao_encontrado")
        if not self._pedido_controller.confirmar_pedido(id_pedido):
            return Result(status="invalid", error="pedido_nao_confirmado")
        self._pedido_controller.iniciar_preparo(id_pedido)
        return Result(status="ok", data={"pedido": p}, message_key="pedido_confirmado")
    
    def pedido_pronto(self, id_pedido: int) -> Result:
        p = self._pedido_controller.encontrar_pedido_por_id(id_pedido)
        if not p:
            return Result(status="not_found", error="pedido_nao_encontrado")
        if not self._pedido_controller.marcar_pronto(id_pedido):
            return Result(status="invalid", error="pedido_nao_pronto")
        return Result(status="ok", data={"pedido": p}, message_key="pedido_pronto")

    def entregar_pedido(self, id_pedido: int) -> Result:
        p = self._pedido_controller.encontrar_pedido_por_id(id_pedido)
        if not p:
            return Result(status="not_found", error="pedido_nao_encontrado")
        if not self._pedido_controller.marcar_entregue(id_pedido):
            return Result(status="invalid", error="pedido_nao_entregue")
        return Result(status="ok", data={"pedido": p}, message_key="pedido_entregue")

    def tentar_alocar_fila(self, greedy: bool = False) -> list[Result]:

        resultados: list[Result] = []
        fila_snapshot = self._fila_controller.listar()  # cópia

        for grupo in fila_snapshot:
            # tenta achar a melhor mesa livre p/ este grupo
            mesa = self._mesa_controller.encontrar_mesa_livre(grupo.numero_pessoas)  # 
            if not mesa:
                if not greedy:
                    break  # FIFO estrito: primeiro que não coube => para tudo
                else:
                    continue  # greedy: tenta próximos

            # designa garçom se houver (não é bloqueante)
            garcom = self._funcionario_controller.encontrar_garcom_disponivel()  # 
            if garcom:
                self._mesa_controller.designar_garcom(mesa, garcom)  # 

            # ocupa mesa; se falhar por corrida, tenta próximo conforme política
            if not self._mesa_controller.ocupar_mesa(mesa.id_mesa, grupo):  # 
                if not greedy:
                    break
                else:
                    continue

            # remove da fila e abre conta (ASS: precisa do arg 'mesa'!)
            self._fila_controller.remover(grupo)
            conta = self._conta_controller.abrir_nova_conta(grupo, mesa)  # 

            resultados.append(Result(
                status="ok",
                data={"grupo": grupo, "mesa": mesa, "garcom": garcom, "conta": conta},
                message_key="grupo_alocado"
            ))

        return resultados