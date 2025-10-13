from typing import List, Optional, Tuple
from models.grupo_cliente import GrupoCliente

class ClienteController:
    def __init__(self):
        self._grupos_clientes: List[GrupoCliente] = []
        self._proximo_id_grupo = 1

    def _gerar_id_grupo(self) -> int:
        id_gerado = self._proximo_id_grupo
        self._proximo_id_grupo += 1
        return id_gerado

    def criar_grupo(self, numero_pessoas: int) -> Tuple[Optional[GrupoCliente], str]:

        try:
            novo_id = self._gerar_id_grupo()
            novo_grupo = GrupoCliente(id_grupo=novo_id, numero_pessoas=numero_pessoas)
            self._grupos_clientes.append(novo_grupo)
            return novo_grupo, f"[OK] Grupo {novo_grupo.id_grupo} criado com {numero_pessoas} pessoas."

        except (ValueError, TypeError) as e:
            return None, f"[ERRO] Não foi possível criar o grupo: {e}"

    def listar_grupos(self) -> List[GrupoCliente]:
        return self._grupos_clientes