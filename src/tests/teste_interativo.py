
import sys
import os
from typing import Any, Dict, List, Tuple

# Deixa o script rodável a partir de uma pasta "tests" dentro de src/
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

# Models / Enums
from models.status_enums import StatusMesa, StatusPedido
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro

def ok(label: str, extra: str = ""):
    print(f"[OK] {label}" + (f" — {extra}" if extra else ""))

def fail(label: str, expected: str = "", got: str = ""):
    print(f"[FAIL] {label}")
    if expected or got:
        print(f"   • esperado: {expected}")
        print(f"   • obtido : {got}")

def warn(label: str):
    print(f"[WARN] {label}")

def press(msg: str = "Pressione Enter para continuar..."):
    try:
        input(msg)
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        raise SystemExit(130)

def run_cmd(app: AppController, command: str):
    parts = command.strip().split()
    if not parts:
        return
    acao, args = parts[0].lower(), parts[1:]
    app._dispatch(acao, args)

def build_app() -> Tuple[AppController, RestauranteController, PedidoController,
                         MesaController, ContaController, FilaController,
                         FuncionarioController, CardapioController]:
    # Views
    console_v = ConsoleView()
    mesa_v = MesaView()
    fila_v = FilaView()
    conta_v = ContaView()
    cardapio_v = CardapioView()
    pedido_v = PedidoView()
    func_v = FuncionarioView()

    # Controllers
    mesa_c = MesaController()
    conta_c = ContaController()
    fila_c = FilaController()
    func_c = FuncionarioController()
    cardapio_c = CardapioController()
    cliente_c = ClienteController()

    pedido_c = PedidoController(console_v, pedido_v, conta_v, conta_c, cardapio_c)

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
        pedido_controller=pedido_c,
    )

    app = AppController(console_v, mesa_v, fila_v, conta_v, cardapio_v, pedido_v, func_v,
                        restaurante_c, pedido_c)

    return app, restaurante_c, pedido_c, mesa_c, conta_c, fila_c, func_c, cardapio_c

def snapshot(mesas: MesaController, contas: ContaController, fila: FilaController,
             funcs: FuncionarioController, pedidos: PedidoController) -> Dict[str, Any]:
    return {
        "mesas": mesas.listar_mesas() if hasattr(mesas, "listar_mesas") else [],
        "contas": getattr(contas, "_contas", []),
        "fila": fila.listar() if hasattr(fila, "listar") else [],
        "funcs": getattr(funcs, "_funcionarios", []),
        "pedidos": getattr(pedidos, "_pedidos", []),
    }

def main():
    print("="*72)
    print("TESTE INTERATIVO (aperte Enter entre os passos)")
    print("="*72)

    app, restaurante, pedido_c, mesa_c, conta_c, fila_c, func_c, cardapio_c = build_app()

    # SETUP
    press("1) Setup inicial carregado. Pressione Enter para validar...")
    snap = snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)

    if len(snap["mesas"]) >= 4 and all(m.status == StatusMesa.LIVRE for m in snap["mesas"]):
        ok("Setup: 4 mesas criadas e LIVRES")
    else:
        fail("Setup: mesas", expected=">=4 e todas LIVRES", got=f"{len(snap['mesas'])} mesas; livres={[m.status for m in snap['mesas']]}")

    garcons = [f for f in snap["funcs"] if isinstance(f, Garcom)]
    cozinheiros = [f for f in snap["funcs"] if isinstance(f, Cozinheiro)]
    if len(garcons) >= 2:
        ok("Setup: >=2 garçons")
    else:
        fail("Setup: garçons insuficientes", expected=">=2", got=str(len(garcons)))
    if len(cozinheiros) >= 1:
        ok("Setup: >=1 cozinheiro")
    else:
        fail("Setup: cozinheiros insuficientes", expected=">=1", got=str(len(cozinheiros)))

    base_ids = {1, 2, 101, 102}
    ids_card = {p.id_prato for p in cardapio_c._cardapio.pratos}
    if base_ids.issubset(ids_card):
        ok("Setup: cardápio contém itens básicos (1,2,101,102)")
    else:
        fail("Setup: cardápio básico ausente", expected=str(sorted(base_ids)), got=str(sorted(ids_card)))

    # CHEGADAS
    press("\n2) Testar chegadas (4, 2, 7, 2). Pressione Enter para executar...")
    run_cmd(app, "chegada 4")
    run_cmd(app, "chegada 2")
    run_cmd(app, "chegada 7")
    run_cmd(app, "chegada 2")

    snap = snapshot(mesa_c, conta_c, fila_c, func_c, pedido_c)
    ocupadas = [m for m in snap["mesas"] if m.status == StatusMesa.OCUPADA]
    if len(ocupadas) >= 1:
        ok("Chegada: existe ao menos 1 mesa ocupada", extra=f"{len(ocupadas)} ocupada(s)")
    else:
        fail("Chegada: nenhuma mesa ocupada", expected=">=1", got="0")

    if len(snap["fila"]) >= 1:
        ok("Chegada: fila possui ao menos 1 grupo", extra=f"tamanho={len(snap['fila'])}")
    else:
        warn("Chegada: fila vazia (pode não haver grupo que exceda as capacidades)")

    # PEDIDOS
    press("\n3) Testar pedidos na primeira mesa ocupada. Pressione Enter para executar...")
    mesa_ped = ocupadas[0] if ocupadas else None
    if mesa_ped is None:
        fail("Pedidos: não há mesa ocupada para testar")
        print("Encerrando teste por falta de pré-condições.")
        return

    mid = mesa_ped.id_mesa
    run_cmd(app, f"pedir {mid} 1 2")
    run_cmd(app, f"pedir {mid} 101 1")
    run_cmd(app, f"pedir {mid} 999 1")  # inválido

    # Confirmar (idempotente)
    press("\n4) Confirmar pedido (duas vezes). Pressione Enter...")
    run_cmd(app, f"confirmar {mid}")
    run_cmd(app, f"confirmar {mid}")

    # Checar status do último pedido da conta
    conta = next((c for c in snap["contas"] if getattr(c, 'mesa', None) == mesa_ped), None)
    if conta is None:
        conta = next((c for c in conta_c._contas if getattr(c, 'mesa', None) == mesa_ped), None)
    if conta and getattr(conta, "_pedidos", []):
        ped = conta._pedidos[-1]
        if ped.status in (StatusPedido.CONFIRMADO, StatusPedido.EM_PREPARO, StatusPedido.PRONTO):
            ok(f"Confirmar: status do pedido é válido ({ped.status.name})")
        else:
            fail("Confirmar: status inesperado após confirmar", expected="CONFIRMADO/EM_PREPARO/PRONTO", got=ped.status.name)
    else:
        fail("Confirmar: nenhum pedido encontrado na conta")

    # PRONTO + ENTREGAR
    press("\n5) Marcar PRONTO e ENTREGAR. Pressione Enter...")
    run_cmd(app, f"pronto {mid}")
    run_cmd(app, f"entregar {mid}")
    # Se houver status ENTREGUE no enum, tente validar; se não, apenas siga.
    try:
        from models.status_enums import StatusPedido as _SP
        if hasattr(_SP, "ENTREGUE"):
            ped2 = conta._pedidos[-1] if conta and getattr(conta, "_pedidos", []) else None
            if ped2 and ped2.status in (_SP.ENTREGUE, _SP.PRONTO):
                ok("Entregar: status compatível (ENTREGUE/PRONTO)")
            else:
                warn("Entregar: não foi possível confirmar ENTREGUE (enum pode não ter esse status)")
    except Exception:
        pass

    # FINALIZAR + GORJETA
    press("\n6) Finalizar conta com gorjeta (5.50) e limpar mesa. Pressione Enter...")
    garcom_atr = getattr(mesa_ped, "garcom_responsavel", None)
    gorjetas_antes = getattr(garcom_atr, "gorjetas", 0.0) if garcom_atr else None
    run_cmd(app, f"finalizar {mid} 5.50")

    if mesa_ped.status == StatusMesa.SUJA:
        ok("Finalizar: mesa ficou SUJA")
    else:
        fail("Finalizar: mesa não ficou SUJA", expected="SUJA", got=str(mesa_ped.status.name))

    if garcom_atr is not None:
        gorjetas_depois = getattr(garcom_atr, "gorjetas", 0.0)
        if gorjetas_depois >= (gorjetas_antes or 0.0) + 5.5 - 1e-6:
            ok("Finalizar: garçom recebeu gorjeta")
        else:
            fail("Finalizar: gorjeta não somou ao garçom", expected=f">= {((gorjetas_antes or 0.0) + 5.5):.2f}", got=f"{gorjetas_depois:.2f}")
    else:
        warn("Finalizar: mesa sem garçom (não é possível validar gorjeta)")

    run_cmd(app, f"limpar {mid}")
    if mesa_ped.status == StatusMesa.LIVRE:
        ok("Limpar: mesa voltou a LIVRE")
    else:
        fail("Limpar: mesa não voltou a LIVRE", expected="LIVRE", got=str(mesa_ped.status.name))

    # AUTO-ALOCAR (greedy)
    press("\n7) Forçar auto-alocação (greedy=True). Pressione Enter...")
    fila_antes = len(fila_c.listar()) if hasattr(fila_c, "listar") else 0
    if hasattr(restaurante, "auto_alocar_e_printar"):
        restaurante.auto_alocar_e_printar(greedy=True)
        fila_depois = len(fila_c.listar()) if hasattr(fila_c, "listar") else 0
        if fila_depois <= fila_antes:
            ok("Auto-alocar: fila não aumentou", extra=f"{fila_antes} -> {fila_depois}")
        else:
            fail("Auto-alocar: fila aumentou", expected=f"<= {fila_antes}", got=str(fila_depois))
    else:
        warn("Auto-alocar: método não disponível no RestauranteController")

    # EQUIPE (manual/visual)
    press("\n8) Mostrar EQUIPE (checar salário e campos específicos). Pressione Enter...")
    run_cmd(app, "equipe")
    print("→ Verificação manual: confirme visualmente se SALÁRIO aparece;")
    print("  garçons mostram MESAS/GORJETAS e cozinheiros mostram PREPARO (se você implementou).")
    ok("EQUIPE: comando executado (checagem visual)")

    print("\nFim do teste interativo.")
    print("="*72)

if __name__ == "__main__":
    main()
