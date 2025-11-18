# controllers/conta_controller.py
from typing import List, Optional, Tuple
from models.conta import Conta
from models.grupo_cliente import GrupoCliente
from models.mesa import Mesa

class ContaController:
    def __init__(self):
        self._contas: List[Conta] = []
        self._proximo_id_conta = 1 

    def _gerar_id_conta(self) -> int:
        id_gerado = self._proximo_id_conta
        self._proximo_id_conta += 1
        return id_gerado


    def abrir_nova_conta(self, grupo_cliente: GrupoCliente, mesa: Mesa) -> Conta:
        id_conta = self._gerar_id_conta()
        nova_conta = Conta(id_conta=id_conta, grupo_cliente=grupo_cliente, mesa=mesa)
        mesa.conta = nova_conta 
        self._contas.append(nova_conta)
        
        return nova_conta

    def fechar_conta(self, conta: Conta) -> None:
        if not isinstance(conta, Conta):
            raise TypeError("Objeto fornecido não é uma Conta válida.")
        conta.fechar()


    def encontrar_conta_por_mesa(self, numero_mesa: int) -> Optional[Conta]:
        for conta in self._contas:
            if conta.esta_aberta and conta.mesa.id_mesa == numero_mesa:
                return conta
        return None