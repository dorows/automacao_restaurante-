import pickle
from persistence.abstract_dao import DAO
from models.funcionario import Funcionario
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro
from typing import List, Dict, Union, Tuple
import os 
from typing import cast 
FuncionarioData = Tuple[Dict[int, Funcionario], int] 

class FuncionarioDAO(DAO):
    def __init__(self):
        self.__datasource = 'funcionarios.pkl'
        self._funcionarios: Dict[int, Funcionario] = {}
        self._proximo_id = 101 
        
        try:
            self.__load_all()
        except FileNotFoundError:
            self._setup_inicial()
            self.__dump_all()
        except ValueError:
            self._setup_inicial()
            self.__dump_all()

    def __dump_all(self):
        data: FuncionarioData = (self._funcionarios, self._proximo_id)
        with open(self.__datasource, 'wb') as f:
            pickle.dump(data, f)

    def __load_all(self):
        if os.path.exists(self.__datasource):
            if os.path.getsize(self.__datasource) > 0:
                with open(self.__datasource, 'rb') as f:
                    self._funcionarios, self._proximo_id = pickle.load(f)
            else:
                raise FileNotFoundError
        else:
            raise FileNotFoundError

    # Sobrescrevemos os métodos públicos para interagir com o novo cache privado
    
    def add(self, key: int, obj: Funcionario):
        self._funcionarios[key] = obj
        self._proximo_id += 1 
        self.__dump_all()

    def update(self, key: int, obj: Funcionario):
        try:
            if self._funcionarios[key] is not None:
                self._funcionarios[key] = obj 
                self.__dump_all()
        except KeyError:
            pass 

    def get(self, key: int) -> Union[Funcionario, None]:
        try:
            return self._funcionarios[key]
        except KeyError:
            return None

    def remove(self, key: int):
        try:
            self._funcionarios.pop(key)
            self.__dump_all() 
        except KeyError:
            pass 

    def get_all(self) -> List[Funcionario]:
        return list(self._funcionarios.values())
    
    def get_proximo_id(self) -> int:
        return self._proximo_id

    def _setup_inicial(self):
        self._funcionarios.clear() 
        self._funcionarios[101] = Garcom(id_funcionario=101, nome="Carlos", salario_base=1500.0)
        self._funcionarios[102] = Garcom(id_funcionario=102, nome="Beatriz", salario_base=1500.0)
        self._funcionarios[103] = Cozinheiro(id_funcionario=103, nome="Ana", salario_base=1800.0)
        self._proximo_id = 104