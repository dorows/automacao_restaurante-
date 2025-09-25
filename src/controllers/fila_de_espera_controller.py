# controllers/fila_controller.py

from typing import Optional

# Importa os modelos que este controlador gerencia
from models.fila_de_espera import FilaDeEspera
from models.grupo_cliente import GrupoCliente

class FilaController:
    def __init__(self):
        self._fila_de_espera = FilaDeEspera()

    def adicionar_grupo(self, grupo: GrupoCliente):
        self._fila_de_espera.adicionar_grupo(grupo)

    def chamar_proximo_grupo(self, capacidade_disponivel: int) -> Optional[GrupoCliente]:
        return self._fila_de_espera.chamar_proximo_grupo(capacidade_disponivel)

    def get_fila(self) -> FilaDeEspera:
        return self._fila_de_espera

    def esta_vazia(self) -> bool:
        return len(self._fila_de_espera) == 0