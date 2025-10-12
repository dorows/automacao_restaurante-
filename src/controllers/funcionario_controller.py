from typing import List, Optional, Tuple
from models.funcionario import Funcionario
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro

class FuncionarioController:

    def __init__(self):
        self._funcionarios: List[Funcionario] = []
        self._proximo_id = 101 
        self._setup_inicial()

    def _gerar_id(self) -> int:
        id_gerado = self._proximo_id
        self._proximo_id += 1
        return id_gerado

    def _setup_inicial(self):
        self.contratar_garcom("Carlos", 1500.0)
        self.contratar_garcom("Beatriz", 1500.0)
        self.contratar_cozinheiro("Ana", 1800.0)

    def contratar_garcom(self, nome: str, salario_base: float) -> Garcom:
        novo_id = self._gerar_id()
        novo_garcom = Garcom(id_funcionario=novo_id, nome=nome, salario_base=salario_base)
        self._funcionarios.append(novo_garcom)
        return novo_garcom

    def contratar_cozinheiro(self, nome: str, salario_base: float) -> Cozinheiro:
        novo_id = self._gerar_id()
        novo_cozinheiro = Cozinheiro(id_funcionario=novo_id, nome=nome, salario_base=salario_base)
        self._funcionarios.append(novo_cozinheiro)
        return novo_cozinheiro

    def listar_funcionarios(self) -> List[Funcionario]:
        return self._funcionarios

    def encontrar_garcom_disponivel(self) -> Optional[Garcom]:
        garcons = [f for f in self._funcionarios if isinstance(f, Garcom)]
        if not garcons:
            return None
        
        garcom_livre = min(garcons, key=lambda g: len(g.mesas_atendidas))

        if len(garcom_livre.mesas_atendidas) < 4:
            return garcom_livre
        return None

    def encontrar_cozinheiro_disponivel(self) -> Optional[Cozinheiro]:
        cozinheiros = [f for f in self._funcionarios if isinstance(f, Cozinheiro)]
        if not cozinheiros:
            return None
        return min(cozinheiros, key=lambda c: len(c.pedidos_em_preparo))
    
    def encontrar_funcionario_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        return next((f for f in self._funcionarios if f.id_funcionario == id_funcionario), None)

    def demitir_funcionario(self, id_funcionario: int) -> Tuple[bool, Optional[Funcionario], Optional[str]]:
        func = self.encontrar_funcionario_por_id(id_funcionario)
        if not func:
            return False, None, "func_nao_encontrado"

        # Regras específicas por função
        if isinstance(func, Cozinheiro):
            # só demite se não tiver trabalho pendente
            if func.pedidos_em_preparo:
                return False, None, "cozinheiro_com_pedidos_em_preparo"

        if isinstance(func, Garcom):
            # desassocia mesas do garçom e limpa o vínculo na mesa
            for mesa in list(func.mesas_atendidas):  # .mesas_atendidas já retorna cópia
                if getattr(mesa, "garcom_responsavel", None) is func:
                    mesa.garcom_responsavel = None
                func.remover_mesa(mesa)

        self._funcionarios.remove(func)
        return True, func, None
