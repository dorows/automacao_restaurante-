class Prato:
    def __init__(self, id_prato: int, nome: str, preco: float, descricao: str):
        self.__id_prato = id_prato
        self.__nome = nome
        self.__preco = preco
        self.__descricao = descricao

    @property
    def id_prato(self) -> int:
        return self.__id_prato

    @property
    def nome(self) -> str:
        return self.__nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        self.__nome = novo_nome.strip()
    
    @property
    def preco(self) -> float:
        return self.__preco
    
    @preco.setter
    def preco(self, novo_preco: float):
        self.__preco = float(novo_preco)

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, nova_descricao: str):
        self.__descricao = nova_descricao
    
    def __str__(self):
        return f"{self.id_prato}. {self.nome} - R$ {self.preco:.2f}"
    