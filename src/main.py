from controllers.restaurante_controller import RestauranteController
from views.console_view import ConsoleView

def main():
    controller = RestauranteController()
    view = ConsoleView()

    view.exibir_mensagem("="*60)
    view.exibir_mensagem("BEM-VINDO AO SISTEMA DE GESTÃO DO RESTAURANTE")
    view.exibir_mensagem("="*60)

    while True:
        view.exibir_estado_do_restaurante(
            mesas=controller.mesas,
            fila=controller.fila_de_espera
        )
        
        acao, args = view.obter_comando()
        
        try:
            if acao == "chegada":
                if not args: raise ValueError("Número de pessoas não fornecido.")
                resultado = controller.receber_clientes(int(args[0]))
                view.exibir_mensagem(resultado)
            
            elif acao == "pedir":
                if len(args) < 3: raise ValueError("Argumentos insuficientes.")
                num_mesa, id_prato, qtd = map(int, args)
                resultado = controller.realizar_pedido(num_mesa, id_prato, qtd)
                view.exibir_mensagem(resultado)

            elif acao == "confirmar":
                if not args: raise ValueError("ID do pedido não fornecido.")
                resultado = controller.confirmar_e_enviar_pedido_para_cozinha(int(args[0]))
                view.exibir_mensagem(resultado)

            elif acao == "pronto":
                if not args: raise ValueError("ID do pedido não fornecido.")
                resultado = controller.finalizar_preparo_pedido(int(args[0]))
                view.exibir_mensagem(resultado)

            elif acao == "finalizar":
                if not args: raise ValueError("Número da mesa não fornecido.")
                conta_fechada = controller.finalizar_atendimento(int(args[0]))
                if conta_fechada:
                    view.exibir_extrato(conta_fechada)
            
            elif acao == "equipe":
                view.exibir_funcionarios(controller.funcionarios)

            elif acao == "cardapio":
                view.exibir_cardapio(controller.cardapio)

            elif acao == "sair":
                view.exibir_mensagem("Obrigado por usar o sistema. Até logo!")
                break
                
            else:
                view.exibir_mensagem(f"Comando '{acao}' desconhecido. Por favor, tente novamente.")

        except (ValueError, IndexError) as e:
            view.exibir_mensagem(f"Erro no comando: {e}. Verifique os argumentos e tente novamente.")
        except Exception as e:
            view.exibir_mensagem(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()