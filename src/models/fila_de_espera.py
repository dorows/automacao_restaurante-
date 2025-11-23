from typing import List, Optional, Iterator
from .grupo_cliente import GrupoCliente 

class FilaDeEspera:
    def __init__(self):
        self._fila: List[GrupoCliente] = []

    def adicionar_grupo(self, grupo: GrupoCliente) -> None: 
        from .grupo_cliente import GrupoCliente
        if not isinstance(grupo, GrupoCliente):
            raise TypeError("Apenas objetos da classe GrupoCliente podem ser adicionados à fila.")
        if grupo in self._fila:
            raise ValueError(f"O Grupo {grupo.id_grupo} já se encontra na fila de espera.")
            
        self._fila.append(grupo)

    def remover(self, grupo: GrupoCliente) -> None:
        if not isinstance(grupo, GrupoCliente):
            raise TypeError("Apenas um objeto GrupoCliente pode ser removido da fila.")
        if grupo in self._fila:
            self._fila.remove(grupo)
        else:
            raise ValueError(f"O Grupo {grupo.id_grupo} não foi encontrado na fila de espera.")

    def chamar_proximo_grupo(self, capacidade_disponivel: int) -> Optional[GrupoCliente]:

        if not isinstance(capacidade_disponivel, int) or capacidade_disponivel <= 0:
            raise ValueError("A capacidade disponível deve ser um número inteiro positivo.")
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
        if not self._fila:
            return "Fila vazia"
        return " -> ".join(f"G{g.id_grupo}({g.numero_pessoas})" for g in self._fila)