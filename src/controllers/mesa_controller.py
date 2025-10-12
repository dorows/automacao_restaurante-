from typing import List, Optional
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.status_enums import StatusMesa

class MesaController:
    def __init__(self):
        self._mesas: List[Mesa] = []
        self._setup_inicial()

    def _setup_inicial(self):
        self._mesas.extend([
            Mesa(id_mesa=1, capacidade=4),
            Mesa(id_mesa=2, capacidade=2),
            Mesa(id_mesa=3, capacidade=2),
            Mesa(id_mesa=4, capacidade=6),
        ])

    # -------------------------------------------------------------------------
    # Consultas
    def listar_mesas(self) -> List[Mesa]:
        return self._mesas

    def encontrar_mesa_por_numero(self, numero_mesa: int) -> Optional[Mesa]:
        return next((m for m in self._mesas if m.id_mesa == numero_mesa), None)

    def encontrar_mesa_livre(self, qtd_pessoas: int) -> Optional[Mesa]:
        """Escolhe a menor mesa que comporte o grupo (desempate por id)."""
        melhor: Optional[Mesa] = None
        for m in self._mesas:
            if m.status == StatusMesa.LIVRE and m.capacidade >= qtd_pessoas:
                if (melhor is None or
                    m.capacidade < melhor.capacidade or
                    (m.capacidade == melhor.capacidade and m.id_mesa < melhor.id_mesa)):
                    melhor = m
        return melhor

    def ocupar_mesa(self, numero_mesa: int, grupo: GrupoCliente) -> bool:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        return bool(mesa and mesa.ocupar(grupo))

    def liberar_mesa(self, numero_mesa: int) -> bool:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        if mesa and mesa.status == StatusMesa.OCUPADA:
            mesa.liberar()   # vai a SUJA
            mesa.limpar()    # SUJA -> LIVRE; também zera conta e garçom_responsavel
            return True
        return False

    def designar_garcom(self, mesa: Mesa, garcom: Garcom) -> bool:
        if not mesa or not garcom:
            return False

        # Se já estiver com o mesmo garçom, nada a fazer
        if getattr(mesa, "garcom_responsavel", None) is garcom:
            return True

        # Se havia outro garçom, desfaça vínculo simétrico
        antigo = getattr(mesa, "garcom_responsavel", None)
        if antigo is not None and antigo is not garcom:
            mesa.garcom_responsavel = None
            try:
                antigo.remover_mesa(mesa)
            except Exception:
                pass

        # Pede ao garçom para assumir a mesa; só depois escreve na mesa
        if garcom.adicionar_mesa(mesa):
            mesa.garcom_responsavel = garcom
            return True

        # Se o garçom recusou (lotado), mantém mesa sem responsável
        return False

    def cadastrar_mesa(self, id_mesa: int, capacidade: int) -> Optional[Mesa]:
        if id_mesa <= 0 or capacidade <= 0:
            return None
        if self.encontrar_mesa_por_numero(id_mesa) is not None:
            return None

        nova = Mesa(id_mesa=id_mesa, capacidade=capacidade)
        self._mesas.append(nova)
        return nova