from enum import Enum

class StatusMesa(Enum):
    LIVRE = "Livre"
    OCUPADA = "Ocupada"
    SUJA = "Suja"

class StatusGrupoCliente(Enum):
    ESPERANDO = "Esperando na Fila"
    SENTADO = "Sentado à Mesa"
    SAIU = "Saiu do Restaurante"

class StatusPedido(Enum):
    ABERTO = "Aberto (em anotação)"
    CONFIRMADO = "Confirmado (enviado à cozinha)"
    EM_PREPARO = "Em Preparo"
    PRONTO = "Pronto para Servir"
    ENTREGUE = "Entregue ao Cliente"
    CANCELADO = "Cancelado"