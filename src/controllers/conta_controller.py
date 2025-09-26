from typing import List, Optional

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

        print('debugando contacontroller.py')
        id_conta = self._gerar_id_conta()
        nova_conta = Conta(id_conta=id_conta, grupo_cliente=grupo_cliente, mesa=mesa)
        self._contas.append(nova_conta)
        mesa.conta = nova_conta 
        
        print(f"[ContaController] Conta {id_conta} aberta para o {grupo_cliente} na Mesa {mesa.id_mesa}.")
        return nova_conta

    def fechar_conta(self, conta: Conta) -> bool:
        if conta and conta.esta_aberta:
            conta.fechar()
            print(f"[ContaController] Conta {conta.id_conta} foi fechada.")
            return True
        return False

    def encontrar_conta_por_mesa(self, numero_mesa: int) -> Optional[Conta]:
        for conta in self._contas:
            if conta.esta_aberta and conta.mesa.id_mesa == numero_mesa:
                return conta
        return None