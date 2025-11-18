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

    def get_cardapio_data(self) -> List[Dict[str, object]]:
        return self._cardapio.listar_pratos_para_view()
    
    def print_dashboard(self) -> None:
        dados = {
            "mesas": self._mesa.listar_mesas_para_view(),
            "fila": self._fila.listar_para_view(),
            "garcons": self._func.listar_garcons_para_view(),   
            "cardapio": self._cardapio.listar_pratos_para_view()
        }
        self.console.render_dashboard(dados)
        self.mesa_v.exibir_mesas(dados["mesas"])
        self.fila_v.exibir_fila(dados["fila"])

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

                # Tenta designar um garçom (não bloqueante se falhar)
                garcom = None
                try:
                    garcom = self._func.encontrar_garcom_disponivel()
                    if garcom:
                        self._mesa.designar_garcom(mesa, garcom)
                except (ValueError, TypeError) as e_garcom:
                    self.console.print_lines([f"[AVISO] {e_garcom}"])
                    garcom = None 
                
                conta = None
                try:
                    self._mesa.ocupar_mesa(mesa.id_mesa, grupo)
                    conta = self._conta.abrir_nova_conta(grupo, mesa)
                except (ValueError, TypeError) as e_alocar:
                    self.console.print_lines([f"[AVISO] Falha ao auto-alocar Grupo {grupo.id_grupo}: {e_alocar}"])
                    if not greedy:
                        break
                    else:
                        continue
                
                # Se deu certo, remove da fila e registra
                self._fila.remover(grupo)
                
                msgs.append(f"[ALOCADO] Grupo {grupo.id_grupo} ({grupo.numero_pessoas}) -> Mesa {mesa.id_mesa} "
                            f"(Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}")

                self.conta_v.exibir_extrato(self._pedido_controller.conta_para_view(conta))

            if msgs:
                self.console.print_lines(msgs)
        except Exception as e:
            self.console.print_lines([f"[ERRO] Falha durante a auto-alocação: {e}"])

    def receber_clientes_e_printar(self, qtd: int) -> None:
        try:
            # 1. Cria o grupo (lança erro se qtd for inválida)
            grupo = self._cliente.criar_grupo(qtd)

            # 2. Busca mesa
            mesa = self._mesa.encontrar_mesa_livre(grupo.numero_pessoas)
            
            # 3. Se não tem mesa, vai para a fila
            if not mesa:
                self._fila.adicionar_grupo(grupo)
                self.console.print_lines([f"[FILA] {grupo} adicionado à fila."])
                return

            # 4. Se tem mesa, tenta designar garçom
            garcom = None
            try:
                garcom = self._func.encontrar_garcom_disponivel()
                if garcom:
                    self._mesa.designar_garcom(mesa, garcom)
            except (ValueError, TypeError) as e_garcom:
                self.console.print_lines([f"[AVISO] {e_garcom}"])
                garcom = None 

            # 5. Ocupa a mesa e abre a conta
            self._mesa.ocupar_mesa(mesa.id_mesa, grupo)
            conta = self._conta.abrir_nova_conta(grupo, mesa)

            # 6. Feedback
            self.console.print_lines([f"[ALOCADO] {grupo} -> Mesa {mesa.id_mesa} (Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}"])
            self.conta_v.exibir_extrato(self._pedido_controller.conta_para_view(conta))

        except (ValueError, TypeError, RuntimeError) as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def finalizar_atendimento_e_printar(self, mesa_id: int, gorjeta: float = 0.0) -> None:
        try:
            # 1. Busca a conta
            conta = self._conta.encontrar_conta_por_mesa(mesa_id)
            if not conta:
                raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

            # 2. Processa a gorjeta (se houver)
            garcom_responsavel = conta.mesa.garcom_responsavel
            if garcom_responsavel and gorjeta > 0:
                try:
                    garcom_responsavel.adicionar_gorjeta(gorjeta)
                    self.console.print_lines([f"[INFO] Gorjeta de R$ {gorjeta:.2f} registrada para o Garçom {garcom_responsavel.nome}."])
                except (ValueError, TypeError) as e:
                    self.console.print_lines([f"[AVISO] Não foi possível registrar a gorjeta: {e}"])
            
            # 3. Prepara dados para exibição final
            total = conta.calcular_total()
            extrato_data = self._pedido_controller.conta_para_view(conta)

            # 4. Fecha a conta
            self._conta.fechar_conta(conta)

            # 5. Libera a mesa (status vira SUJA)
            self._mesa.liberar_mesa(mesa_id)
            msg_mesa = f"Mesa {mesa_id} liberada e aguardando limpeza."

            # 6. Feedback
            self.conta_v.exibir_extrato(extrato_data)
            self.console.print_lines([f"[OK] Conta #{conta.id_conta} fechada (R$ {total:.2f}). {msg_mesa}"])

        except (ValueError, TypeError, RuntimeError) as e:
            self.console.print_lines([f"[ERRO] {e}"])

    def limpar_mesa_e_printar(self, mesa_id: int) -> None:
            try:
                self._mesa.limpar_mesa(mesa_id)
                
                self.console.print_lines([f"[OK] Mesa {mesa_id} limpa e está livre."])
                self.auto_alocar_e_printar(greedy=True)
            except (ValueError, TypeError) as e:
                self.console.print_lines([f"[ERRO] {e}"])

    def listar_equipe_e_printar(self) -> None:

        try:
            lista_para_view = []
            for f in self._func.listar_funcionarios():
                dados_func = {
                    "id": f.id_funcionario,
                    "nome": f.nome,
                    "papel": "Funcionário", 
                    "mesas": 0,
                    "salario": f.salario_base,
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
        try:    
            garcom_contratado = self._func.contratar_garcom(nome, salario)
            mensagem = f"[OK] Garçom {garcom_contratado.nome} (ID: {garcom_contratado.id_funcionario}) contratado."
            self.console.print_lines([mensagem])
            self.listar_equipe_e_printar()
            
        except (ValueError, TypeError) as e:
            mensagem = f"[ERRO] Não foi possível contratar o garçom: {e}"
            self.console.print_lines([mensagem])

    def contratar_cozinheiro_e_printar(self, nome: str, salario: float) -> None:
        try:
            cozinheiro_contratado = self._func.contratar_cozinheiro(nome, salario)
            mensagem = f"[OK] Cozinheiro {cozinheiro_contratado.nome} (ID: {cozinheiro_contratado.id_funcionario}) contratado."
            self.console.print_lines([mensagem])
            self.listar_equipe_e_printar()
        except (ValueError, TypeError) as e:
            mensagem = f"[ERRO] Não foi possível contratar o cozinheiro: {e}"
            self.console.print_lines([mensagem])

    def demitir_funcionario_e_printar(self, id_func: int) -> None:
        try:
            func_demitido = self._func.demitir_funcionario(id_func)
            
            mensagem = f"[OK] Funcionário {func_demitido.nome} (ID: {func_demitido.id_funcionario}) foi demitido."
            self.console.print_lines([mensagem])
            self.listar_equipe_e_printar()

        except ValueError as e:
            mensagem = f"[ERRO] {e}"
            self.console.print_lines([mensagem])

    def adicionar_mesa_e_printar(self, id_mesa: int, capacidade: int) -> None:
        try:
            mesa_criada = self._mesa.cadastrar_mesa(id_mesa, capacidade)
            mensagem = f"Mesa {mesa_criada.id_mesa} cadastrada com sucesso."
            self.console.print_lines([mensagem])
            self.mesa_v.exibir_mesas([self._mesa.mesa_para_dict(m) for m in self._mesa.listar_mesas()])
            self.auto_alocar_e_printar(greedy=False)
            
        except (ValueError, TypeError) as e:
            mensagem = str(e)
            self.console.print_lines([f"[ERRO] {mensagem}"])
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
    
    def renomear_funcionario_e_printar(self, id_func: int, novo_nome: str) -> None:
        try:
            func_atualizado = self._func.atualizar_nome(id_func, novo_nome)
            
            mensagem = f"[OK] Nome atualizado para '{func_atualizado.nome}' (ID {func_atualizado.id_funcionario})."
            self.console.print_lines([mensagem])

        except (ValueError, TypeError) as e:
            mensagem = f"[ERRO] {e}"
            self.console.print_lines([mensagem])

    def atualizar_salario_funcionario_e_printar(self, id_func: int, novo_salario: float) -> None:
        try:
            func_atualizado = self._func.atualizar_salario(id_func, novo_salario)
            
            mensagem = f"[OK] Salário atualizado para R$ {func_atualizado.salario_base:.2f} (ID {func_atualizado.id_funcionario})."
            self.console.print_lines([mensagem])
            
        except (ValueError, TypeError) as e:
            mensagem = f"[ERRO] {e}"
            self.console.print_lines([mensagem])