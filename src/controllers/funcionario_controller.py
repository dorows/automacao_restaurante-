from typing import List, Optional, Tuple, Dict
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

    def contratar_garcom(self, nome: str, salario_base: float) -> Tuple[Optional[Garcom], str]:
        try:
            novo_id = self._gerar_id()
            novo_garcom = Garcom(id_funcionario=novo_id, nome=nome, salario_base=salario_base)
            self._funcionarios.append(novo_garcom)
            return novo_garcom, f"[OK] Garçom {nome} (ID: {novo_id}) contratado."
        except (ValueError, TypeError) as e:
            return None, f"[ERRO] Não foi possível contratar o garçom: {e}"

    def contratar_cozinheiro(self, nome: str, salario_base: float) -> Tuple[Optional[Cozinheiro], str]:
        try:
            novo_id = self._gerar_id()
            novo_cozinheiro = Cozinheiro(id_funcionario=novo_id, nome=nome, salario_base=salario_base)
            self._funcionarios.append(novo_cozinheiro)
            return novo_cozinheiro, f"[OK] Cozinheiro {nome} (ID: {novo_id}) contratado."
        except (ValueError, TypeError) as e:
            return None, f"[ERRO] Não foi possível contratar o cozinheiro: {e}"

    def demitir_funcionario(self, id_funcionario: int) -> Tuple[bool, str]:
        try:
            func = self.encontrar_funcionario_por_id(id_funcionario)
            if not func:
                raise ValueError(f"Funcionário com ID {id_funcionario} não encontrado.")

            if isinstance(func, Cozinheiro) and func.pedidos_em_preparo:
                raise ValueError(f"Não é possível demitir o Cozinheiro {func.nome}, pois ele tem pedidos em preparo.")
            
            if isinstance(func, Garcom) and func.mesas_atendidas:
                raise ValueError(f"Não é possível demitir o Garçom {func.nome}, pois ele está atendendo mesas.")

            self._funcionarios.remove(func)
            return True, f"[OK] Funcionário {func.nome} (ID: {func.id_funcionario}) foi demitido."

        except ValueError as e:
            return False, f"[ERRO] {e}"

    def listar_funcionarios(self) -> List[Funcionario]:
        return self._funcionarios

    def encontrar_garcom_disponivel(self) -> Optional[Garcom]:
        garcons = [f for f in self._funcionarios if isinstance(f, Garcom)]
        if not garcons: return None
        
        garcom_livre = min(garcons, key=lambda g: len(g.mesas_atendidas))
        if len(garcom_livre.mesas_atendidas) < 4:
            return garcom_livre
        return None

    def encontrar_cozinheiro_disponivel(self) -> Optional[Cozinheiro]:
        cozinheiros = [f for f in self._funcionarios if isinstance(f, Cozinheiro)]
        if not cozinheiros: return None
        return min(cozinheiros, key=lambda c: len(c.pedidos_em_preparo))
    
    def encontrar_funcionario_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        return next((f for f in self._funcionarios if f.id_funcionario == id_funcionario), None)

    def atualizar_nome(self, id_funcionario: int, novo_nome: str) -> tuple[bool, str]:
        try:
            func = self.encontrar_funcionario_por_id(id_funcionario)
            if not func:
                return False, f"Funcionário com ID {id_funcionario} não encontrado."
            func.nome = novo_nome  # usa o setter do model (valida vazio, normaliza etc.)
            return True, f"[OK] Nome atualizado para '{func.nome}' (ID {func.id_funcionario})."
        except (ValueError, TypeError) as e:
            return False, f"[ERRO] {e}"

    def atualizar_salario(self, id_funcionario: int, novo_salario: float) -> tuple[bool, str]:
        try:
            func = self.encontrar_funcionario_por_id(id_funcionario)
            if not func:
                return False, f"Funcionário com ID {id_funcionario} não encontrado."
            func.salario_base = float(novo_salario)  # usa o setter do model (valida negativo etc.)
            return True, f"[OK] Salário atualizado para R$ {func.salario_base:.2f} (ID {func.id_funcionario})."
        except (ValueError, TypeError) as e:
            return False, f"[ERRO] {e}"
    
    def listar_garcons_para_view(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for f in self._funcionarios:
            if isinstance(f, Garcom):
                out.append({
                    "id": f.id_funcionario,
                    "nome": f.nome,
                    "mesas": len(f.mesas_atendidas),
                })
        return out
