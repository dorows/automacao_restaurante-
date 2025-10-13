from models.status_enums import StatusGrupoCliente

class GrupoCliente:
    def __init__(self, id_grupo: int, numero_pessoas: int):
        if not isinstance(id_grupo, int) or id_grupo <= 0:
            raise ValueError("O ID do grupo deve ser um número inteiro positivo.")
        if not isinstance(numero_pessoas, int) or numero_pessoas <= 0:
            raise ValueError("O número de pessoas no grupo deve ser um número inteiro positivo.")

        self._id_grupo = id_grupo
        self._numero_pessoas = numero_pessoas
        self._status = StatusGrupoCliente.ESPERANDO

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
        if not isinstance(novo_status, StatusGrupoCliente):
            raise TypeError("O status deve ser um membro válido de StatusGrupoCliente.")
        self._status = novo_status

    def sentar(self) -> None: 
        if self.status != StatusGrupoCliente.ESPERANDO:
            raise ValueError(f"Não é possível sentar o Grupo {self.id_grupo}, pois seu status é '{self.status.value}'.")
        self.status = StatusGrupoCliente.SENTADO

    def sair(self) -> None:
        if self.status == StatusGrupoCliente.SAIU:
            raise ValueError(f"O Grupo {self.id_grupo} já saiu do restaurante.")
        self.status = StatusGrupoCliente.SAIU

    def __str__(self) -> str:
        return f"Grupo {self.id_grupo} ({self.numero_pessoas} pessoas) - Status: {self.status.value}"