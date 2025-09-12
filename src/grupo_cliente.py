class GrupoCliente:
    _id_counter = 0
    def __init__(self, quantidade_pessoas: int):
        GrupoCliente._id_counter += 1
        self.id = GrupoCliente._id_counter
        self.quantidade_pessoas = quantidade_pessoas

    def __str__(self) -> str:
        return f"Grupo {self.id} ({self.quantidade_pessoas} pessoas)"