from models.status_enums import StatusGrupoCliente
from models.pedido import Pedido


class GrupoCliente:
    def __init__(self, id_grupo: int, numero_pessoas: int):
        self._id_grupo = id_grupo
        self._numero_pessoas = numero_pessoas
        self._status = StatusGrupoCliente.ESPERANDO

    @property
    def id_grupo(self) -> int: return self._id_grupo
    @property
    def numero_pessoas(self) -> int: return self._numero_pessoas

    @property
    def status(self) -> StatusGrupoCliente: return self._status
    @status.setter
    def status(self, novo: StatusGrupoCliente):
        if isinstance(novo, StatusGrupoCliente):
            self._status = novo

    def sentar(self) -> bool:
        if self.status == StatusGrupoCliente.ESPERANDO:
            self.status = StatusGrupoCliente.SENTADO
            return True
        return False  # <- aqui estava "Fals"

    def sair(self) -> bool:
        if self.status != StatusGrupoCliente.SAIU:
            self.status = StatusGrupoCliente.SAIU
            return True
        return False

    def __str__(self) -> str:
        return f"Grupo {self.id_grupo} ({self.numero_pessoas} pessoas) - Status: {self.status.value}"
