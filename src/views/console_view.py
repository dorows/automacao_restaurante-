from typing import Tuple, List, Dict, Callable, Optional
from controllers.restaurante_controller import RestauranteController
from views.mesa_view import MesaView
from views.funcionario_view import FuncionarioView
from views.cardapio_view import CardapioView
from views.conta_view import ContaView
from views.pedido_view import PedidoView
from views.fila_view import FilaView
from core.result import Result

class ConsoleView:
    def __init__(self, restaurante: RestauranteController):
        self.restaurante = restaurante
        self.mesa_view = MesaView()
        self.func_view = FuncionarioView()
        self.card_view = CardapioView()
        self.conta_view = ContaView()
        self.pedido_view = PedidoView()
        self.fila_view = FilaView()

        self.handlers: Dict[str, Callable[[List[str]], None]] = {
            "chegada": self.handle_chegada,
            "pedir": self.handle_pedir,
            "confirmar": self.handle_confirmar,  
            "pronto": self.handle_pronto,        
            "finalizar": self.handle_finalizar,
            "limpar": self.handle_limpar_mesa,
            "equipe": self.handle_equipe,
            "cardapio": self.handle_cardapio,
            "mesas": self.handle_mesas,
            "fila": self.handle_fila,
            "ajuda": self.handle_ajuda,
            "sair": self.handle_sair,
            "mesaadd": self.handle_mesa_add,
        }
        self._rodando = True

    def loop(self):
        while self._rodando:
            self.render_dashboard()
            acao, args = self.obter_comando()
            handler = self.handlers.get(acao)
            if handler:
                handler(args)
            else:
                self.exibir_mensagem("Comando inválido. Digite 'ajuda' para ver os comandos.")

    def render_dashboard(self):
        print("\n" + "="*62)
        print("PAINEL DO RESTAURANTE".center(62))
        print("="*62)
        self.mesa_view.exibir_mesas(self.restaurante.mesas)
        self.fila_view.exibir_fila(self.restaurante.fila_de_espera)

    def obter_comando(self) -> Tuple[str, List[str]]:
        prompt = (
            "\nDigite um comando:\n"
            "  - chegada [n_pessoas]\n"
            "  - pedir [n_mesa] [id_prato] [qtd]\n"
            "  - confirmar [id_pedido]\n"
            "  - pronto [id_pedido]\n"
            "  - finalizar [n_mesa]\n"
            "  - limpar [n_mesa]\n"
            "  - equipe | cardapio | mesas | fila | ajuda | sair\n"
            "> "
        )
        partes = input(prompt).strip().split()
        if not partes:
            return "ajuda", []
        return partes[0].lower(), partes[1:]

    def exibir_mensagem(self, mensagem: str):
        print(mensagem)

    def handle_chegada(self, args: List[str]):
        if len(args) != 1 or not args[0].isdigit():
            self.exibir_mensagem("[ERRO] Uso: chegada [n_pessoas]")
            return
        n = int(args[0])
        r: Result = self.restaurante.receber_clientes(n)
        self._render_result(r)

        if r.status == "ok" and r.message_key == "grupo_alocado":
            conta = r.data["conta"]
            self.conta_view.exibir_extrato(conta)

    def handle_pedir(self, args: List[str]):
        if len(args) != 3:
            self.exibir_mensagem("[ERRO] Uso: pedir [n_mesa] [id_prato] [qtd]")
            return
        try:
            n_mesa, id_prato, qtd = map(int, args)
        except ValueError:
            self.exibir_mensagem("[ERRO] Argumentos devem ser inteiros.")
            return
        r: Result = self.restaurante.realizar_pedido(n_mesa, id_prato, qtd)
        self._render_result(r)
        if r.status == "ok":
            conta = r.data["conta"]
            self.conta_view.exibir_extrato(conta)

    def handle_confirmar(self, args: List[str]):
        self.exibir_mensagem("[TODO] confirmar [id_pedido] (expor no controller)")

    def handle_pronto(self, args: List[str]):
        self.exibir_mensagem("[TODO] pronto [id_pedido] (expor no controller)")

    def handle_finalizar(self, args: List[str]):
        if len(args) != 1:
            self.exibir_mensagem("[ERRO] Uso: finalizar [n_mesa]")
            return
        n_mesa = int(args[0])
        r: Result = self.restaurante.finalizar_atendimento(n_mesa)
        self._render_result(r)
        if r.status == "ok":
            # Mostrar extrato final
            conta = r.data["conta"]
            self.conta_view.exibir_extrato(conta)

    def handle_limpar_mesa(self, args: List[str]):
        if len(args) != 1:
            self.exibir_mensagem("[ERRO] Uso: limpar [n_mesa]")
            return
        n_mesa = int(args[0])
        r = self.restaurante.limpar_mesa(n_mesa)
        self._render_result(r)
        if not mesa:
            self.exibir_mensagem("[ERRO] Mesa inexistente.")
            return
        ok = mesa.limpar()
        if ok:
            self.exibir_mensagem("[OK] Mesa limpa e livre.")
        else:
            self.exibir_mensagem("[ERRO] Mesa não está suja.")

    def handle_equipe(self, args: List[str]):
        self.func_view.exibir_funcionarios(self.restaurante.funcionarios)

    def handle_cardapio(self, args: List[str]):
        self.card_view.exibir_cardapio(self.restaurante.cardapio)

    def handle_mesas(self, args: List[str]):
        self.mesa_view.exibir_mesas(self.restaurante.mesas)

    def handle_fila(self, args: List[str]):
        self.fila_view.exibir_fila(self.restaurante.fila_de_espera)

    def handle_ajuda(self, args: List[str]):
        self.exibir_mensagem("Comandos: chegada, pedir, confirmar, pronto, finalizar, limpar, equipe, cardapio, mesas, fila, sair")

    def handle_sair(self, args: List[str]):
        self._rodando = False
        self.exibir_mensagem("Saindo...")

    def handle_mesa_add(self, args):
        if len(args) != 2 or not all(a.isdigit() for a in args):
            self.exibir_mensagem("[ERRO] Uso: mesaadd [id_mesa] [capacidade]")
            return
        id_mesa, cap = map(int, args)
        r = self.restaurante.cadastrar_mesa(id_mesa, cap)
        self._render_result(r)

    def _render_result(self, r: Result):
        messages = {
            # sucesso
            "grupo_alocado": lambda d: f"Bem-vindo! Grupo {d['grupo'].id_grupo} sentado na Mesa {d['mesa'].id_mesa}" + (f" (Garçom: {d['garcom'].nome})" if d.get("garcom") else ""),
            "grupo_para_fila": lambda d: f"{d['grupo']} adicionado à fila de espera.",
            "item_adicionado": lambda d: f"Item '{d['prato'].nome}' (x{d['quantidade']}) adicionado ao pedido da Mesa {d['conta'].mesa.id_mesa}.",
            "conta_fechada":   lambda d: f"Conta #{d['conta'].id_conta} fechada. Mesa {d['mesa'].id_mesa} marcada como SUJA.",
            "mesa_limpa": lambda d: f"Mesa {d['mesa'].id_mesa} limpa e livre.",
            "mesa_nao_suja": lambda d: "[ERRO] Mesa não está suja.",
            "pedido_confirmado": lambda d: f"Pedido #{d['pedido'].id_pedido} confirmado.",
            "pedido_pronto":     lambda d: f"Pedido #{d['pedido'].id_pedido} pronto para servir.",
            "pedido_nao_confirmado": lambda d: "[ERRO] Não foi possível confirmar (status inválido?).",
            "pedido_nao_pronto":     lambda d: "[ERRO] Não foi possível marcar como pronto (status inválido?).",


            # erros
            "grupo_invalido":      lambda d: "[ERRO] Número de pessoas inválido.",
            "mesa_invalida":       lambda d: "[ERRO] Mesa inválida ou não está ocupada.",
            "conta_nao_encontrada":lambda d: "[ERRO] Nenhuma conta ativa para a mesa informada.",
            "prato_nao_encontrado":lambda d: "[ERRO] ID de prato inexistente.",
            "item_nao_adicionado": lambda d: "[ERRO] Não foi possível adicionar o item (conta fechada? pedido não aberto? quantidade inválida?).",
        }

        if r.status == "ok":
            if r.message_key and r.message_key in messages:
                self.exibir_mensagem(messages[r.message_key](r.data or {}))
            else:
                self.exibir_mensagem("[OK]")
        else:
            key = r.error or r.message_key
            if key and key in messages:
                self.exibir_mensagem(messages[key](r.data or {}))
            else:
                self.exibir_mensagem(f"[ERRO] {r.error or 'Operação inválida.'}")
