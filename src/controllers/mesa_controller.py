from typing import List, Optional, Tuple, Dict
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.status_enums import StatusMesa

class MesaController:
    def __init__(self):
        self._mesas: List[Mesa] = []
        self._setup_inicial()

    def _setup_inicial(self):
        self._mesas.extend([
            Mesa(id_mesa=1, capacidade=4),
            Mesa(id_mesa=2, capacidade=2),
            Mesa(id_mesa=3, capacidade=2),
            Mesa(id_mesa=4, capacidade=6),
        ])

    def listar_mesas(self) -> List[Mesa]:
        return self._mesas

    def encontrar_mesa_por_numero(self, numero_mesa: int) -> Optional[Mesa]:
        return next((m for m in self._mesas if m.id_mesa == numero_mesa), None)

    def encontrar_mesa_livre(self, qtd_pessoas: int) -> Optional[Mesa]:
        melhor: Optional[Mesa] = None
        for m in self._mesas:
            if m.status == StatusMesa.LIVRE and m.capacidade >= qtd_pessoas:
                if (melhor is None or
                    m.capacidade < melhor.capacidade or
                    (m.capacidade == melhor.capacidade and m.id_mesa < melhor.id_mesa)):
                    melhor = m
        return melhor

    def ocupar_mesa(self, numero_mesa: int, grupo: GrupoCliente) -> Tuple[bool, str]:
        try:
            mesa = self.encontrar_mesa_por_numero(numero_mesa)
            if not mesa:
                raise ValueError(f"Mesa com número {numero_mesa} não encontrada.")
            
            mesa.ocupar(grupo)
            return True, f"Mesa {numero_mesa} ocupada com sucesso."
        except (ValueError, TypeError) as e:
            return False, str(e)

    def liberar_mesa(self, numero_mesa: int) -> Tuple[bool, str]:
        try:
            mesa = self.encontrar_mesa_por_numero(numero_mesa)
            if not mesa:
                raise ValueError(f"Mesa com número {numero_mesa} não encontrada.")
            mesa.liberar() 
            return True, f"Mesa {numero_mesa} liberada e aguardando limpeza."
        except ValueError as e:
            return False, str(e)
    def limpar_mesa(self, numero_mesa: int) -> Tuple[bool, str]:

        try:
            mesa = self.encontrar_mesa_por_numero(numero_mesa)
            if not mesa:
                raise ValueError(f"Mesa com número {numero_mesa} não encontrada.")
            mesa.limpar() 
            return True, f"Mesa {numero_mesa} foi limpa e está livre."
        except ValueError as e:
            return False, str(e)


    def designar_garcom(self, mesa: Mesa, garcom: Garcom) -> Tuple[bool, str]:
        try:
            if not isinstance(mesa, Mesa) or not isinstance(garcom, Garcom):
                raise TypeError("Argumentos inválidos para designar garçom.")

            antigo_garcom = mesa.garcom_responsavel
            if antigo_garcom is not garcom:
                if antigo_garcom:
                    antigo_garcom.remover_mesa(mesa)
                garcom.adicionar_mesa(mesa)
                mesa.garcom_responsavel = garcom
            
            return True, f"Garçom {garcom.nome} designado para a Mesa {mesa.id_mesa}."
        except (ValueError, TypeError) as e:
            return False, str(e)

    def cadastrar_mesa(self, id_mesa: int, capacidade: int) -> Tuple[Optional[Mesa], str]:
        try:
            if self.encontrar_mesa_por_numero(id_mesa):
                raise ValueError(f"Já existe uma mesa com o ID {id_mesa}.")
            nova = Mesa(id_mesa=id_mesa, capacidade=capacidade)
            self._mesas.append(nova)
            return nova, f"Mesa {id_mesa} cadastrada com sucesso."
        except (ValueError, TypeError) as e:
            return None, str(e)

    def mesa_para_dict(self, mesa: Mesa) -> Dict[str, object]:
        garcom = getattr(mesa, "garcom_responsavel", None)
        return {
            "id": mesa.id_mesa,
            "cap": mesa.capacidade,
            "status": mesa.status.name if hasattr(mesa.status, "name") else str(mesa.status),
            "garcom": garcom.nome if garcom else None,
        }

    def listar_mesas_para_view(self) -> List[Dict[str, object]]:
        return [self.mesa_para_dict(m) for m in self._mesas]
