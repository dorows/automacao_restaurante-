from typing import List, Dict, Optional

class FilaView:
    def exibir_fila(self, fila: List[Dict[str, object]]) -> None:
        print("\n--- FILA DE ESPERA ---")
        if not fila:
            print("A fila de espera está vazia.")
            return
            
        for g in fila:
            try:
                print(f"{g['pos']:02d}. {g['nome']} - {g['pessoas']} pessoas")
            
            except KeyError as e:
                self.erro(f"Item na fila com dados incompletos. Chave ausente: {e}")
            
            except (ValueError, TypeError) as e:
                self.erro(f"Item na fila com formato de dado inválido. Detalhe: {e}")

    def exibir_chamada(self, grupo: Optional[Dict[str, object]]) -> None:
        if grupo:
            try:
                print(f"Chamando {grupo['nome']} ({grupo['pessoas']} pessoas)")
            
            except KeyError as e:
                self.erro(f"Não foi possível exibir a chamada. Dado ausente no grupo: {e}")
            
            except TypeError:
                self.erro("Formato de dados do grupo inválido para exibição.")
        else:
            print("Nenhum grupo adequado disponível para a capacidade informada.")

    def ok(self, msg: str) -> None: 
        print(f"[OK] {msg}")
        
    def erro(self, msg: str) -> None: 
        print(f"[ERRO] {msg}")