class Prato:
    def __init__(self, id_prato: int, nome: str, preco: float, descricao: str):
        if not isinstance(id_prato, int) or id_prato <= 0:
            raise ValueError("O ID do prato deve ser um número inteiro positivo.")
        self._id_prato = id_prato 
        
        self.nome = nome
        self.preco = preco
        self.descricao = descricao

    @property
    def id_prato(self) -> int:
        return self._id_prato

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            raise ValueError("O nome do prato não pode ser vazio.")
        self._nome = novo_nome.strip().title() 
    
    @property
    def preco(self) -> float:
        return self._preco
    
    @preco.setter
    def preco(self, novo_preco: float):
        if not isinstance(novo_preco, (int, float)):
            raise TypeError("O preço do prato deve ser um valor numérico.")
        if novo_preco < 0:
            raise ValueError("O preço do prato não pode ser negativo.")
        self._preco = float(novo_preco)

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, nova_descricao: str):
        if not isinstance(nova_descricao, str):
            raise TypeError("A descrição deve ser um texto (string).")
        self._descricao = nova_descricao.strip()
    
    def __str__(self):
        return f"{self.id_prato}. {self.nome} - R$ {self.preco:.2f}"