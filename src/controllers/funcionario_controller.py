from typing import List, Optional, Dict, Any
from models.funcionario import Funcionario
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro
from persistence.funcionario_dao import FuncionarioDAO

class FuncionarioController:
    def __init__(self):
        self._dao = FuncionarioDAO()

    def _gerar_id(self) -> int:
        return self._dao.get_proximo_id() 

    def contratar_garcom(self, nome: str, salario_base: float) -> Garcom:
        novo_id = self._gerar_id()
        novo_garcom = Garcom(id_funcionario=novo_id, nome=nome, salario_base=salario_base)
        self._dao.add(novo_id, novo_garcom) 
        
        return novo_garcom

    def contratar_cozinheiro(self, nome: str, salario_base: float) -> Cozinheiro:
        novo_id = self._gerar_id()
        novo_cozinheiro = Cozinheiro(id_funcionario=novo_id, nome=nome, salario_base=salario_base)
        self._dao.add(novo_id, novo_cozinheiro)
        
        return novo_cozinheiro

    def demitir_funcionario(self, id_funcionario: int) -> Funcionario:
        func = self.encontrar_funcionario_por_id(id_funcionario)
        if not func:
            raise ValueError(f"Funcionário com ID {id_funcionario} não encontrado.")

        if isinstance(func, Cozinheiro) and func.pedidos_em_preparo:
            raise ValueError(f"Não é possível demitir o Cozinheiro {func.nome}, pois ele tem pedidos em preparo.")
        
        if isinstance(func, Garcom) and func.mesas_atendidas:
            raise ValueError(f"Não é possível demitir o Garçom {func.nome}, pois ele está atendendo mesas.")


        self._dao.remove(id_funcionario)
        return func

    def listar_funcionarios(self) -> List[Funcionario]:
        return self._dao.get_all()

    def encontrar_garcom_disponivel(self) -> Optional[Garcom]:
        garcons = [f for f in self.listar_funcionarios() if isinstance(f, Garcom)]
        if not garcons: return None
        
        garcom_livre = min(garcons, key=lambda g: len(g.mesas_atendidas))
        if len(garcom_livre.mesas_atendidas) < 4:
            return garcom_livre
        return None

    def encontrar_cozinheiro_disponivel(self) -> Optional[Cozinheiro]:
        cozinheiros = [f for f in self.listar_funcionarios() if isinstance(f, Cozinheiro)]
        if not cozinheiros: return None
        return min(cozinheiros, key=lambda c: len(c.pedidos_em_preparo))
    
    def encontrar_funcionario_por_id(self, id_funcionario: int) -> Optional[Funcionario]:
        return self._dao.get(id_funcionario)

    def atualizar_nome(self, id_funcionario: int, novo_nome: str) -> Funcionario:
        func = self.encontrar_funcionario_por_id(id_funcionario)
        if not func:
            raise ValueError(f"Funcionário com ID {id_funcionario} não encontrado.")

        func.nome = novo_nome
        self._dao.update(id_funcionario, func)
        return func

    def atualizar_salario(self, id_funcionario: int, novo_salario: float) -> Funcionario:
        func = self.encontrar_funcionario_por_id(id_funcionario)
        if not func:
            raise ValueError(f"Funcionário com ID {id_funcionario} não encontrado.")
            
        func.salario_base = float(novo_salario)
        self._dao.update(id_funcionario, func) 
        return func

    def listar_garcons_para_view(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for f in self.listar_funcionarios():
            if isinstance(f, Garcom):
                out.append({
                    "id": f.id_funcionario,
                    "nome": f.nome,
                    "mesas": len(f.mesas_atendidas),
                })
        return out
    
    def listar_funcionarios_para_view_gui(self) -> List[List[Any]]:
        dados_formatados = []
        for f in self.listar_funcionarios():
            papel = "Funcionario"
            info_extra = "-"
            gorjetas = "-"
            
            if isinstance(f, Garcom):
                papel = "Garçom"
                info_extra = f"{len(f.mesas_atendidas)} mesas"
                gorjetas = f"R$ {f.gorjetas:.2f}"
            elif isinstance(f, Cozinheiro):
                papel = "Cozinheiro"
                info_extra = f"{len(f.pedidos_em_preparo)} pds em prep."
            
            dados_formatados.append([
                f.id_funcionario,
                f.nome,
                papel,
                f"R$ {f.salario_base:.2f}",
                info_extra,
                gorjetas
            ])

        dados_formatados.sort(key=lambda x: x[0])
        return dados_formatados
    def gerar_relatorio_garcons(self) -> List[Dict[str, Any]]:

        dados = []
        for f in self.listar_funcionarios():
            if isinstance(f, Garcom):
                qtd_mesas = len(f.mesas_atendidas)
                total_gorjetas = f.gorjetas
                media = (total_gorjetas / qtd_mesas) if qtd_mesas > 0 else 0.0
                
                dados.append({
                    "id": f.id_funcionario,
                    "nome": f.nome,
                    "mesas": qtd_mesas,
                    "total_gorjetas": total_gorjetas,
                    "media_por_mesa": media
                })
        dados.sort(key=lambda x: x["total_gorjetas"], reverse=True)
        return dados