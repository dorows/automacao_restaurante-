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

    def abrir_nova_conta(self, grupo_cliente: GrupoCliente, mesa: Mesa) -> Tuple[Optional[Conta], str]:
        try:
            id_conta = self._gerar_id_conta()
            nova_conta = Conta(id_conta=id_conta, grupo_cliente=grupo_cliente, mesa=mesa)
            mesa.conta = nova_conta
            
            self._contas.append(nova_conta)
            
            mensagem = f"[ContaController] Conta {id_conta} aberta para o {grupo_cliente} na Mesa {mesa.id_mesa}."
            return nova_conta, mensagem

        except (ValueError, TypeError) as e:
            mensagem = f"Não foi possível abrir a conta: {e}"
            return None, mensagem

    def fechar_conta(self, conta: Conta) -> Tuple[bool, str]:
        if not isinstance(conta, Conta):
            return False, "Objeto fornecido não é uma Conta válida."
        
        try:
            conta.fechar()
            mensagem = f"[ContaController] Conta {conta.id_conta} foi fechada."
            return True, mensagem
        except ValueError as e:
            return False, str(e)

    def encontrar_conta_por_mesa(self, numero_mesa: int) -> Optional[Conta]:
        for conta in self._contas:
            if conta.esta_aberta and conta.mesa.id_mesa == numero_mesa:
                return conta
        return None