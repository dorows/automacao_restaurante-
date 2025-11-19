from .abstract_dao import DAO
from models.mesa import Mesa

class MesaDAO(DAO):
    def __init__(self):
        super().__init__('mesas.pkl') 
        if not self.get_all():
            self._setup_inicial()

    def _setup_inicial(self):
        mesas_iniciais = [
            (1, 4),
            (2, 2),
            (3, 2),
            (4, 6),
        ]
        
        for id_m, capacidade_m in mesas_iniciais:
            try:
                mesa = Mesa(id_mesa=id_m, capacidade=capacidade_m)
                self.add(id_m, mesa) 
            except (ValueError, TypeError) as e:
                pass

    def encontrar_mesa_por_numero(self, numero_mesa: int) -> Mesa:
        return self.get(numero_mesa)