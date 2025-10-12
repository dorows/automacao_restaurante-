# FilaView: impressão da fila de espera
from typing import List, Dict, Optional

class FilaView:
    def exibir_fila(self, fila: List[Dict[str, object]]) -> None:
        print("\n--- FILA DE ESPERA ---")
        if not fila:
            print("A fila de espera está vazia.")
            return
        for g in fila:
            print(f"{g['pos']:02d}. {g['nome']} - {g['pessoas']} pessoas")

    def exibir_chamada(self, grupo: Optional[Dict[str, object]]) -> None:
        if grupo:
            print(f"Chamando {grupo['nome']} ({grupo['pessoas']} pessoas)")
        else:
            print("Nenhum grupo adequado disponível para a capacidade informada.")

    def ok(self, msg: str) -> None: print(f"[OK] {msg}")
    def erro(self, msg: str) -> None: print(f"[ERRO] {msg}")
