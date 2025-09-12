
from __future__ import annotations
from typing import Optional
from status_enums import StatusMesa
from grupo_cliente import GrupoCliente

class Mesa:
    
    def __init__(self, numero: int, capacidade: int):
        self.numero: int = numero
        self.capacidade: int = capacidade
        self.status: StatusMesa = StatusMesa.LIVRE
        self.grupo_cliente: Optional[GrupoCliente] = None

    def __str__(self) -> str:
        grupo_info = f"Ocupada por: {self.grupo_cliente}" if self.grupo_cliente else "Ninguém"
        return (f"Mesa {self.numero} (Cap: {self.capacidade}) - "
                f"Status: {self.status.value} - {grupo_info}")

    def ocupar(self, grupo: GrupoCliente):
        if self.status == StatusMesa.LIVRE and grupo.quantidade_pessoas <= self.capacidade:
            self.status = StatusMesa.OCUPADA
            self.grupo_cliente = grupo
            return True
        return False

    def liberar(self):
        if self.status == StatusMesa.OCUPADA:
            self.status = StatusMesa.SUJA
            self.grupo_cliente = None
            return True
        return False

    def limpar(self):
        if self.status == StatusMesa.SUJA:
            self.status = StatusMesa.LIVRE
            return True
        return False