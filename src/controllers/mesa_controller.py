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
            Mesa(id_mesa=4, capacidade=6)
        ])

    def listar_mesas(self) -> List[Mesa]:
        return self._mesas

    def encontrar_mesa_por_numero(self, numero_mesa: int) -> Optional[Mesa]:
        return next((m for m in self._mesas if m.id_mesa == numero_mesa), None)

    def encontrar_mesa_livre(self, qtd_pessoas: int) -> Optional[Mesa]:
        for mesa in self._mesas:
            if mesa.status == StatusMesa.LIVRE and mesa.capacidade >= qtd_pessoas:
                return mesa
        return None

    def ocupar_mesa(self, numero_mesa: int, grupo: GrupoCliente) -> bool:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        if mesa:
            return mesa.ocupar(grupo) 
        return False

    def liberar_mesa(self, numero_mesa: int) -> bool:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        if mesa and mesa.status == StatusMesa.OCUPADA:
            mesa.liberar()
            mesa.limpar() 
            return True
        return False
        
    def designar_garcom(self, mesa: Mesa, garcom: Garcom):
        if mesa and garcom:
            mesa.garcom_responsavel = garcom
            garcom.adicionar_mesa(mesa)