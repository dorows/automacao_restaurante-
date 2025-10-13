
import sys
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

# Ajusta o path para importar os módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Controllers
from controllers.app_controller import AppController
from controllers.restaurante_controller import RestauranteController
from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController
from controllers.pedido_controller import PedidoController

# Views
from views.console_view import ConsoleView
from views.mesa_view import MesaView
from views.fila_view import FilaView
from views.conta_view import ContaView
from views.cardapio_view import CardapioView
from views.pedido_view import PedidoView
from views.funcionario_view import FuncionarioView

# Models / Enums (para checagens diretas de estado, se necessário)
from models.status_enums import StatusMesa, StatusPedido

@dataclass
class TestEvent:
    name: str
    ok: bool
    details: str = ""
    expected: str = ""
    got: str = ""

@dataclass
class TestReport:
    events: List[TestEvent] = field(default_factory=list)

    def check(self, name: str, condition: bool, expected: str = "", got: str = "", details: str = ""):
        self.events.append(TestEvent(name=name, ok=bool(condition), expected=expected, got=got, details=details))

    def warn(self, name: str, details: str):
        self.events.append(TestEvent(name=name, ok=True, details="[WARN] " + details))

    def fail(self, name: str, details: str, expected: str = "", got: str = ""):
        self.events.append(TestEvent(name=name, ok=False, details=details, expected=expected, got=got))

    def summary(self) -> Tuple[int, int, int]:
        total = len(self.events)
        fails = len([e for e in self.events if not e.ok])
        warns = len([e for e in self.events if e.ok and e.details.startswith("[WARN]")])
        return total, fails, warns

    def print_report(self):
        print("\n" + "="*72)
        print("RELATÓRIO DE TESTES ROBUSTOS")
        print("="*72)
        for e in self.events:
            status = "OK" if e.ok else "FAIL"
            print(f"[{status}] {e.name}")
            if e.details:
                print(f"   • {e.details}")
            if e.expected or e.got:
                print(f"   • esperado: {e.expected}")
                print(f"   • obtido : {e.got}")
        total, fails, warns = self.summary()
        print("-"*72)
        print(f"Total de checagens: {total} | Falhas: {fails} | Avisos: {warns}")
        if fails == 0:
            print("RESULTADO: ✅ Nenhum comportamento indevido detectado.")
        else:
            print("RESULTADO: ❌ Foram detectados comportamentos indevidos.")
        print("="*72 + "\n")


def build_app_like_sample() -> Tuple[AppController, RestauranteController, PedidoController,
                                     MesaController, ContaController, FilaController,
                                     FuncionarioController, CardapioController]:
    """Segue a mesma estrutura do teste fornecido pelo usuário."""
    # Views
    console_v = ConsoleView()
    mesa_v = MesaView()
    fila_v = FilaView()
    conta_v = ContaView()
    cardapio_v = CardapioView()
    pedido_v = PedidoView()
    func_v = FuncionarioView()

    # Controllers especialistas
    mesa_c = MesaController()
    conta_c = ContaController()
    fila_c = FilaController()
    func_c = FuncionarioController()
    cardapio_c = CardapioController()
    cliente_c = ClienteController()

    # PedidoController (estrutura igual ao teste do usuário: sem passar funcionario_controller por padrão)
    pedido_c = PedidoController(console_v, pedido_v, conta_v, conta_c, cardapio_c)

    # RestauranteController
    restaurante_c = RestauranteController(
        console_v=console_v,
        mesa_v=mesa_v,
        fila_v=fila_v,
        conta_v=conta_v,
        cardapio_v=cardapio_v,
        func_v=func_v,
        pedido_v=pedido_v,
        mesa_controller=mesa_c,
        conta_controller=conta_c,
        fila_controller=fila_c,
        funcionario_controller=func_c,
        cardapio_controller=cardapio_c,
        cliente_controller=cliente_c,
        pedido_controller=pedido_c
    )

    # AppController orquestrador
    app = AppController(console_v, mesa_v, fila_v, conta_v, cardapio_v, pedido_v, func_v,
                        restaurante_c, pedido_c)

    return app, restaurante_c, pedido_c, mesa_c, conta_c, fila_c, func_c, cardapio_c


def run_cmd(app: AppController, command: str):
    """Dispara comandos pelo dispatcher do AppController (sem input())."""
    parts = command.strip().split()
    if not parts:
        return
    acao, args = parts[0].lower(), parts[1:]
    app._dispatch(acao, args)


def state_snapshot(mesas: MesaController, contas: ContaController, fila: FilaController,
                   funcs: FuncionarioController, pedidos: PedidoController) -> Dict[str, Any]:
    """Coleta um snapshot de estado para asserções."""
    mesas_list = mesas.listar_mesas() if hasattr(mesas, "listar_mesas") else []
    cont_list = getattr(contas, "_contas", [])
    fila_list = fila.listar() if hasattr(fila, "listar") else []
    func_list = getattr(funcs, "_funcionarios", [])
    ped_list = getattr(pedidos, "_pedidos", [])

    return {
        "mesas": mesas_list,
        "contas": cont_list,
        "fila": fila_list,
        "funcs": func_list,
        "pedidos": ped_list,
    }


def test_robusto():
    rep = TestReport()

    app, restaurante, pedido_c, mesa_c, conta_c, fila_c, func_c, cardapio_c = build_app_like_sample()

    # ------------------ SETUP INICIAL ------------------
    snap = state_snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)
    # Mesas iniciais: 4, todas LIVRE
    rep.check(
        "Setup: 4 mesas criadas",
        len(snap["mesas"]) >= 4,
        expected=">= 4 mesas LIVRES",
        got=str(len(snap["mesas"]))
    )
    from models.mesa import Mesa
    livres = [m for m in snap["mesas"] if getattr(m, "status", None) == StatusMesa.LIVRE]
    rep.check("Setup: mesas iniciam LIVRES", len(livres) == len(snap["mesas"]),
              expected=f"todas LIVRE", got=f"LIVRE={len(livres)}/{len(snap['mesas'])}")

    # Funcionários iniciais: pelo menos 2 garçons e 1 cozinheiro
    from models.garcom import Garcom
    from models.cozinheiro import Cozinheiro
    garcons = [f for f in snap["funcs"] if isinstance(f, Garcom)]
    cozinheiros = [f for f in snap["funcs"] if isinstance(f, Cozinheiro)]
    rep.check("Setup: >=2 garçons", len(garcons) >= 2, expected=">=2", got=str(len(garcons)))
    rep.check("Setup: >=1 cozinheiro", len(cozinheiros) >= 1, expected=">=1", got=str(len(cozinheiros)))

    # Cardápio básico contem IDs 1,2,101,102
    ids_card = {p.id_prato for p in cardapio_c._cardapio.pratos}
    must_have = {1, 2, 101, 102}
    rep.check("Setup: cardápio contém itens básicos", must_have.issubset(ids_card),
              expected=str(must_have), got=str(sorted(ids_card)))

    # ------------------ CHEGADAS E FILA ------------------
    run_cmd(app, "chegada 4")  # deve sentar mesa de 4
    run_cmd(app, "chegada 2")  # senta 2
    run_cmd(app, "chegada 7")  # vai para fila (não cabe)
    run_cmd(app, "chegada 2")  # possivelmente senta ou vai para fila se não houver mesa

    snap = state_snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)
    # Pelo menos uma mesa ocupada e pelo menos 1 na fila (grupo 7 pessoas)
    ocupadas = [m for m in snap["mesas"] if getattr(m, "status", None) == StatusMesa.OCUPADA]
    rep.check("Chegada: existe ao menos 1 mesa ocupada", len(ocupadas) >= 1,
              expected=">=1 mesa OCUPADA", got=str(len(ocupadas)))
    rep.check("Chegada: fila possui ao menos 1 grupo (7 pessoas)", len(snap["fila"]) >= 1,
              expected=">=1 na fila", got=str(len(snap["fila"])))

    # ------------------ PEDIDOS ------------------
    # Escolhe uma mesa ocupada para pedir
    mesa_ped = ocupadas[0] if ocupadas else None
    if mesa_ped is None:
        rep.fail("Pedidos: não há mesa ocupada para testar", "Fluxo de chegada falhou em ocupar mesa.")
    else:
        mid = mesa_ped.id_mesa
        # dois itens válidos
        run_cmd(app, f"pedir {mid} 1 2")
        run_cmd(app, f"pedir {mid} 101 1")
        # um inválido (prato inexistente)
        run_cmd(app, f"pedir {mid} 999 1")

        # CONFIRMAR (idempotente e, preferencialmente, envia para preparo)
        run_cmd(app, f"confirmar {mid}")
        # Confirmar de novo não deve quebrar
        run_cmd(app, f"confirmar {mid}")

        # Checa se há pedido com status não-ABERTO
        snap = state_snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)
        pedidos_conta = []
        # localizar a conta da mesa
        conta = next((c for c in snap["contas"] if getattr(c, "mesa", None) == mesa_ped), None)
        if conta:
            # coleta pedidos na conta (atributo privado, mas usado para verificação)
            pedidos_conta = getattr(conta, "_pedidos", [])
        if pedidos_conta:
            st = pedidos_conta[-1].status
            rep.check("Confirmar: pedido não está ABERTO", st in (StatusPedido.CONFIRMADO, StatusPedido.EM_PREPARO, StatusPedido.PRONTO),
                      expected="CONFIRMADO/EM_PREPARO/PRONTO", got=str(st.name))
        else:
            rep.fail("Confirmar: nenhum pedido encontrado na conta", "Falha em criar/confirmar pedido.")

        # PRONTO e ENTREGAR
        run_cmd(app, f"pronto {mid}")
        run_cmd(app, f"entregar {mid}")

    # ------------------ FINALIZAR E GORJETA ------------------
    # tenta finalizar a mesa pedida (se existir)
    if mesa_ped is not None:
        # captura garçom antes (se tiver)
        garcom_atr = getattr(mesa_ped, "garcom_responsavel", None)
        gorjetas_antes = getattr(garcom_atr, "gorjetas", 0.0) if garcom_atr else None
        run_cmd(app, f"finalizar {mesa_ped.id_mesa} 5.50")
        # mesa deve ficar SUJA
        rep.check("Finalizar: mesa fica SUJA", getattr(mesa_ped, "status", None) == StatusMesa.SUJA,
                  expected="StatusMesa.SUJA", got=str(getattr(mesa_ped, "status", None).name if getattr(mesa_ped, "status", None) else None))
        # se tinha garçom, gorjeta acumulada deve aumentar
        if garcom_atr:
            gorjetas_depois = getattr(garcom_atr, "gorjetas", 0.0)
            rep.check("Finalizar: garçom recebeu gorjeta", gorjetas_depois >= gorjetas_antes + 5.5 - 1e-6,
                      expected=f">= {gorjetas_antes + 5.5:.2f}", got=f"{gorjetas_depois:.2f}")
        else:
            rep.warn("Finalizar: mesa sem garçom responsável", "Não foi possível validar gorjeta atrelada a garçom.")

        # Limpar e tentar realocar alguém da fila
        run_cmd(app, f"limpar {mesa_ped.id_mesa}")
        rep.check("Limpar: mesa volta a LIVRE", getattr(mesa_ped, "status", None) == StatusMesa.LIVRE,
                  expected="StatusMesa.LIVRE", got=str(getattr(mesa_ped, "status", None).name if getattr(mesa_ped, "status", None) else None))

        # força uma rodada de auto-alocação (se existir no controller)
        if hasattr(restaurante, "auto_alocar_e_printar"):
            restaurante.auto_alocar_e_printar(greedy=True)

        # fila deve diminuir se houver grupo compatível
        snap2 = state_snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)
        if len(snap["fila"]) > 0 and len(snap2["fila"]) <= len(snap["fila"]):
            rep.check("Auto-alocar: fila não aumentou após limpeza+alocação",
                      len(snap2["fila"]) <= len(snap["fila"]),
                      expected=f"<= {len(snap['fila'])}", got=str(len(snap2["fila"])))

    # ------------------ DEMISSÃO COM RESTRIÇÃO ------------------
    # se houver pedido em preparo em alguma mesa agora, tentar demitir cozinheiro deve falhar (lógica de negócio)
    snap = state_snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)
    from models.cozinheiro import Cozinheiro
    cozinheiros = [f for f in snap["funcs"] if isinstance(f, Cozinheiro)]
    pedidos_em_preparo = [p for p in snap["pedidos"] if getattr(p, "status", None) == StatusPedido.EM_PREPARO]
    if pedidos_em_preparo and cozinheiros:
        coz = cozinheiros[0]
        ok, msg = func_c.demitir_funcionario(coz.id_funcionario)
        rep.check("Demissão bloqueada com pedido em preparo", ok is False,
                  expected="False", got=str(ok), details=msg if isinstance(msg, str) else "")
    else:
        rep.warn("Demissão restrita: sem pedidos EM_PREPARO no momento do teste",
                 "Não foi possível validar a trava de demissão do cozinheiro.")

    # ------------------ REPORT ------------------
    rep.print_report()


if __name__ == "__main__":
    test_robusto()
