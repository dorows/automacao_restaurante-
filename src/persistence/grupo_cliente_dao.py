import pickle
from persistence.abstract_dao import DAO
from models.grupo_cliente import GrupoCliente
from typing import List, Dict, Union, Tuple
import os

GrupoClienteData = Tuple[Dict[int, GrupoCliente], int] 

class GrupoClienteDAO(DAO):
    def __init__(self):
        self.__datasource = 'grupos_clientes.pkl'
        self._grupos: Dict[int, GrupoCliente] = {}
        self._proximo_id = 1 
        
        try:
            self.__load_all()
        except FileNotFoundError:
            self._grupos.clear()
            self._proximo_id = 1
            self.__dump_all()
        except ValueError:
            print(f"[AVISO DAO] Arquivo '{self.__datasource}' vazio ou corrompido. Reiniciando IDs.")
            self._grupos.clear()
            self._proximo_id = 1
            self.__dump_all()

    def __dump_all(self):
        data: GrupoClienteData = (self._grupos, self._proximo_id)
        with open(self.__datasource, 'wb') as f:
            pickle.dump(data, f)

    def __load_all(self):
        if os.path.exists(self.__datasource) and os.path.getsize(self.__datasource) > 0:
            with open(self.__datasource, 'rb') as f:
                self._grupos, self._proximo_id = pickle.load(f)
        else:
            raise FileNotFoundError

    # Sobrescrevemos os métodos públicos para interagir com o cache privado
    
    def add(self, key: int, obj: GrupoCliente):
        self._grupos[key] = obj
        self._proximo_id += 1 
        self.__dump_all()

    def update(self, key: int, obj: GrupoCliente):
        try:
            if self._grupos[key] is not None:
                self._grupos[key] = obj 
                self.__dump_all()
        except KeyError:
            pass 

    def get(self, key: int) -> Union[GrupoCliente, None]:
        try:
            return self._grupos[key]
        except KeyError:
            return None

    def remove(self, key: int):
        try:
            self._grupos.pop(key)
            self.__dump_all() 
        except KeyError:
            pass 

    def get_all(self) -> List[GrupoCliente]:
        return list(self._grupos.values())
    
    def get_proximo_id(self) -> int:
        return self._proximo_id