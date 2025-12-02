import cadastro
from consultarhorarios import consultar_horarios
import consultarassentos
import relatorios
from datetime import datetime, timedelta
import lerarquivo 
import reservarassento as rauto 

if __name__ == "__main__": 

    linhas = {} #Inicializa o dicionário de linhas

    if not hasattr(relatorios, 'historico_vendas'): #Garantir que o histórico de vendas exista
        relatorios.historico_vendas = [] #Lista para armazenar o histórico de vendas

    while True:
        print("\n\t\t SISTEMA DE TRANSPORTE DE PASSAGEIROS \n") #Menu principal, com todas as opções disponíveis

        print("1 - Cadastro de Linhas")
        print("    1.1 - Inserir Linha")
        print("    1.2 - Remover Linha")
        print("    1.3 - Alterar Linha")
        print("2 - Listar Linhas Cadastradas")
        print("3 - Consultar horários disponíveis por cidade")
        print("4 - Consultar assentos disponíveis")
        print("5 - Reserva automatica de assentos")
        print("6 - Relatórios")
        print("    6.1 - Total arrecadado no mês por linha")
        print("    6.2 - Ocupação média por dia da semana")
        print("    6.3 - Relatório de erros")
        print("    6.4 - Gerar arquivo de reservas inválidas")
        print("7 - Ler reservas de arquivo texto")
        print("0 - Sair")
        print("\n\n")

        try:
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                print("\n\t CADASTRO DE LINHAS \n")
                print("1 - Inserir Linha")
                print("2 - Remover Linha")
                print("3 - Alterar Linha\n")

                try:
                    opcao2 = input("Escolha: ").strip()

                    if opcao2 == "1":
                        cadastro.inserirlinha(linhas) #Chama a função para inserir uma nova linha

                    elif opcao2 == "2":
                        cadastro.removerlinha(linhas) #Chama a função para remover uma linha existente

                    elif opcao2 == "3":
                        cadastro.alterarlinha(linhas) #Chama a função para alterar os dados de uma linha existente

                    else:
                        print("Opção inválida!")

                except Exception as e:
                    print("Erro no submenu de cadastro!")
                    print(e)

            elif opcao == "2":
                cadastro.imprimirlinhas(linhas) #Chama a função para imprimir todas as linhas cadastradas

            elif opcao == "3":
                consultar_horarios(linhas) #Chama a função para consultar horários por cidade de destino

            elif opcao == "4":
                consultarassentos.consultar_assentos(linhas) #Chama a função para consultar assentos disponíveis

            elif opcao == "5":

                try:
                    print("\n\t RESERVA AUTOMÁTICA\n")

                    if not linhas:
                        print("Nenhuma linha cadastrada!\n")
                        continue

                    cadastro.imprimirlinhas(linhas) #Mostra todas as linhas cadastradas com os ID's, para o usuário escolher qual reservar

                    entrada = input("Digite o ID da linha (ex: L1 ou 1) ou 's' para sair: ").strip() #Solicita o ID da linha ao usuário
                    if entrada.lower() == 's':
                        continue

                    ent = entrada.upper() #Normaliza a entrada do usuário para facilitar a verificação
                    if ent.startswith("L") and ent[1:].isdigit(): #Verifica se o formato é 'L' seguido de números
                        linha_id = "L" + str(int(ent[1:])) #Extrai o número e forma o ID correto

                    elif ent.isdigit(): #Verifica se a entrada é apenas números
                        linha_id = "L" + str(int(ent)) #Forma o ID adicionando 'L' na frente

                    else:
                        print("ID inválido. Use 'L1' ou '1'.\n")
                        relatorios.registrar_erro("ID de linha inválido", "-", "-", "-") #Registra o erro no relatório
                        continue

                    if linha_id not in linhas:
                        print("Linha não encontrada!\n")
                        relatorios.registrar_erro("Linha não encontrada", linha_id, "-", "-") #Registra o erro no relatório
                        continue

                    dados = linhas[linha_id] #Obtém os dados da linha selecionada
                    horario_linha = dados[2] #Obtém o horário da linha

                    data_str = input("Digite a data da viagem (dd/mm/aaaa): ").strip()

                    try:
                        data_usuario = datetime.strptime(data_str, "%d/%m/%Y").date() #Tenta converter a string da data para um objeto date
                    except:
                        print("Data inválida! Use dd/mm/aaaa.\n")
                        relatorios.registrar_erro("Data inválida", linha_id, data_str, "-") #Em caso de erro, registra o erro no relatório
                        continue

                    hoje = datetime.today().date() #Obtém a data atual para comparações

                    if data_usuario < hoje: #Compara a data da viagem com a data atual
                        print("\nNão é permitido reservar para uma data que já passou!\n")
                        relatorios.registrar_erro("Data já passou", linha_id, data_str, "-") #Caso a data já tenha passado, registra o erro
                        continue

                    if data_usuario > hoje + timedelta(days=30): #Verifica se a data está dentro do limite de 30 dias
                        print("\nA data deve estar dentro de 30 dias.\n")
                        relatorios.registrar_erro("Data acima de 30 dias", linha_id, data_str, "-") #Registra o erro se a data exceder o limite
                        continue

                    agora = datetime.now() #Obtém a data e hora atual

                    if data_usuario == hoje: #Se a data da viagem for hoje, verifica o horário
                        hh, mm = map(int, horario_linha.split(":")) #Pega as horas e minutos do horário da linha
                        if hh < agora.hour or (hh == agora.hour and mm <= agora.minute): #Compara com o horário atual
                            print("\nEsse ônibus já partiu hoje.\n")
                            relatorios.registrar_erro("Ônibus já partiu", linha_id, data_str, "-") #Registra o erro se o ônibus já partiu
                            continue

                    onibus = consultarassentos.pegar_ou_criar_onibus_por_data(linhas, linha_id, data_str) #Obtém o mapa de assentos para a data especificada
                    
                    
                    escolhido = rauto.reservar_assento_automatico(onibus) #Tenta reservar um assento automaticamente

                    if escolhido is None:
                        print("Nenhum assento disponível!\n")
                        relatorios.registrar_erro("Ônibus cheio", linha_id, data_str, "-") #Registra o erro se não houver assentos disponíveis
                        continue

                    print(f"Assento {escolhido:02d} reservado automaticamente na linha {linha_id} em {data_str}!\n")

                    preco = linhas[linha_id][3] 
                    relatorios.registrar_venda(linha_id, data_str, preco) #Registra a venda no relatório

                except Exception as e:
                    print("Erro ao processar reserva automática:")
                    print(e)

            elif opcao == "6":
                try:
                    print("\n\t RELATÓRIOS \n")
                    print("1 - Total arrecadado no mês por linha")
                    print("2 - Ocupação média por dia da semana")
                    print("3 - Relatório de erros")
                    print("4 - Gerar arquivo de reservas inválidas")
                    print("0 - Voltar\n")

                    r = input("Escolha: ").strip()

                    if r == "1":
                        modo = input("Imprimir na tela (T) ou salvar em arquivo (A)? ").strip().upper()
                        relatorios.relatorio_faturamento(linhas, imprimir_na_tela=(modo == "T")) #Chama a função de relatório de faturamento

                    elif r == "2":
                        modo = input("Imprimir na tela (T) ou salvar em arquivo (A)? ").strip().upper()
                        relatorios.relatorio_ocupacao(linhas, imprimir_na_tela=(modo == "T")) #Chama a função de relatório de ocupação média

                    elif r == "3":
                        modo = input("Imprimir na tela (T) ou salvar em arquivo (A)? ").strip().upper()
                        relatorios.relatorio_erros(imprimir_na_tela=(modo == "T")) #Chama a função de relatório de erros

                    elif r == "4":
                        relatorios.salvar_reservas_invalidas(linhas) #Chama a função para salvar reservas inválidas em arquivo

                    elif r == "0":
                        pass

                    else:
                        print("Opção inválida!\n")

                except Exception as e:
                    print("Erro inesperado no menu de relatórios.")
                    print(e)

            elif opcao == "7":
                print("\n\t IMPORTAÇÃO DE RESERVAS EM LOTE \n")
                print("Certifique-se que o arquivo está na pasta do projeto.")
                print("Formato exigido: CIDADE_DESTINO, HORARIO, DATA, ASSENTO")
                
                nome_arq = input("Digite o nome do arquivo (ex: reservas.txt): ").strip()
                
                if not nome_arq:
                    nome_arq = "reservas.txt" #Nome padrão caso o usuário não informe nenhum
                
                lerarquivo.processar_arquivo_reservas(linhas, relatorios.historico_vendas, nome_arq) #Chama a função para processar o arquivo de reservas
                
                input("\nPressione ENTER para continuar")

            elif opcao == "0":
                print("Encerrando o sistema")
                break

            else:
                print("Opção inválida! Tente novamente.")

        except Exception as e:
            print("Erro inesperado! Tente novamente.")
            print(e)