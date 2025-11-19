from typing import List, Optional, Tuple
from models.grupo_cliente import GrupoCliente
from persistence.grupo_cliente_dao import GrupoClienteDAO 

class ClienteController:
    def __init__(self):
        self._dao = GrupoClienteDAO()

    def _gerar_id_grupo(self) -> int:
        return self._dao.get_proximo_id()

    def criar_grupo(self, numero_pessoas: int) -> GrupoCliente:
        novo_id = self._gerar_id_grupo()
        novo_grupo = GrupoCliente(id_grupo=novo_id, numero_pessoas=numero_pessoas)
        self._dao.add(novo_id, novo_grupo) 
        
        return novo_grupo

    def listar_grupos(self) -> List[GrupoCliente]:
        return self._dao.get_all()
    
    def encontrar_grupo_por_id(self, id_grupo: int) -> Optional[GrupoCliente]:
        return self._dao.get(id_grupo)
    
    def atualizar_grupo(self, grupo: GrupoCliente) -> None:
        self._dao.update(grupo.id_grupo, grupo)
        
    def remover_grupo(self, id_grupo: int) -> None:
        self._dao.remove(id_grupo)