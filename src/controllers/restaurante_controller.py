from __future__ import annotations
from typing import List, Dict, Optional

from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.funcionario_view import FuncionarioView
from views.pedido_view import PedidoView

from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController
from controllers.pedido_controller import PedidoController

from models.status_enums import StatusMesa
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro
from models.conta import Conta

class RestauranteController:
    def __init__(self,
                 console_v: ConsoleView,
                 mesa_v: MesaView,
                 fila_v: FilaView,
                 conta_v: ContaView,
                 cardapio_v: CardapioView,
                 func_v: FuncionarioView,
                 pedido_v: PedidoView,
                 mesa_controller: MesaController,
                 conta_controller: ContaController,
                 fila_controller: FilaController,
                 funcionario_controller: FuncionarioController,
                 cardapio_controller: CardapioController,
                 cliente_controller: ClienteController,
                 pedido_controller: PedidoController) -> None:
        
        self.console = console_v
        self.mesa_v = mesa_v
        self.fila_v = fila_v
        self.conta_v = conta_v
        self.cardapio_v = cardapio_v
        self.func_v = func_v
        self.pedido_v = pedido_v

        self._pedido_controller = pedido_controller
        self._mesa = mesa_controller
        self._conta = conta_controller
        self._fila = fila_controller
        self._func = funcionario_controller
        self._cardapio = cardapio_controller
        self._cliente = cliente_controller

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
    def get_cardapio_data(self) -> List[Dict[str, object]]:
        return self._cardapio_list()
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
        try:
            msgs: List[str] = []
            snapshot = self._fila.listar() 
            
            for grupo in snapshot:
                mesa = self._mesa.encontrar_mesa_livre(grupo.numero_pessoas)
                if not mesa:
                    if not greedy:
                        break
                    else:
                        continue

                garcom = self._func.encontrar_garcom_disponivel()
                sucesso_designacao, msg_designacao = self._mesa.designar_garcom(mesa, garcom)
                if not sucesso_designacao:
                    garcom = None
                    self.console.print_lines([f"[AVISO] {msg_designacao}"])

                sucesso_ocupar, msg_ocupar = self._mesa.ocupar_mesa(mesa.id_mesa, grupo)
                if not sucesso_ocupar:
                    if not greedy:
                        break
                    else:
                        continue
                conta, msg_conta = self._conta.abrir_nova_conta(grupo, mesa)
                if not conta:
                    self.console.print_lines([f"[AVISO] Falha ao auto-alocar: {msg_conta}"])
                    continue
                self._fila.remover(grupo)
                
                msgs.append(f"[ALOCADO] Grupo {grupo.id_grupo} ({grupo.numero_pessoas}) -> Mesa {mesa.id_mesa} "
                            f"(Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}")

                self.conta_v.exibir_extrato(self._conta_dict(conta))

            if msgs:
                self.console.print_lines(msgs)
        except Exception as e:
            self.console.print_lines([f"[ERRO] Falha durante a auto-alocação: {e}"])

    # ----------------------------- casos de uso mesa/conta ------------------------
    def receber_clientes_e_printar(self, qtd: int) -> None:
        try:
            grupo, msg_grupo = self._cliente.criar_grupo(qtd)
            if not grupo:
                raise ValueError(msg_grupo)

            mesa = self._mesa.encontrar_mesa_livre(grupo.numero_pessoas)
            if not mesa:
                sucesso_fila, msg_fila = self._fila.adicionar_grupo(grupo)
                if not sucesso_fila: 
                    raise ValueError(msg_fila)
                self.console.print_lines([f"[FILA] {grupo} adicionado à fila."])
                return

            garcom = self._func.encontrar_garcom_disponivel()
            sucesso_designacao, msg_designacao = self._mesa.designar_garcom(mesa, garcom)
            if not sucesso_designacao: 
                self.console.print_lines([f"[AVISO] {msg_designacao}"])

            sucesso_ocupar, msg_ocupar = self._mesa.ocupar_mesa(mesa.id_mesa, grupo)
            if not sucesso_ocupar: 
                raise RuntimeError(msg_ocupar)
            conta, msg_conta = self._conta.abrir_nova_conta(grupo, mesa)
            if not conta:
                raise RuntimeError(f"Falha crítica ao abrir conta: {msg_conta}")

            self.console.print_lines([f"[ALOCADO] {grupo} -> Mesa {mesa.id_mesa} (Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}"])
            self.conta_v.exibir_extrato(self._conta_dict(conta))

        except (ValueError, TypeError, RuntimeError) as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def finalizar_atendimento_e_printar(self, mesa_id: int, gorjeta: float = 0.0) -> None:

        try:
            conta = self._conta.encontrar_conta_por_mesa(mesa_id)
            if not conta:
                raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

            garcom_responsavel = conta.mesa.garcom_responsavel
            if garcom_responsavel and gorjeta > 0:
                try:
                    garcom_responsavel.adicionar_gorjeta(gorjeta)
                    self.console.print_lines([f"[INFO] Gorjeta de R$ {gorjeta:.2f} registrada para o Garçom {garcom_responsavel.nome}."])
                except (ValueError, TypeError) as e:
                    self.console.print_lines([f"[AVISO] Não foi possível registrar a gorjeta: {e}"])
            total = conta.calcular_total()
            extrato_data = self._conta_dict(conta)

            sucesso_conta, msg_conta = self._conta.fechar_conta(conta)
            if not sucesso_conta:
                raise RuntimeError(f"Falha ao fechar conta: {msg_conta}")

            sucesso_mesa, msg_mesa = self._mesa.liberar_mesa(mesa_id)
            if not sucesso_mesa:
                self.conta_v.exibir_extrato(extrato_data)
                raise RuntimeError(f"Falha ao libertar mesa: {msg_mesa}")

            self.conta_v.exibir_extrato(extrato_data)
            self.console.print_lines([f"[OK] Conta #{conta.id_conta} fechada (R$ {total:.2f}). {msg_mesa}"])

        except (ValueError, TypeError, RuntimeError) as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def limpar_mesa_e_printar(self, mesa_id: int) -> None:
            try:
                mesa = self._mesa.encontrar_mesa_por_numero(mesa_id)
                if not mesa:
                    raise ValueError(f"Mesa {mesa_id} não existe.")
                mesa.limpar()
                self.console.print_lines([f"[OK] Mesa {mesa_id} limpa e está livre."])
                self.auto_alocar_e_printar(greedy=True)
            except (ValueError, TypeError) as e:
                self.console.print_lines([f"[ERRO] {e}"])

    # ----------------------------- equipe: listar/contratar/demitir --------------
    def listar_equipe_e_printar(self) -> None:

        try:
            lista_para_view = []
            for f in self._func.listar_funcionarios():
                dados_func = {
                    "id": f.id_funcionario,
                    "nome": f.nome,
                    "papel": "Funcionário", 
                    "mesas": 0,
                    "gorjetas": None 
                }
                if isinstance(f, Garcom):
                    dados_func["papel"] = "Garçom"
                    dados_func["mesas"] = len(f.mesas_atendidas)
                    dados_func["gorjetas"] = f._gorjetas 
                elif isinstance(f, Cozinheiro):
                    dados_func["papel"] = "Cozinheiro"
                
                lista_para_view.append(dados_func)

            self.func_v.exibir_funcionarios(lista_para_view)

        except Exception as e:
            self.console.print_lines([f"[ERRO] Não foi possível listar a equipe: {e}"])

    def contratar_garcom_e_printar(self, nome: str, salario: float) -> None:
        garcom_contratado, mensagem = self._func.contratar_garcom(nome, salario)
        
        self.console.print_lines([mensagem])
        if garcom_contratado:
            self.listar_equipe_e_printar()

    def contratar_cozinheiro_e_printar(self, nome: str, salario: float) -> None:
        cozinheiro_contratado, mensagem = self._func.contratar_cozinheiro(nome, salario)
        self.console.print_lines([mensagem])
        if cozinheiro_contratado:
            self.listar_equipe_e_printar()

    def demitir_funcionario_e_printar(self, id_func: int) -> None:
        sucesso, mensagem = self._func.demitir_funcionario(id_func)
        self.console.print_lines([mensagem])
        if sucesso:
            self.listar_equipe_e_printar()

    def adicionar_mesa_e_printar(self, id_mesa: int, capacidade: int) -> None:
        mesa_criada, mensagem = self._mesa.cadastrar_mesa(id_mesa, capacidade)
        self.console.print_lines([mensagem])
        if mesa_criada:
            self.mesa_v.exibir_mesas([self._mesa_dict(m) for m in self._mesa.listar_mesas()])
            self.auto_alocar_e_printar(greedy=False)
    def ver_prato_mais_pedido_e_printar(self) -> None:

        try:
            estatisticas = self._pedido_controller.get_estatisticas_pratos()
            
            if not estatisticas:
                self.console.print_lines(["[INFO] Nenhuma estatística de pedidos disponível ainda."])
                return

            prato_mais_pedido = max(estatisticas, key=estatisticas.get)
            quantidade = estatisticas[prato_mais_pedido]

            dados_para_view = {
                "prato_nome": prato_mais_pedido.nome,
                "quantidade": quantidade
            }
            
            self.pedido_v.exibir_prato_mais_pedido(dados_para_view)
        
        except Exception as e:
            self.console.print_lines([f"[ERRO] Não foi possível gerar as estatísticas: {e}"])