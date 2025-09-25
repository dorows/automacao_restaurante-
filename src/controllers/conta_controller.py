# controllers/conta_controller.py

from typing import List, Optional

# Importando os modelos necessários
from models.conta import Conta
from models.grupo_cliente import GrupoCliente
from models.mesa import Mesa

class ContaController:
    """Controlador para gerenciar as operações relacionadas a Contas."""

    def __init__(self):
        self._contas: List[Conta] = []
        self._proximo_id_conta = 1 

    def _gerar_id_conta(self) -> int:
        """Gera um novo ID sequencial para a conta."""
        id_gerado = self._proximo_id_conta
        self._proximo_id_conta += 1
        return id_gerado

    def abrir_nova_conta(self, grupo_cliente: GrupoCliente, mesa: Mesa) -> Conta:

        print('debugando contacontroller.py')
        """
        Cria uma nova conta, garantindo que o argumento 'mesa' seja passado
        para o construtor da classe Conta.
        """
        id_conta = self._gerar_id_conta()
        
        # A linha crucial: garantimos que 'mesa=mesa' está sendo passado.
        nova_conta = Conta(id_conta=id_conta, grupo_cliente=grupo_cliente, mesa=mesa)
        
        self._contas.append(nova_conta)
        
        mesa.conta = nova_conta 
        
        print(f"[ContaController] Conta {id_conta} aberta para o {grupo_cliente} na Mesa {mesa.id_mesa}.")
        return nova_conta

    def fechar_conta(self, conta: Conta) -> bool:
        """Fecha uma conta."""
        if conta and conta.esta_aberta:
            conta.fechar()
            # O print foi movido para cá para consistência
            print(f"[ContaController] Conta {conta.id_conta} foi fechada.")
            return True
        return False

    def encontrar_conta_por_mesa(self, numero_mesa: int) -> Optional[Conta]:
        """Encontra a conta ativa em uma determinada mesa."""
        for conta in self._contas:
            if conta.esta_aberta and conta.mesa.id_mesa == numero_mesa:
                return conta
        return None