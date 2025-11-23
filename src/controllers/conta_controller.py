from typing import List, Optional

from models.conta import Conta
from models.grupo_cliente import GrupoCliente
from models.mesa import Mesa
from persistence.conta_dao import ContaDAO


class ContaController:
    def __init__(self):
        self._dao = ContaDAO()

    def _gerar_id_conta(self) -> int:
        return self._dao.get_proximo_id()

    def abrir_nova_conta(self, grupo_cliente: GrupoCliente, mesa: Mesa) -> Conta:
        if not isinstance(grupo_cliente, GrupoCliente):
            raise TypeError("grupo_cliente deve ser um GrupoCliente válido.")
        if not isinstance(mesa, Mesa):
            raise TypeError("mesa deve ser uma Mesa válida.")

        novo_id = self._gerar_id_conta()
        nova_conta = Conta(id_conta=novo_id, grupo_cliente=grupo_cliente, mesa=mesa)

        try:
            mesa.conta = nova_conta
        except AttributeError:
            pass

        self._dao.add(novo_id, nova_conta)
        return nova_conta

    def fechar_conta(self, conta: Conta) -> None:
        if not isinstance(conta, Conta):
            raise TypeError("Objeto fornecido não é uma Conta válida.")
        conta.fechar()
        self._dao.update(conta.id_conta, conta)

    def atualizar_conta(self, conta: Conta) -> None:
        if not isinstance(conta, Conta):
            raise TypeError("Objeto fornecido não é uma Conta válida.")
        self._dao.update(conta.id_conta, conta)

    def encontrar_conta_por_mesa(self, numero_mesa: int) -> Optional[Conta]:
        for conta in self._dao.get_all():
            if conta.esta_aberta and conta.mesa.id_mesa == numero_mesa:
                return conta
        return None

    def listar_contas(self) -> List[Conta]:
        return self._dao.get_all()
