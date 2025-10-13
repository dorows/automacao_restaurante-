from typing import List, Dict

class MesaView:
    def exibir_mesas(self, mesas: List[Dict[str, object]]) -> None:
        print("\n--- STATUS ATUAL DAS MESAS ---")
        if not mesas:
            print("Nenhuma mesa cadastrada no sistema.")
            return
            
        for m in mesas:
            try:
                gar = m.get("garcom") or "-"
                print(f"#{m['id']:>2} | cap:{m['cap']:<2} | {m['status']:<8} | garçom: {gar}")
            except KeyError as e:
                self.erro(f"Mesa com dados incompletos. Chave ausente: {e}")
            except (ValueError, TypeError) as e:
                self.erro(f"Mesa com formato de dado inválido. Detalhe: {e}")
                
        print("-" * 40)

    def exibir_detalhes_mesa(self, mesa: Dict[str, object]) -> None:
        try:
            print(f"\n--- Detalhes da Mesa {mesa['id']} ---")
            gar = mesa.get("garcom") or "-"
            conta = mesa.get("conta_id")
            conta_txt = f"Conta #{conta}" if conta else "Sem conta"
            print(f"cap:{mesa['cap']}  |  {mesa['status']}  |  garçom: {gar}  |  {conta_txt}")
            
        except KeyError as e:
            self.erro(f"Não foi possível exibir detalhes. Dado ausente: {e}")
        except Exception as e:
            self.erro(f"Ocorreu um erro ao exibir os detalhes da mesa: {e}")
            
        print("-" * 40)

    def ok(self, msg: str) -> None: 
        print(f"[OK] {msg}")
        
    def erro(self, msg: str) -> None: 
        print(f"[ERRO] {msg}")