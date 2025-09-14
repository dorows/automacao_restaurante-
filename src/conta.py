from grupo_cliente import GrupoCliente
from pedido import Pedido 

class Conta:
    """Gerencia todos os PEDIDOS feitos por um GrupoCliente."""

    def __init__(self, id_conta: int, grupo_cliente: GrupoCliente):
        self.__id_conta = id_conta
        self.__grupo_cliente = grupo_cliente
        self.__pedidos: list[Pedido] = []
        self.__aberta = True

    @property
    def id_conta(self) -> int:
        return self.__id_conta
    
    @property
    def grupo_cliente(self) -> GrupoCliente:
        return self.__grupo_cliente

    def adicionar_pedido(self, pedido: Pedido): 
        
        if self.__aberta:
            self.__pedidos.append(pedido)
            print(f"Pedido {pedido.id_pedido} adicionado à conta {self.id_conta}.")
        else:
            print("Não é possível adicionar pedidos a uma conta fechada.")

    def calcular_total(self) -> float: 
        """Soma o subtotal de todos os pedidos da conta."""
        total = 0.0
        for pedido in self.__pedidos:
            total += pedido.calcular_subtotal_pedido()
        return total

    def fechar_conta(self) -> str: 
        """Fecha a conta e gera um extrato final."""
        self.__aberta = False
        
        extrato = f"--- EXTRATO CONTA {self.id_conta} ---\n"
        extrato += f"Cliente: {self.grupo_cliente}\n"
        extrato += "="*30 + "\n"
        
        if not self.__pedidos:
            extrato += "Nenhum pedido realizado.\n"
        else:
            for pedido in self.__pedidos:
                extrato += f" > Pedido ID: {pedido.id_pedido}\n"
                for item in pedido.itens:
                    extrato += f"   - {str(item)}\n"
        
        extrato += "="*30 + "\n"
        extrato += f"TOTAL GERAL: R$ {self.calcular_total():.2f}\n"
        extrato += "--- CONTA FECHADA ---\n"
        
        return extrato

