from typing import List, Optional, Iterator
from .grupo_cliente import GrupoCliente

class FilaDeEspera:
    def __init__(self):
        self._fila: List[GrupoCliente] = []

    def adicionar_grupo(self, grupo: GrupoCliente):
        if grupo not in self._fila:
            self._fila.append(grupo)

    def chamar_proximo_grupo(self, capacidade_disponivel: int) -> Optional[GrupoCliente]:
        for i, grupo in enumerate(self._fila):
            if grupo.numero_pessoas <= capacidade_disponivel:
                return self._fila.pop(i)
        return None

    def __len__(self) -> int:
        return len(self._fila)

    def __iter__(self) -> Iterator[GrupoCliente]:
        return iter(self._fila)

    def to_list(self) -> List[GrupoCliente]:
        return self._fila.copy()

    def __str__(self) -> str:
        # para debug
        return f"FilaDeEspera(len={len(self)})"
