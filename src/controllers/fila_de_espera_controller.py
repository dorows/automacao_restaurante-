from typing import Optional, Tuple, List, Dict
from models.fila_de_espera import FilaDeEspera 
from models.grupo_cliente import GrupoCliente

from persistence.fila_de_espera_dao import FilaDeEsperaDAO
from controllers.grupo_cliente_controller import ClienteController 

class FilaController:
    def __init__(self, cliente_controller: ClienteController):
        self._dao = FilaDeEsperaDAO()
        self._cliente_controller = cliente_controller
        
        self._fila_de_espera = self._reconstruir_fila() 

    def _reconstruir_fila(self) -> FilaDeEspera:
        fila = FilaDeEspera()
        for id_grupo in self._dao.get_ids_fila():
            grupo = self._cliente_controller.encontrar_grupo_por_id(id_grupo)
            if grupo:
                fila.adicionar_grupo(grupo)
            else:
                self._dao.remover_id(id_grupo) 
        return fila

    @property
    def fila(self) -> FilaDeEspera: 
        return self._fila_de_espera

    def adicionar_grupo(self, grupo: GrupoCliente) -> None:
        self._fila_de_espera.adicionar_grupo(grupo)
        self._dao.adicionar_id(grupo.id_grupo)

    def chamar_proximo_grupo(self, capacidade_disponivel: int) -> Optional[GrupoCliente]:
        
        grupos_persistidos = self._cliente_controller._dao._grupos 
        
        id_proximo = self._dao.chamar_proximo_id(capacidade_disponivel, grupos_persistidos)
        
        if id_proximo > 0:
            for i, grupo in enumerate(self._fila_de_espera.to_list()):
                if grupo.id_grupo == id_proximo:
                    return self._fila_de_espera._fila.pop(i) 
        
        return None

    def remover(self, grupo: GrupoCliente) -> None:
        self._fila_de_espera.remover(grupo)
        self._dao.remover_id(grupo.id_grupo)

    def esta_vazia(self) -> bool:
        return len(self._fila_de_espera) == 0
    
    def listar(self) -> List[GrupoCliente]:
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