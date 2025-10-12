from __future__ import annotations
from typing import List, Dict, Optional

from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.funcionario_view import FuncionarioView

from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController

from models.status_enums import StatusMesa
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro
from models.conta import Conta

class RestauranteController:
    """Coordena fluxos gerais do restaurante e imprime via views passivas."""
    def __init__(self,
                 console_v: ConsoleView,
                 mesa_v: MesaView,
                 fila_v: FilaView,
                 conta_v: ContaView,
                 cardapio_v: CardapioView,
                 func_v: FuncionarioView,
                 mesa_controller: MesaController,
                 conta_controller: ContaController,
                 fila_controller: FilaController,
                 funcionario_controller: FuncionarioController,
                 cardapio_controller: CardapioController,
                 cliente_controller: ClienteController) -> None:
        self.console = console_v
        self.mesa_v = mesa_v
        self.fila_v = fila_v
        self.conta_v = conta_v
        self.cardapio_v = cardapio_v
        self.func_v = func_v

        self._mesa = mesa_controller
        self._conta = conta_controller
        self._fila = fila_controller
        self._func = funcionario_controller
        self._cardapio = cardapio_controller
        self._cliente = cliente_controller

    # --------------------------- helpers: Model -> primitivos --------------------
    def _mesa_dict(self, m: Mesa) -> Dict[str, object]:
        return {
            "id": m.id_mesa,
            "cap": m.capacidade,
            "status": m.status.name if hasattr(m.status, "name") else str(m.status),
            "garcom": m.garcom_responsavel.nome if getattr(m, "garcom_responsavel", None) else None
        }

    def _fila_list(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for i, g in enumerate(self._fila.listar(), start=1):
            out.append({"pos": i, "nome": f"Grupo {g.id_grupo}", "pessoas": g.numero_pessoas})
        return out

    def _garcons_list(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for f in self._func.listar_funcionarios():
            if isinstance(f, Garcom):
                out.append({"id": f.id_funcionario, "nome": f.nome, "mesas": len(f.mesas_atendidas)})
        return out

    def _cardapio_list(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for p in self._cardapio.cardapio.pratos:
            out.append({"id": p.id_prato, "nome": p.nome, "preco": p.preco})
        return out

    def _conta_dict(self, conta: Conta) -> Dict[str, object]:
        itens = []
        for ped in conta.pedidos:
            linhas = [f"{it.quantidade}x {it.prato.nome} - R$ {(it.quantidade * it.prato.preco):.2f}" for it in ped.itens]
            itens.append({
                "pedido_id": ped.id_pedido,
                "status": ped.status.name if hasattr(ped.status, "name") else str(ped.status),
                "linhas": linhas
            })
        return {
            "id_conta": conta.id_conta,
            "mesa_id": conta.mesa.id_mesa,
            "cliente": f"Grupo {conta.grupo_cliente.id_grupo}",
            "itens": itens,
            "total": conta.calcular_total()
        }

    # ------------------------------ dashboard ------------------------------------
    def print_dashboard(self) -> None:
        dados = {
            "mesas": [self._mesa_dict(m) for m in self._mesa.listar_mesas()],
            "fila": self._fila_list(),
            "garcons": self._garcons_list(),
            "cardapio": self._cardapio_list(),
        }
        self.console.render_dashboard(dados)
        self.mesa_v.exibir_mesas(dados["mesas"])
        self.fila_v.exibir_fila(dados["fila"])

    # ----------------------------- autoalocação ----------------------------------
    def auto_alocar_e_printar(self, greedy: bool = False) -> None:
        msgs: List[str] = []
        snapshot = self._fila.listar()
        for grupo in snapshot:
            mesa = self._mesa.encontrar_mesa_livre(grupo.numero_pessoas)
            if not mesa:
                if not greedy:
                    break
                else:
                    continue

            # tenta designar garçom; se não houver disponível, segue sem
            garcom = self._func.encontrar_garcom_disponivel()
            if garcom:
                ok = self._mesa.designar_garcom(mesa, garcom)
                if not ok:
                    garcom = None  # não deixa estado inconsistente

            if not self._mesa.ocupar_mesa(mesa.id_mesa, grupo):
                if not greedy:
                    break
                else:
                    continue

            self._fila.remover(grupo)
            conta = self._conta.abrir_nova_conta(grupo, mesa)
            msgs.append(f"[ALOCADO] Grupo {grupo.id_grupo} ({grupo.numero_pessoas}) -> Mesa {mesa.id_mesa} "
                        f"(Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}")

            # Mostra extrato inicial
            self.conta_v.exibir_extrato(self._conta_dict(conta))

        if msgs:
            self.console.print_lines(msgs)

    # ----------------------------- casos de uso mesa/conta ------------------------
    def receber_clientes_e_printar(self, qtd: int) -> None:
        if qtd <= 0:
            self.console.print_lines(["[ERRO] Quantidade inválida."])
            return

        grupo = self._cliente.criar_grupo(qtd)
        mesa = self._mesa.encontrar_mesa_livre(qtd)
        if not mesa:
            self._fila.adicionar_grupo(grupo)
            self.console.print_lines([f"[FILA] Grupo {grupo.id_grupo} ({qtd}) adicionado à fila."])
            return

        garcom = self._func.encontrar_garcom_disponivel()
        if garcom and not self._mesa.designar_garcom(mesa, garcom):
            garcom = None  # não travar por falta de vaga

        if not self._mesa.ocupar_mesa(mesa.id_mesa, grupo):
            # corrida: manda pra fila
            self._fila.adicionar_grupo(grupo)
            self.console.print_lines([f"[FILA] Grupo {grupo.id_grupo} ({qtd}) adicionado à fila."])
            return

        conta = self._conta.abrir_nova_conta(grupo, mesa)
        self.console.print_lines([f"[ALOCADO] Grupo {grupo.id_grupo} -> Mesa {mesa.id_mesa} "
                                  f"(Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}"])
        self.conta_v.exibir_extrato(self._conta_dict(conta))

    def finalizar_atendimento_e_printar(self, mesa_id: int) -> None:
        conta = self._conta.encontrar_conta_por_mesa(mesa_id)
        if not conta:
            self.console.print_lines([f"[ERRO] Não há conta aberta na mesa {mesa_id}."])
            return

        total = conta.calcular_total()
        self._conta.fechar_conta(conta)
        liberada = self._mesa.liberar_mesa(mesa_id)

        self.conta_v.exibir_extrato(self._conta_dict(conta))
        if liberada:
            self.console.print_lines([f"[OK] Conta #{conta.id_conta} fechada (R$ {total:.2f}). Mesa {mesa_id} liberada e limpa."])
        else:
            self.console.print_lines([f"[OK] Conta #{conta.id_conta} fechada (R$ {total:.2f}). Mesa {mesa_id} não pôde ser liberada agora."])

    def limpar_mesa_e_printar(self, mesa_id: int) -> None:
        mesa = self._mesa.encontrar_mesa_por_numero(mesa_id)
        if not mesa:
            self.console.print_lines([f"[ERRO] Mesa {mesa_id} não existe."])
            return
        if mesa.status == StatusMesa.SUJA:
            if mesa.limpar():
                self.console.print_lines([f"[OK] Mesa {mesa_id} limpa e liberada."])
            else:
                self.console.print_lines([f"[ERRO] Falha ao limpar a mesa {mesa_id}."])
        else:
            self.console.print_lines([f"[INFO] Mesa {mesa_id} não está suja (status: {mesa.status.value})."])

    # ----------------------------- equipe: listar/contratar/demitir --------------
    def listar_equipe_e_printar(self) -> None:
        lst = []
        for f in self._func.listar_funcionarios():
            papel = "Garçom" if isinstance(f, Garcom) else ("Cozinheiro" if isinstance(f, Cozinheiro) else "Funcionário")
            mesas = len(getattr(f, "mesas_atendidas", [])) if isinstance(f, Garcom) else 0
            lst.append({"id": f.id_funcionario, "nome": f.nome, "papel": papel, "mesas": mesas})
        self.func_v.exibir_funcionarios(lst)

    def contratar_garcom_e_printar(self, nome: str, salario: float) -> None:
        nome = (nome or "").strip()
        if not nome:
            self.console.print_lines(["[ERRO] Nome do garçom não pode ser vazio."])
            return
        if salario <= 0:
            self.console.print_lines(["[ERRO] Salário deve ser positivo."])
            return
        g = self._func.contratar_garcom(nome, salario)
        self.console.print_lines([f"[OK] Garçom {g.nome} (ID {g.id_funcionario}) contratado(a)."])
        self.listar_equipe_e_printar()

    def contratar_cozinheiro_e_printar(self, nome: str, salario: float) -> None:
        nome = (nome or "").strip()
        if not nome:
            self.console.print_lines(["[ERRO] Nome do cozinheiro não pode ser vazio."])
            return
        if salario <= 0:
            self.console.print_lines(["[ERRO] Salário deve ser positivo."])
            return
        c = self._func.contratar_cozinheiro(nome, salario)
        self.console.print_lines([f"[OK] Cozinheiro(a) {c.nome} (ID {c.id_funcionario}) contratado(a)."])
        self.listar_equipe_e_printar()

    def demitir_funcionario_e_printar(self, id_func: int) -> None:
        if id_func <= 0:
            self.console.print_lines(["[ERRO] ID inválido."])
            return
        ok, func, err = self._func.demitir_funcionario(id_func)
        if ok and func:
            self.console.print_lines([f"[OK] Funcionário #{func.id_funcionario} ({func.nome}) demitido(a)."])
            self.listar_equipe_e_printar()
            return

        # mensagens de erro sem brechas
        if err == "func_nao_encontrado":
            self.console.print_lines([f"[ERRO] Funcionário #{id_func} não encontrado."])
        elif err == "cozinheiro_com_pedidos_em_preparo":
            self.console.print_lines(["[ERRO] Não é possível demitir: cozinheiro possui pedidos em preparo."])
        else:
            self.console.print_lines(["[ERRO] Não foi possível demitir o funcionário."])

    def adicionar_mesa_e_printar(self, id_mesa: int, capacidade: int) -> None:
        if id_mesa <= 0:
            self.console.print_lines(["[ERRO] ID da mesa deve ser positivo."])
            return
        if capacidade <= 0:
            self.console.print_lines(["[ERRO] Capacidade deve ser >= 1."])
            return
        if self._mesa.encontrar_mesa_por_numero(id_mesa):
            self.console.print_lines([f"[ERRO] Já existe mesa com ID {id_mesa}."])
            return

        nova = self._mesa.cadastrar_mesa(id_mesa, capacidade)
        if not nova:
            self.console.print_lines(["[ERRO] Não foi possível cadastrar a mesa."])
            return

        self.console.print_lines([f"[OK] Mesa {nova.id_mesa} cadastrada (capacidade {nova.capacidade})."])
        # Mostra a lista atualizada e tenta realocar fila (FIFO estrito)
        self.mesa_v.exibir_mesas([self._mesa_dict(m) for m in self._mesa.listar_mesas()])
        self.auto_alocar_e_printar(greedy=False)