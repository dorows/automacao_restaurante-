import pickle
from persistence.abstract_dao import DAO
from typing import List
import os
from models.excecoes import ArquivoCorrompidoError

class FilaDeEsperaDAO(DAO):
    def __init__(self):
        self.__datasource = 'fila_de_espera.pkl'
        self._ids_fila: List[int] = [] 
        
        try:
            self.__load_all()
        except FileNotFoundError:
            self.__dump_all()
        except ValueError:
            self._ids_fila = []
            self.__dump_all()
            
    # Sobrescrevemos os métodos privados de persistência (dump/load)

    def __dump_all(self):
        # Salva apenas a lista de IDs
        with open(self.__datasource, 'wb') as f:
            pickle.dump(self._ids_fila, f)

    def __load_all(self):
        if os.path.exists(self.__datasource) and os.path.getsize(self.__datasource) > 0:
            with open(self.__datasource, 'rb') as f:
                data = pickle.load(f)
                self._ids_fila = data if isinstance(data, list) else []
        else:
            raise FileNotFoundError

    # Métodos de acesso específicos para a lista de IDs

    def adicionar_id(self, id_grupo: int) -> None:
        if id_grupo not in self._ids_fila:
            self._ids_fila.append(id_grupo)
            self.__dump_all()

    def remover_id(self, id_grupo: int) -> None:
        if id_grupo in self._ids_fila:
            self._ids_fila.remove(id_grupo)
            self.__dump_all()

    def get_ids_fila(self) -> List[int]:
        return self._ids_fila.copy()

    def chamar_proximo_id(self, capacidade_disponivel: int, grupos_persistidos: dict) -> int:
        for i, id_grupo in enumerate(self._ids_fila):
            grupo = grupos_persistidos.get(id_grupo)
            if grupo and grupo.numero_pessoas <= capacidade_disponivel:
                return self._ids_fila.pop(i) 
        return 0