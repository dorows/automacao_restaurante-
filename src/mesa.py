
from typing import Optional
from status_enums import StatusMesa, StatusGrupoCliente
from grupo_cliente import GrupoCliente
from conta import Conta

class Mesa:    
    _proximo_id_conta = 101 # Variável de classe para gerar IDs de conta únicos

    def __init__(self, id_mesa: int, capacidade: int):
        self.__id_mesa = id_mesa
        self.__capacidade = capacidade
        self.__status = StatusMesa.LIVRE
        self.__grupo_cliente: Optional[GrupoCliente] = None
        self.__conta: Optional[Conta] = None

    @property
    def id_mesa(self) -> int:
        return self.__id_mesa

    @property
    def capacidade(self) -> int:
        return self.__capacidade

    @property
    def status(self) -> StatusMesa:
        return self.__status
    
    @property
    def conta(self) -> Optional[Conta]:
        return self.__conta

    def ocupar(self, grupo: GrupoCliente) -> bool:
        """Tenta alocar um grupo a esta mesa."""
        if self.status != StatusMesa.LIVRE:
            print(f"Erro: Mesa {self.id_mesa} não está livre.")
            return False
        
        if grupo.numero_pessoas > self.capacidade:
            print(f"Erro: Grupo de {grupo.numero_pessoas} pessoas não cabe na mesa {self.id_mesa} (capacidade: {self.capacidade}).")
            return False
        
        print(f"Mesa {self.id_mesa} sendo ocupada pelo {grupo}.")
        self.__status = StatusMesa.OCUPADA
        self.__grupo_cliente = grupo
        self.__grupo_cliente.status = StatusGrupoCliente.SENTADO
        
        self.__conta = Conta(Mesa._proximo_id_conta, self.__grupo_cliente)
        Mesa._proximo_id_conta += 1
        
        return True

    def liberar(self) -> Optional[Conta]:
        if self.status != StatusMesa.OCUPADA:
            print(f"Aviso: Mesa {self.id_mesa} não está ocupada, não pode ser liberada.")
            return None
            
        print(f"Liberando a mesa {self.id_mesa}. Agora precisa ser limpa.")
        self.__status = StatusMesa.SUJA
        
        conta_finalizada = self.__conta
        
        if self.__grupo_cliente:
             self.__grupo_cliente.status = StatusGrupoCliente.SAIU
        self.__grupo_cliente = None
        self.__conta = None
        
        return conta_finalizada

    def limpar(self):
        """Marca uma mesa suja como livre e pronta para uso."""
        if self.status != StatusMesa.SUJA:
            print(f"Aviso: Mesa {self.id_mesa} não precisa ser limpa.")
            return

        print(f"Mesa {self.id_mesa} foi limpa e está livre.")
        self.__status = StatusMesa.LIVRE

    def __str__(self) -> str:
        return f"Mesa {self.id_mesa:02d} ({self.capacidade} lugares) - Status: {self.status.value}"

