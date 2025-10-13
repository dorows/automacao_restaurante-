from typing import List, Dict

class PedidoView:
    def exibir_pedido(self, pedido: Dict[str, object]) -> None:
        try:
            print("\n" + "-"*45)
            print(f"Pedido #{pedido['id_pedido']} | Mesa {pedido['mesa_id']} | {pedido['status']}")
            
            linhas = pedido.get("linhas", [])
            if not linhas:
                print("Sem itens.")
            else:
                for ln in linhas:
                    print(f" - {ln}")
            
            print(f"Subtotal: R$ {pedido['subtotal']:.2f}")
            print("-"*45)

        except KeyError as e:
            self.erro(f"Não foi possível exibir o pedido. Dado ausente: {e}")
        except (ValueError, TypeError) as e:
            self.erro(f"Não foi possível exibir o pedido. Formato de dado inválido: {e}")
        except Exception as e:
            self.erro(f"Ocorreu um erro inesperado ao exibir o pedido: {e}")

    def exibir_lista_pedidos(self, pedidos: List[Dict[str, object]]) -> None:
        if not pedidos:
            print("\nNenhum pedido cadastrado.")
            return
        
        for p in pedidos:
            try:
                self.exibir_pedido(p)
            except TypeError:
                self.erro("Formato de item inválido na lista de pedidos.")

    def ok(self, msg: str) -> None: 
        print(f"[OK] {msg}")
        
    def erro(self, msg: str) -> None: 
        print(f"[ERRO] {msg}")

    def exibir_prato_mais_pedido(self, dados: Dict[str, object]) -> None:
        try:
            print("\n--- ESTATÍSTICAS ---")
            print(f"Prato mais pedido: {dados['prato_nome']} (pedido {dados['quantidade']} vezes)")
            print("--------------------")
        except KeyError as e:
            self.erro(f"Não foi possível exibir as estatísticas. Dado ausente: {e}")