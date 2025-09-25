from controllers.restaurante_controller import RestauranteController
from views.console_view import ConsoleView

def main():
        """
        Função principal que inicializa o sistema e executa o loop da aplicação.
        """
        # 1. Instancia as camadas principais da arquitetura MVC
        controller = RestauranteController()
        view = ConsoleView()

        view.exibir_mensagem("="*60)
        view.exibir_mensagem("BEM-VINDO AO SISTEMA DE GESTÃO DO RESTAURANTE")
        view.exibir_mensagem("="*60)

        # Exibe o cardápio uma vez no início para o usuário saber as opções
        view.exibir_cardapio(controller.cardapio)

        # 2. Loop principal da aplicação
        while True:
            # a. A View exibe o estado atual do restaurante (busca dados do controller)
            view.exibir_estado_do_restaurante(
                mesas=controller.mesas,
                fila=controller.fila_de_espera
            )
            
            # b. A View captura a entrada do usuário
            acao, args = view.obter_comando()
            
            # c. O Controller processa a ação com base no comando
            try:
                if acao == "chegada":
                    if not args: raise ValueError("Número de pessoas não fornecido.")
                    resultado = controller.receber_clientes(int(args[0]))
                    view.exibir_mensagem(resultado)
                
                elif acao == "pedir":
                    if len(args) < 3: raise ValueError("Argumentos insuficientes.")
                    num_mesa = int(args[0])
                    id_prato = int(args[1])
                    qtd = int(args[2])
                    resultado = controller.realizar_pedido(num_mesa, id_prato, qtd)
                    view.exibir_mensagem(resultado)

                elif acao == "confirmar":
                    if not args: raise ValueError("ID do pedido não fornecido.")
                    resultado = controller.confirmar_e_enviar_pedido_para_cozinha(int(args[0]))
                    view.exibir_mensagem(resultado)

                elif acao == "finalizar":
                    if not args: raise ValueError("Número da mesa não fornecido.")
                    conta_fechada = controller.finalizar_atendimento(int(args[0]))
                    if conta_fechada:
                        # A view é responsável por formatar e exibir o extrato
                        view.exibir_extrato(conta_fechada)
                
                elif acao == "sair":
                    view.exibir_mensagem("Obrigado por usar o sistema. Até logo!")
                    break
                    
                else:
                    view.exibir_mensagem(f"Comando '{acao}' desconhecido. Por favor, tente novamente.")

            except (ValueError, IndexError) as e:
                # Captura erros de conversão (ex: digitar texto em vez de número) ou falta de argumentos
                view.exibir_mensagem(f"Erro no comando: {e}. Verifique os argumentos e tente novamente.")
            except Exception as e:
                # Captura qualquer outro erro inesperado
                view.exibir_mensagem(f"Ocorreu um erro inesperado: {e}")


    # Ponto de entrada padrão para um script Python
if __name__ == "__main__":
    main()