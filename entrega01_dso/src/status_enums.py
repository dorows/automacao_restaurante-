from enum import Enum

class StatusMesa(Enum):
    LIVRE = "Livre"
    OCUPADA = "Ocupada"
    SUJA = "Suja"

class StatusGrupoCliente(Enum):
    ESPERANDO = "Esperando na Fila"
    SENTADO = "Sentado à Mesa"
    SAIU = "Saiu do Restaurante"