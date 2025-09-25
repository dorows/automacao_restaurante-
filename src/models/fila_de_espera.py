from typing import List, Optional
from .grupo_cliente import GrupoCliente

class FilaDeEspera:
    def __init__(self):
        self._fila: List[GrupoCliente] = []

    def adicionar_grupo(self, grupo: GrupoCliente):
        if grupo in self._fila:
            return
        
        self._fila.append(grupo)

    def chamar_proximo_grupo(self, capacidade_disponivel: int) -> Optional[GrupoCliente]:
        for i, grupo in enumerate(self._fila):
            if grupo.numero_pessoas <= capacidade_disponivel:
                return self._fila.pop(i)
        return None

    def __len__(self) -> int:
        return len(self._fila)

    def __str__(self) -> str:
        if not self._fila:
            return "A fila de espera está vazia."
        
        titulo = "--- FILA DE ESPERA ---\n"
        itens_fila = "\n".join(
            f"{i+1}. {str(grupo)}" for i, grupo in enumerate(self._fila)
        )
        return titulo + itens_fila