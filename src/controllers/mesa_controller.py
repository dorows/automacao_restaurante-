from typing import List, Optional, Dict
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.status_enums import StatusMesa
from persistence.mesa_dao import MesaDAO 

class MesaController:
    def __init__(self):
        self._mesa_dao = MesaDAO()

    def listar_mesas(self) -> List[Mesa]:
        return list(self._mesa_dao.get_all())

    def encontrar_mesa_por_numero(self, numero_mesa: int) -> Optional[Mesa]:
        return self._mesa_dao.get(numero_mesa)

    def encontrar_mesa_livre(self, qtd_pessoas: int) -> Optional[Mesa]:
        melhor: Optional[Mesa] = None
        for m in self.listar_mesas(): 
            if m.status == StatusMesa.LIVRE and m.capacidade >= qtd_pessoas:
                if (melhor is None or
                    m.capacidade < melhor.capacidade or
                    (m.capacidade == melhor.capacidade and m.id_mesa < melhor.id_mesa)):
                    melhor = m
        return melhor

    def ocupar_mesa(self, numero_mesa: int, grupo: GrupoCliente) -> Mesa:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        if not mesa:
            raise ValueError(f"Mesa com número {numero_mesa} não encontrada.")
        
        mesa.ocupar(grupo)
        
        self._mesa_dao.update(numero_mesa, mesa) 
        
        return mesa

    def liberar_mesa(self, numero_mesa: int) -> Mesa:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        if not mesa:
            raise ValueError(f"Mesa com número {numero_mesa} não encontrada.")
        
        mesa.liberar() 
        self._mesa_dao.update(numero_mesa, mesa) 
        return mesa

    def limpar_mesa(self, numero_mesa: int) -> Mesa:
        mesa = self.encontrar_mesa_por_numero(numero_mesa)
        if not mesa:
            raise ValueError(f"Mesa com número {numero_mesa} não encontrada.")
        
        mesa.limpar() 
        self._mesa_dao.update(numero_mesa, mesa) 
        return mesa

    def designar_garcom(self, mesa: Mesa, garcom: Garcom) -> None:
        if not isinstance(mesa, Mesa) or not isinstance(garcom, Garcom):
            raise TypeError("Argumentos inválidos para designar garçom.")

        antigo_garcom = mesa.garcom_responsavel
        
        if antigo_garcom is not garcom:
            if antigo_garcom:
                antigo_garcom.remover_mesa(mesa) 
            
            garcom.adicionar_mesa(mesa)
            mesa.garcom_responsavel = garcom
            
        self._mesa_dao.update(mesa.id_mesa, mesa)

    def cadastrar_mesa(self, id_mesa: int, capacidade: int) -> Mesa:
        if self._mesa_dao.get(id_mesa):
            raise ValueError(f"Já existe uma mesa com o ID {id_mesa}.")

        nova = Mesa(id_mesa=id_mesa, capacidade=capacidade)
        self._mesa_dao.add(id_mesa, nova)
        return nova

    def mesa_para_dict(self, mesa: Mesa) -> Dict[str, object]:
        garcom = getattr(mesa, "garcom_responsavel", None)
        return {
            "id": mesa.id_mesa,
            "cap": mesa.capacidade,
            "status": mesa.status.name if hasattr(mesa.status, "name") else str(mesa.status),
            "garcom": garcom.nome if garcom else None,
        }

    def listar_mesas_para_view(self) -> List[Dict[str, object]]:
        return [self.mesa_para_dict(m) for m in self.listar_mesas()]
    
    def remover_mesa(self, id_mesa: int) -> None:
        mesa = self.encontrar_mesa_por_numero(id_mesa)
        if not mesa:
            raise ValueError(f"Mesa {id_mesa} não encontrada.")
        
        if mesa.status != StatusMesa.LIVRE:
            raise ValueError(f"Não é possível remover a Mesa {id_mesa} pois ela está ocupada ou suja.")
            
        self._mesa_dao.remove(id_mesa)

    def atualizar_mesa(self, id_mesa: int, nova_capacidade: int) -> None:
        mesa = self.encontrar_mesa_por_numero(id_mesa)
        if not mesa:
            raise ValueError(f"Mesa {id_mesa} não encontrada.")
        mesa.capacidade = nova_capacidade 
        self._mesa_dao.update(id_mesa, mesa)
            
        if nova_capacidade <= 0:
            raise ValueError("A capacidade deve ser positiva.")
        self._mesa_dao.update(id_mesa, mesa)