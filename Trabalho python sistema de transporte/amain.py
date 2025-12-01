import cadastro
from consultarhorarios import consultar_horarios
import consultarassentos
import relatorios
from datetime import datetime, timedelta
if __name__ == "__main__":

    linhas = {}

    while True:
        print("\n===== SISTEMA DE TRANSPORTE DE PASSAGEIROS =====\n")

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
        print("    6.3 - Relatório de erros (reservas inválidas)")
        print("7 - Ler reservas de arquivo texto")
        print("0 - Sair")
        print("\n===============================================\n")

        try:
            opcao = input("Escolha uma opção: ").strip()

        # =====================================================================
        # OPÇÃO 1 - CADASTRO DE LINHAS
        # =====================================================================
            if opcao == "1":
                print("\n--- CADASTRO DE LINHAS ---")
                print("1 - Inserir Linha")
                print("2 - Remover Linha")
                print("3 - Alterar Linha")

                try:
                    opcao2 = input("Escolha: ").strip()

                    if opcao2 == "1":
                        cadastro.inserirlinha(linhas)

                    elif opcao2 == "2":
                        cadastro.removerlinha(linhas)

                    elif opcao2 == "3":
                        cadastro.alterarlinha(linhas)

                    else:
                        print("Opção inválida no submenu de linhas!")

                except Exception as e:
                    print("Erro no submenu de cadastro! (main)")
                    print(e)


        # =====================================================================
        # OPÇÃO 2 - LISTAR LINHAS
        # =====================================================================
            elif opcao == "2":
                cadastro.imprimirlinhas(linhas)


        # =====================================================================
        # OPÇÃO 3 - CONSULTAR HORÁRIOS
        # =====================================================================
            elif opcao == "3":
                consultar_horarios(linhas)


        # =====================================================================
        # OPÇÃO 4 - CONSULTAR ASSENTOS
        # =====================================================================
            elif opcao == "4":
                consultarassentos.consultar_assentos(linhas)


        # =====================================================================
        # OPÇÃO 5 – RESERVA AUTOMÁTICA
        # =====================================================================
            elif opcao == "5":

                try:
                    print("\n=== RESERVA AUTOMÁTICA ===\n")

                    if not linhas:
                        print("Nenhuma linha cadastrada!\n")
                        continue

                    cadastro.imprimirlinhas(linhas)

                    entrada = input("Digite o ID da linha (ex: L1 ou 1) ou 's' para sair: ").strip()
                    if entrada.lower() == 's':
                        continue

                    # normalizar ID
                    ent = entrada.upper()
                    if ent.startswith("L") and ent[1:].isdigit():
                        linha_id = "L" + str(int(ent[1:]))

                    elif ent.isdigit():
                        linha_id = "L" + str(int(ent))

                    else:
                        print("ID inválido. Use 'L1' ou '1'.\n")
                        relatorios.registrar_erro("ID de linha inválido", "-", "-", "-")
                        continue

                    if linha_id not in linhas:
                        print("Linha não encontrada!\n")
                        relatorios.registrar_erro("Linha não encontrada", linha_id, "-", "-")
                        continue

                    dados = linhas[linha_id]
                    horario_linha = dados[2]   # hh:mm

                    # ---------------------------------------------
                    # VALIDAR DATA
                    # ---------------------------------------------
                    data_str = input("Digite a data da viagem (dd/mm/aaaa): ").strip()

                    try:
                        data_usuario = datetime.strptime(data_str, "%d/%m/%Y").date()
                    except:
                        print("Data inválida! Use dd/mm/aaaa.\n")
                        relatorios.registrar_erro("Data inválida", linha_id, data_str, "-")
                        continue

                    hoje = datetime.today().date()

                    # data passada → proibido
                    if data_usuario < hoje:
                        print("\nNão é permitido reservar para uma data que já passou!\n")
                        relatorios.registrar_erro("Data já passou", linha_id, data_str, "-")
                        continue

                    # mais de 30 dias → proibido
                    if data_usuario > hoje + timedelta(days=30):
                        print("\nA data deve estar dentro de 30 dias.\n")
                        relatorios.registrar_erro("Data acima de 30 dias", linha_id, data_str, "-")
                        continue

                    # se for hoje, verificar horário
                    agora = datetime.now()
                    if data_usuario == hoje:
                        hh, mm = map(int, horario_linha.split(":"))
                        if hh < agora.hour or (hh == agora.hour and mm <= agora.minute):
                            print("\nEsse ônibus já partiu hoje.\n")
                            relatorios.registrar_erro("Ônibus já partiu", linha_id, data_str, "-")
                            continue

                    # ---------------------------------------------
                    # PEGAR OU CRIAR ÔNIBUS POR DATA
                    # ---------------------------------------------
                    from consultarassentos import pegar_ou_criar_onibus_por_data
                    onibus = pegar_ou_criar_onibus_por_data(linhas, linha_id, data_str)

                    # ---------------------------------------------
                    # RESERVA AUTOMÁTICA
                    # ---------------------------------------------
                    import reservarassento as rauto
                    escolhido = rauto.reservar_assento_automatico(onibus)

                    if escolhido is None:
                        print("Nenhum assento disponível!\n")
                        relatorios.registrar_erro("Ônibus cheio", linha_id, data_str, "-")
                        continue

                    print(f"Assento {escolhido:02d} reservado automaticamente "
                          f"na linha {linha_id} em {data_str}!\n")

                    # registrar venda
                    try:
                        preco = linhas[linha_id][3]
                        relatorios.registrar_venda(linha_id, data_str, preco)
                    except:
                        pass

                except Exception as e:
                    print("Erro ao processar reserva automática:")
                    print(e)


            # =====================================================================
            # OPÇÃO 6 – RELATÓRIOS
            # =====================================================================
            elif opcao == "6":
                try:
                    print("\n--- RELATÓRIOS ---")
                    print("1 - Total arrecadado no mês por linha")
                    print("2 - Ocupação média por dia da semana")
                    print("3 - Relatório de erros")
                    print("0 - Voltar\n")

                    r = input("Escolha: ").strip()

                    if r == "1":
                        modo = input("Imprimir na tela (T) ou salvar em arquivo (A)? ").strip().upper()
                        relatorios.relatorio_faturamento(linhas, imprimir_na_tela=(modo == "T"))

                    elif r == "2":
                        modo = input("Imprimir na tela (T) ou salvar em arquivo (A)? ").strip().upper()
                        relatorios.relatorio_ocupacao(linhas, imprimir_na_tela=(modo == "T"))

                    elif r == "3":
                        modo = input("Imprimir na tela (T) ou salvar em arquivo (A)? ").strip().upper()
                        relatorios.relatorio_erros(imprimir_na_tela=(modo == "T"))

                    elif r == "0":
                        pass

                    else:
                        print("Opção inválida!\n")

                except Exception as e:
                    print("Erro inesperado no menu de relatórios.")
                    print(e)


            # -----------------------------------------------------------
            # OPÇÃO 7 - LER ARQUIVO DE RESERVAS
            # -----------------------------------------------------------
            elif opcao == "7":
                print("a ser implementado...")


            # =====================================================================
            # OPÇÃO 0 – SAIR
            # =====================================================================
            elif opcao == "0":
                print("Encerrando o sistema...")
                break

            else:
                print("Opção inválida! Tente novamente.")

        except Exception as e:
            print("Erro inesperado! Tente novamente.")
            print(e)
