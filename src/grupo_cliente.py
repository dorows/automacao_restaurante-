from status_enums import StatusGrupoCliente
from pedido import Pedido
class GrupoCliente:
    def __init__(self, id_grupo: int, numero_pessoas: int):
        self._id_grupo: int = id_grupo
        self._numero_pessoas: int = numero_pessoas
        self._status: StatusGrupoCliente = StatusGrupoCliente.ESPERANDO

    @property
    def id_grupo(self) -> int:
        return self._id_grupo

    @property
    def numero_pessoas(self) -> int:
        return self._numero_pessoas

    @property
    def status(self) -> StatusGrupoCliente:
        return self._status
    
    @status.setter
    def status(self, novo_status: StatusGrupoCliente):
        if isinstance(novo_status, StatusGrupoCliente):
            self._status = novo_status


    def sentar(self):
        
        if self.status == StatusGrupoCliente.ESPERANDO:
            print(f"Grupo {self.id_grupo} está se sentando.")
            self.status = StatusGrupoCliente.SENTADO

    def sair(self):

        print(f"Grupo {self.id_grupo} está saindo do restaurante.")
        self.status = StatusGrupoCliente.SAIU

    def __str__(self) -> str:
        return (f"Grupo {self.id_grupo} ({self.numero_pessoas} pessoas) - "
                f"Status: {self.status.value}")