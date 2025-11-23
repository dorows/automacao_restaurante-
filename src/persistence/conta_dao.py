import os
import pickle
from typing import Dict, List, Tuple, Union

from .abstract_dao import DAO
from models.conta import Conta

ContaData = Tuple[Dict[int, Conta], int]


class ContaDAO(DAO):
    def __init__(self):
        self.__datasource = "contas.pkl"
        self._contas: Dict[int, Conta] = {}
        self._proximo_id: int = 1

        try:
            self.__load_all()
        except (FileNotFoundError, EOFError, ValueError, pickle.UnpicklingError):
            self._contas.clear()
            self._proximo_id = 1
            self.__dump_all()

    def __dump_all(self) -> None:
        data: ContaData = (self._contas, self._proximo_id)
        with open(self.__datasource, "wb") as f:
            pickle.dump(data, f)

    def __load_all(self) -> None:
        if not os.path.exists(self.__datasource) or os.path.getsize(self.__datasource) == 0:
            raise FileNotFoundError

        with open(self.__datasource, "rb") as f:
            data = pickle.load(f)

        if isinstance(data, tuple) and len(data) == 2:
            contas, prox_id = data
            self._contas = dict(contas)
            self._proximo_id = int(prox_id)
        elif isinstance(data, dict):
            self._contas = dict(data)
            self._proximo_id = max(self._contas.keys(), default=0) + 1
        else:
            raise ValueError("Formato de arquivo de contas inválido.")


    def add(self, key: int, obj: Conta) -> None:
        self._contas[key] = obj
        self._proximo_id = max(self._proximo_id, key + 1)
        self.__dump_all()

    def update(self, key: int, obj: Conta) -> None:
        if key in self._contas:
            self._contas[key] = obj
            self.__dump_all()

    def get(self, key: int) -> Union[Conta, None]:
        return self._contas.get(key)

    def remove(self, key: int) -> None:
        if key in self._contas:
            self._contas.pop(key)
            self.__dump_all()

    def get_all(self) -> List[Conta]:
        return list(self._contas.values())

    def get_proximo_id(self) -> int:
        return self._proximo_id
