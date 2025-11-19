# persistence/pedido_dao.py

import os
import pickle
from typing import Dict, List, Union

from .abstract_dao import DAO
from models.pedido import Pedido


class PedidoDAO(DAO):
    def __init__(self):
        self.__datasource = "pedidos.pkl"
        self._pedidos: Dict[int, Pedido] = {}

        try:
            self.__load_all()
        except (FileNotFoundError, EOFError, ValueError, pickle.UnpicklingError):
            self._pedidos.clear()
            self.__dump_all()

    def __dump_all(self) -> None:
        with open(self.__datasource, "wb") as f:
            pickle.dump(self._pedidos, f)

    def __load_all(self) -> None:
        if not os.path.exists(self.__datasource) or os.path.getsize(self.__datasource) == 0:
            raise FileNotFoundError

        with open(self.__datasource, "rb") as f:
            data = pickle.load(f)

        if isinstance(data, dict):
            self._pedidos = dict(data)
        else:
            raise ValueError("Formato de arquivo de pedidos inválido.")

    # ------------------ API pública ------------------

    def add(self, key: int, obj: Pedido) -> None:
        self._pedidos[key] = obj
        self.__dump_all()

    def update(self, key: int, obj: Pedido) -> None:
        if key in self._pedidos:
            self._pedidos[key] = obj
            self.__dump_all()

    def get(self, key: int) -> Union[Pedido, None]:
        return self._pedidos.get(key)

    def remove(self, key: int) -> None:
        if key in self._pedidos:
            self._pedidos.pop(key)
            self.__dump_all()

    def get_all(self) -> List[Pedido]:
        return list(self._pedidos.values())
