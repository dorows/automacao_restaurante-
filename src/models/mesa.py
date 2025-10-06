# models/mesa.py

from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .status_enums import StatusMesa
from .grupo_cliente import GrupoCliente
from .conta import Conta
if TYPE_CHECKING:
    from .garcom import Garcom

class Mesa:
    def __init__(self, id_mesa: int, capacidade: int):
        self._id_mesa: int = id_mesa
        self._capacidade: int = capacidade
        self._status: StatusMesa = StatusMesa.LIVRE
        self._grupo_cliente: Optional[GrupoCliente] = None
        self._conta: Optional[Conta] = None
        self._garcom_responsavel: Optional[Garcom] = None

    @property
    def id_mesa(self) -> int:
        return self._id_mesa

    @property
    def capacidade(self) -> int:
        return self._capacidade
    
    @property
    def status(self) -> StatusMesa:
        return self._status

    @property
    def garcom_responsavel(self) -> Optional[Garcom]:
        return self._garcom_responsavel

    @property
    def grupo_cliente(self) -> Optional[GrupoCliente]:
        return self._grupo_cliente

    @property
    def conta(self) -> Optional[Conta]:
        return self._conta


    @conta.setter
    def conta(self, nova_conta: Optional[Conta]):

        if isinstance(nova_conta, Conta) or nova_conta is None:
            self._conta = nova_conta
        else:
            raise TypeError("O valor atribuído à conta deve ser um objeto Conta ou None.")

    @garcom_responsavel.setter
    def garcom_responsavel(self, garcom: Optional[Garcom]):
        self._garcom_responsavel = garcom

    def ocupar(self, grupo: GrupoCliente) -> bool:
        if self.status == StatusMesa.LIVRE and grupo.numero_pessoas <= self.capacidade:
            self._status = StatusMesa.OCUPADA
            self._grupo_cliente = grupo
            grupo.sentar()
            return True
        return False

    def liberar(self):
        if self.status == StatusMesa.OCUPADA:
            if self._grupo_cliente:
                self._grupo_cliente.sair()
            self._status = StatusMesa.SUJA
            self._grupo_cliente = None


    def limpar(self):
        if self.status == StatusMesa.SUJA:
            self._status = StatusMesa.LIVRE
            self.conta = None 
            self.garcom_responsavel = None
            print(f"Mesa {self.id_mesa} foi limpa e está livre.")

    def __str__(self) -> str:
        garcom = f" (Garçom: {self.garcom_responsavel.nome})" if self.garcom_responsavel else ""
        ocupante = f" (Ocupante: {self._grupo_cliente})" if self._grupo_cliente else ""
        return f"Mesa {self.id_mesa:02d} [{self.capacidade}p] - Status: {self.status.value}{garcom}{ocupante}"