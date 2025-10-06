from typing import List
from models.grupo_cliente import GrupoCliente

class ClienteController:
    def __init__(self):
        self._grupos_clientes: List[GrupoCliente] = []
        self._proximo_id_grupo = 1

    def _gerar_id_grupo(self) -> int:
        id_gerado = self._proximo_id_grupo
        self._proximo_id_grupo += 1
        return id_gerado

    def criar_grupo(self, numero_pessoas: int) -> GrupoCliente:

        if numero_pessoas <= 0:
            raise ValueError("Um grupo deve ter ao menos uma pessoa.")
            
        novo_id = self._gerar_id_grupo()
        novo_grupo = GrupoCliente(id_grupo=novo_id, numero_pessoas=numero_pessoas)
        self._grupos_clientes.append(novo_grupo)
        
        print(f"[ClienteController] Novo {novo_grupo} criado.")
        return novo_grupo

    def listar_grupos(self) -> List[GrupoCliente]:
        return self._grupos_clientes