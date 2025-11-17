from typing import Optional, Tuple, List, Dict
from models.fila_de_espera import FilaDeEspera
from models.grupo_cliente import GrupoCliente

class FilaController:
    def __init__(self):
        self._fila_de_espera = FilaDeEspera()

    @property
    def fila(self) -> FilaDeEspera: 
        return self._fila_de_espera

    def adicionar_grupo(self, grupo: GrupoCliente) -> Tuple[bool, str]:
        try:
            self._fila_de_espera.adicionar_grupo(grupo)
            return True, f"Grupo {grupo.id_grupo} adicionado à fila."
        except (ValueError, TypeError) as e:
            return False, str(e)

    def chamar_proximo_grupo(self, capacidade_disponivel: int) -> Optional[GrupoCliente]:
        try:
            return self._fila_de_espera.chamar_proximo_grupo(capacidade_disponivel)
        except ValueError as e:
            print(f"[ERRO no FilaController] {e}")
            return None

    def remover(self, grupo: GrupoCliente) -> Tuple[bool, str]:
        try:
            self._fila_de_espera.remover(grupo)
            return True, f"Grupo {grupo.id_grupo} removido da fila."
        except (ValueError, TypeError) as e:
            return False, str(e)

    def esta_vazia(self) -> bool:
        return len(self._fila_de_espera) == 0
    
    def listar(self):
        return self._fila_de_espera.to_list()
    
    def listar_para_view(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for i, g in enumerate(self.listar(), start=1):
            out.append({
                "pos": i,
                "nome": f"Grupo {g.id_grupo}",
                "pessoas": g.numero_pessoas,
            })
        return out
