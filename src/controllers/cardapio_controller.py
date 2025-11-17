from typing import Optional, Tuple, List, Dict
from models.cardapio import Cardapio
from models.prato import Prato

class CardapioController:
    def __init__(self):
        self._cardapio = Cardapio()
        self._setup_inicial()

    @property
    def cardapio(self) -> Cardapio:
        return self._cardapio

    def _setup_inicial(self):
        pratos_iniciais = [
            (1,  "Spaghetti alla Carbonara", 55.50, "Massa com ovos, queijo pecorino e pancetta."),
            (2,  "Lasanha Bolonhesa",        62.00, "Massa em camadas com molho à bolonhesa e queijo."),
            (3,  "Risoto de Funghi",         58.90, "Arroz arbóreo com cogumelos e parmesão."),
            (4,  "Filé à Parmegiana",        69.00, "Filé empanado, molho de tomate e queijo gratinado."),
            (5,  "Frango Grelhado",          49.00, "Peito de frango com legumes salteados."),
            (6,  "Pizza Margherita (8f)",    59.00, "Mussarela, tomate e manjericão."),
            (7,  "Salada Caesar",            32.00, "Alface romana, croutons e molho clássico."),

            (101, "Suco de Laranja",         12.00, "500ml, natural."),
            (102, "Água com Gás",             6.00, "300ml."),
            (103, "Refrigerante Lata",        8.00, "350ml, diversos sabores."),
            (104, "Cerveja Pilsen 600ml",    15.00, "Long neck ou garrafa 600ml."),
            (105, "Café Espresso",            6.50, "Curto, intenso."),
            (106, "Chá Gelado",               9.00, "Limão ou pêssego."),

            (201, "Pudim de Leite",          14.00, "Calda de caramelo."),
            (202, "Tiramisù",                18.00, "Clássico italiano."),
            (203, "Sorvete (2 bolas)",       12.00, "Sabores do dia."),
        ]

        for id_p, nome_p, preco_p, desc_p in pratos_iniciais:
            try:
                prato = Prato(id_prato=id_p, nome=nome_p, preco=preco_p, descricao=desc_p)
                self._cardapio.adicionar_prato(prato)
            except (ValueError, TypeError) as e:
                print(f"[AVISO DE INICIALIZAÇÃO] Não foi possível adicionar o prato '{nome_p}': {e}")

    def adicionar_novo_prato(self, id_prato: int, nome: str, preco: float, descricao: str) -> Tuple[bool, str]:
        try:
            novo_prato = Prato(id_prato, nome, preco, descricao)
            self._cardapio.adicionar_prato(novo_prato)
            return True, f"Prato '{nome}' adicionado com sucesso."

        except (ValueError, TypeError) as e:
            return False, str(e)

    def buscar_prato_por_id(self, id_prato: int) -> Optional[Prato]:
        return self._cardapio.buscar_prato_por_id(id_prato)

    def listar_pratos_para_view(self) -> List[Dict[str, object]]:
        out: List[Dict[str, object]] = []
        for p in self._cardapio.pratos:
            out.append({
                "id": p.id_prato,
                "nome": p.nome,
                "preco": p.preco,
            })
        return out
