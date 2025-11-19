from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .status_enums import StatusMesa
from .grupo_cliente import GrupoCliente
from .conta import Conta
if TYPE_CHECKING:
    from .garcom import Garcom
from models.excecoes import StatusMesaInvalidoError, GrupoNaoCabeNaMesaError

class Mesa:
    def __init__(self, id_mesa: int, capacidade: int):
        if not isinstance(id_mesa, int) or id_mesa <= 0:
            raise ValueError("O ID da mesa deve ser um número inteiro positivo.")
        if not isinstance(capacidade, int) or capacidade <= 0:
            raise ValueError("A capacidade da mesa deve ser um número inteiro positivo.")

        self._id_mesa: int = id_mesa
        self._capacidade: int = capacidade
        self._status: StatusMesa = StatusMesa.LIVRE
        self._grupo_cliente: Optional[GrupoCliente] = None
        self._conta: Optional[Conta] = None
        self._garcom_responsavel: Optional[Garcom] = None

    @property
    def id_mesa(self) -> int: return self._id_mesa
    @property
    def capacidade(self) -> int: return self._capacidade
    @property
    def status(self) -> StatusMesa: return self._status
    @property
    def garcom_responsavel(self) -> Optional[Garcom]: return self._garcom_responsavel
    @property
    def grupo_cliente(self) -> Optional[GrupoCliente]: return self._grupo_cliente
    @property
    def conta(self) -> Optional[Conta]: return self._conta

    @conta.setter
    def conta(self, nova_conta: Optional[Conta]):
        if not isinstance(nova_conta, (Conta, type(None))):
            raise TypeError("O valor atribuído à conta deve ser um objeto Conta ou None.")
        self._conta = nova_conta

    @garcom_responsavel.setter
    def garcom_responsavel(self, garcom: Optional[Garcom]):
        from .garcom import Garcom 
        if not isinstance(garcom, (Garcom, type(None))):
            raise TypeError("O responsável deve ser um objeto Garcom ou None.")
        self._garcom_responsavel = garcom

    @property
    def capacidade(self) -> int:
        return self._capacidade
    
    @capacidade.setter
    def capacidade(self, nova_capacidade: int):
        if not isinstance(nova_capacidade, int) or nova_capacidade <= 0:
            raise ValueError("A capacidade deve ser um número inteiro positivo.")
        self._capacidade = nova_capacidade
    
    def ocupar(self, grupo: GrupoCliente) -> None:
        from .grupo_cliente import GrupoCliente
        if not isinstance(grupo, GrupoCliente):
            raise TypeError("Apenas um objeto GrupoCliente pode ocupar uma mesa.")
        if self.status != StatusMesa.LIVRE:
            raise StatusMesaInvalidoError(f"Mesa {self.id_mesa} não está livre (status atual: {self.status.value}).")
        if grupo.numero_pessoas > self.capacidade:
            raise GrupoNaoCabeNaMesaError(f"O grupo ({grupo.numero_pessoas} pessoas) não cabe na Mesa {self.id_mesa} (capacidade: {self.capacidade}).")
        
        self._status = StatusMesa.OCUPADA
        self._grupo_cliente = grupo
        grupo.sentar()

    def liberar(self) -> None:
        if self.status != StatusMesa.OCUPADA:
            raise StatusMesaInvalidoError(f"Apenas uma mesa ocupada pode ser liberada (status atual: {self.status.value}).")
        
        if self._grupo_cliente:
            self._grupo_cliente.sair()
        self._status = StatusMesa.SUJA
        self._grupo_cliente = None

    def limpar(self) -> None:
        if self.status != StatusMesa.SUJA:
            raise StatusMesaInvalidoError(f"Apenas uma mesa suja pode ser limpa (status atual: {self.status.value}).")
        
        self._status = StatusMesa.LIVRE
        self.conta = None
        self.garcom_responsavel = None
        
    def __str__(self) -> str:
        garcom = f" (Garçom: {self.garcom_responsavel.nome})" if self.garcom_responsavel else ""
        ocupante = f" (Ocupante: {self._grupo_cliente})" if self._grupo_cliente else ""
        return f"Mesa {self.id_mesa:02d} [{self.capacidade}p] - Status: {self.status.value}{garcom}{ocupante}"