from __future__ import annotations
from typing import List, Dict, Optional, Any


from controllers.mesa_controller import MesaController
from controllers.conta_controller import ContaController
from controllers.fila_de_espera_controller import FilaController
from controllers.funcionario_controller import FuncionarioController
from controllers.cardapio_controller import CardapioController
from controllers.grupo_cliente_controller import ClienteController
from controllers.pedido_controller import PedidoController

from models.status_enums import StatusMesa
from models.mesa import Mesa
from models.grupo_cliente import GrupoCliente
from models.garcom import Garcom
from models.cozinheiro import Cozinheiro
from models.conta import Conta

class RestauranteController:
    def __init__(self,
                 mesa_controller: MesaController,
                 conta_controller: ContaController,
                 fila_controller: FilaController,
                 funcionario_controller: FuncionarioController,
                 cardapio_controller: CardapioController,
                 cliente_controller: ClienteController,
                 pedido_controller: PedidoController) -> None:
        
        self._pedido_controller = pedido_controller
        self._mesa = mesa_controller
        self._conta = conta_controller
        self._fila = fila_controller
        self._func = funcionario_controller
        self._cardapio = cardapio_controller
        self._cliente = cliente_controller

    def get_cardapio_data(self) -> List[Dict[str, object]]:
        return self._cardapio.listar_pratos_para_view()
    

    def auto_alocar_grupos(self, greedy: bool = False) -> List[str]:
        msgs: List[str] = []
        snapshot = self._fila.listar() 
        
        for grupo in snapshot:
            mesa = self._mesa.encontrar_mesa_livre(grupo.numero_pessoas)
            
            if not mesa:
                if not greedy: break
                else: continue
            garcom = None
            try:
                garcom = self._func.encontrar_garcom_disponivel()
                if garcom:
                    try:
                        self._mesa.designar_garcom(mesa, garcom)
                    except ValueError:

                        pass
            except Exception as e_garcom:
                msgs.append(f"[AVISO] Erro ao buscar garçom: {e_garcom}")
                garcom = None 
            try:
                self._mesa.ocupar_mesa(mesa.id_mesa, grupo)
                conta = self._conta.abrir_nova_conta(grupo, mesa)
            except Exception as e_alocar:
                msgs.append(f"[AVISO] Falha ao auto-alocar: {e_alocar}")
                if not greedy: break
                else: continue
            
            self._fila.remover(grupo)
            
            nome_garcom = garcom.nome if garcom else "N/A"
            msgs.append(f"[ALOCADO] G{grupo.id_grupo} -> Mesa {mesa.id_mesa} ({nome_garcom})")

        return msgs

    def receber_clientes(self, qtd: int) -> str:
        grupo = self._cliente.criar_grupo(qtd)
        mesa = self._mesa.encontrar_mesa_livre(grupo.numero_pessoas)
        if not mesa:
            self._fila.adicionar_grupo(grupo)
            return f"[FILA] Grupo {grupo.id_grupo} ({qtd} pessoas) adicionado à fila."
        garcom = None
        try:
            garcom = self._func.encontrar_garcom_disponivel()
            if garcom:
                self._mesa.designar_garcom(mesa, garcom)
        except Exception as e_garcom:
            pass 
        self._mesa.ocupar_mesa(mesa.id_mesa, grupo)
        conta = self._conta.abrir_nova_conta(grupo, mesa)
        return (f"[ALOCADO] Grupo {grupo.id_grupo} ({grupo.numero_pessoas}) -> Mesa {mesa.id_mesa} "
                f"(Garçom: {garcom.nome if garcom else '-'}) | Conta #{conta.id_conta}")


    def finalizar_atendimento(self, mesa_id: int, gorjeta: float = 0.0) -> Dict[str, Any]:
        conta = self._conta.encontrar_conta_por_mesa(mesa_id)
        if not conta:
            raise ValueError(f"Não há conta aberta na mesa {mesa_id}.")

        garcom_responsavel = conta.mesa.garcom_responsavel
        if garcom_responsavel and gorjeta > 0:
            garcom_responsavel.adicionar_gorjeta(gorjeta)
        
        extrato_data = self._pedido_controller.conta_para_view(conta)

        self._conta.fechar_conta(conta)

        self._mesa.liberar_mesa(mesa_id)

        return extrato_data


    def limpar_mesa(self, mesa_id: int) -> str:

        mesa = self._mesa.encontrar_mesa_por_numero(mesa_id)
        
        if mesa and mesa.garcom_responsavel:
            garcom_id = mesa.garcom_responsavel.id_funcionario
            garcom_real = self._func.encontrar_funcionario_por_id(garcom_id)
            
            if garcom_real and isinstance(garcom_real, Garcom):
                mesas_para_manter = [m for m in garcom_real.mesas_atendidas if m.id_mesa != mesa_id]
                
                while len(garcom_real.mesas_atendidas) > 0:
                    m = garcom_real.mesas_atendidas[0]
                    garcom_real.remover_mesa(m)
                
                for m in mesas_para_manter:
                    garcom_real.adicionar_mesa(m)
                
                self._func.atualizar_nome(garcom_id, garcom_real.nome)

        self._mesa.limpar_mesa(mesa_id)
            
        return f"Mesa {mesa_id} limpa e está livre. (Use 'Auto Alocar' para preencher)"


    def listar_equipe(self) -> List[Dict[str, object]]:

        lista_para_view = []
        for f in self._func.listar_funcionarios():
            dados_func = {
                "id": f.id_funcionario,
                "nome": f.nome,
                "papel": "Funcionário", 
                "mesas": 0,
                "salario": f.salario_base,
                "gorjetas": None,
                "pedidos_preparo": 0
            }
            if isinstance(f, Garcom):
                dados_func["papel"] = "Garçom"
                dados_func["mesas"] = len(f.mesas_atendidas)
                dados_func["gorjetas"] = f.gorjetas 
            elif isinstance(f, Cozinheiro):
                dados_func["papel"] = "Cozinheiro"
                dados_func["pedidos_preparo"] = len(f.pedidos_em_preparo)
                                
            lista_para_view.append(dados_func)

        return lista_para_view

    def contratar_garcom(self, nome: str, salario: float) -> Garcom:
        return self._func.contratar_garcom(nome, salario)

    def contratar_cozinheiro(self, nome: str, salario: float) -> Cozinheiro:
        return self._func.contratar_cozinheiro(nome, salario)

    def demitir_funcionario(self, id_func: int):
        return self._func.demitir_funcionario(id_func)

    def adicionar_mesa(self, id_mesa: int, capacidade: int) -> Mesa:
        return self._mesa.cadastrar_mesa(id_mesa, capacidade)

    def ver_prato_mais_pedido(self) -> Dict[str, Any]:
        estatisticas = self._pedido_controller.get_estatisticas_pratos()
        
        if not estatisticas:
            return {"prato_nome": "N/A", "quantidade": 0}

        prato_mais_pedido = max(estatisticas, key=estatisticas.get)
        quantidade = estatisticas[prato_mais_pedido]

        return {
            "prato_nome": prato_mais_pedido.nome,
            "quantidade": quantidade
        }
    
    def confirmar_pedido_na_cozinha(self, mesa_id: int) -> str:
        pedido = self._pedido_controller.confirmar_pedido(mesa_id) 

        cozinheiro = self._func.encontrar_cozinheiro_disponivel()
        
        if cozinheiro:
            cozinheiro.iniciar_preparo_pedido(pedido) 
            msg_coz = f"Assumido por Cozinheiro {cozinheiro.nome}"
        else:
            msg_coz = "Nenhum cozinheiro disponível. Pedido aguardando."
            
        return f"Pedido {pedido.id_pedido} confirmado e enviado. {msg_coz}"
    
    def marcar_pedido_pronto(self, mesa_id: int) -> str:

        conta = self._conta.encontrar_conta_por_mesa(mesa_id)
        if not conta: raise ValueError("Mesa sem conta.")
        
        pedido_alvo = None
        for p in conta.pedidos:
            if p.status.name == "EM_PREPARO": 
                pedido_alvo = p
                break
        
        if not pedido_alvo:
            raise ValueError("Nenhum pedido 'Em Preparo' encontrado nesta mesa.")

        cozinheiro_resp = None
        for func in self._func.listar_funcionarios():
            if isinstance(func, Cozinheiro) and pedido_alvo in func.pedidos_em_preparo:
                cozinheiro_resp = func
                break
        
        if not cozinheiro_resp:
            pedido_alvo.finalizar_preparo()
            msg = "Pedido finalizado."
        else:
            cozinheiro_resp.finalizar_preparo_pedido(pedido_alvo)
            msg = f"Cozinheiro {cozinheiro_resp.nome} finalizou o prato."

        return f"Pedido {pedido_alvo.id_pedido} PRONTO. {msg}"

    def renomear_funcionario(self, id_func: int, novo_nome: str) -> str:
        func_atualizado = self._func.atualizar_nome(id_func, novo_nome)
        return f"Nome atualizado para '{func_atualizado.nome}' (ID {func_atualizado.id_funcionario})."

    def atualizar_salario_funcionario(self, id_func: int, novo_salario: float) -> str:
        func_atualizado = self._func.atualizar_salario(id_func, novo_salario)
        return f"Salário atualizado para R$ {func_atualizado.salario_base:.2f} (ID {func_atualizado.id_funcionario})."
    
    def obter_dados_relatorio_equipe(self) -> List[Dict[str, Any]]:
        return self._func.gerar_relatorio_garcons()
    
    def remover_mesa(self, id_mesa: int) -> str:
        self._mesa.remover_mesa(id_mesa)
        return f"Mesa {id_mesa} removida com sucesso."

    def atualizar_mesa(self, id_mesa: int, nova_capacidade: int) -> str:
        self._mesa.atualizar_mesa(id_mesa, nova_capacidade)
        return f"Capacidade da Mesa {id_mesa} atualizada para {nova_capacidade} lugares."