from __future__ import annotations
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from garcom import Garcom

from status_enums import StatusMesa, StatusGrupoCliente
from grupo_cliente import GrupoCliente
from conta import Conta

class Mesa:    
    _proximo_id_conta = 101
    def __init__(self, id_mesa: int, capacidade: int):
        self.__id_mesa = id_mesa
        self.__capacidade = capacidade
        self.__status = StatusMesa.LIVRE
        self.__grupo_cliente: Optional[GrupoCliente] = None
        self.__conta: Optional[Conta] = None
        self.__garcom_responsavel: Optional[Garcom] = None

    @property
    def id_mesa(self) -> int:
        return self.__id_mesa

    @property
    def capacidade(self) -> int:
        return self.__capacidade
    
    @property
    def conta(self) -> Optional[Conta]:
        return self.__conta

    @property
    def status(self) -> StatusMesa:
        return self.__status

    @property
    def garcom_responsavel(self) -> Optional[Garcom]:
        return self.__garcom_responsavel

    @garcom_responsavel.setter
    def garcom_responsavel(self, garcom: Optional[Garcom]):
        self.__garcom_responsavel = garcom

    def ocupar(self, grupo: GrupoCliente) -> bool:
        if self.status == StatusMesa.LIVRE and grupo.numero_pessoas <= self.capacidade:
            self.__status = StatusMesa.OCUPADA
            self.__grupo_cliente = grupo
            self.__grupo_cliente.status = StatusGrupoCliente.SENTADO
            self.__conta = Conta(Mesa._proximo_id_conta, self.__grupo_cliente)
            Mesa._proximo_id_conta += 1
            print(f"Mesa {self.id_mesa} ocupada por {grupo}.")
            return True
        return False

    def liberar(self):
        if self.status == StatusMesa.OCUPADA and self.conta:
            print(f"\nLiberando Mesa {self.id_mesa}...")
            print(self.conta.fechar_conta())
            self.__status = StatusMesa.SUJA
            if self.__grupo_cliente:
                self.__grupo_cliente.status = StatusGrupoCliente.SAIU
            self.__grupo_cliente = None
            self.__conta = None

    def limpar(self):
        if self.status == StatusMesa.SUJA:
            self.__status = StatusMesa.LIVRE
            print(f"Mesa {self.id_mesa} foi limpa e está livre.")

    def __str__(self) -> str:
        garcom = f" (Garçom: {self.garcom_responsavel.nome})" if self.garcom_responsavel else ""
        ocupante = f" (Ocupante: {self.__grupo_cliente})" if self.__grupo_cliente else ""
        return f"Mesa {self.id_mesa:02d} [{self.capacidade}p] - Status: {self.__status.value}{garcom}{ocupante}"
