import cadastro
from consultarhorarios import consultar_horarios
import consultarassentos
import reservarassento

if __name__ == "__main__":

    linhas={}

    while True:
        print("\n===== SISTEMA DE TRANSPORTE DE PASSAGEIROS =====\n")

        print("1 - Cadastro de Linhas")
        print("    1.1 - Inserir Linha")
        print("    1.2 - Remover Linha")
        print("    1.3 - Alterar Linha")
        print("2 - Listar Linhas Cadastradas")
        print("3 - Consultar horários disponíveis por cidade")
        print("4 - Consultar assentos disponíveis")
        print("5 - Reservar assento")
        print("6 - Ler reservas de arquivo texto")
        print("7 - Relatórios")
        print("    7.1 - Total arrecadado no mês por linha")
        print("    7.2 - Ocupação média por dia da semana")
        print("0 - Sair")
        print("\n\n===============================================\n")

        try:
            opcao = input("Escolha uma opção: ").strip()

            # -----------------------------------------------------------
            # OPÇÃO 1 - CADASTRO DE LINHAS
            # -----------------------------------------------------------
            if opcao == "1":
                print("\n--- CADASTRO DE LINHAS ---")
                print("1 - Inserir Linha")
                print("2 - Remover Linha")
                print("3 - Alterar Linha")
                print("4 - Listar Linhas Cadastradas")

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


            elif opcao == "2":
                cadastro.imprimirlinhas(linhas)

            # -----------------------------------------------------------
            # OPÇÃO 3 - CONSULTAR HORÁRIOS
            # -----------------------------------------------------------
            elif opcao == "3":
                consultar_horarios(linhas)
                

            # -----------------------------------------------------------
            # OPÇÃO 4 - CONSULTAR ASSENTOS
            # -----------------------------------------------------------
            elif opcao == "4":
                consultarassentos.consultar_assentos(linhas)
                # lógica

            # -----------------------------------------------------------
            # OPÇÃO 5 - RESERVA MANUAL
            # -----------------------------------------------------------
            elif opcao == "5":
                print("\n=== RESERVA AUTOMÁTICA ===\n")

                if not linhas:
                    print("Nenhuma linha cadastrada!\n")
                    continue

                cadastro.imprimirlinhas(linhas)

                linha_id = input("Digite o ID da linha (ex: L1): ").strip().upper()

                if linha_id not in linhas:
                    print("Linha não encontrada!\n")
                    continue

                dados = linhas[linha_id]

                # se ainda não tem ônibus criado para essa linha, cria
                if len(dados) == 4:
                    dados.append(consultarassentos.gerar_onibus())

                onibus = dados[4]

                import reservarassento
                assento = reservarassento.reservar_assento_automatico(onibus)

                if assento is None:
                    print("Nenhum assento disponível!\n")
                else:
                    print(f"Assento {assento:02d} reservado automaticamente!\n")


            # -----------------------------------------------------------
            # OPÇÃO 6 - LER ARQUIVO DE RESERVAS
            # -----------------------------------------------------------
            elif opcao == "6":
                print("\nLer reservas de arquivo texto...")
                # lógica

            # -----------------------------------------------------------
            # OPÇÃO 7 - RELATÓRIOS
            # -----------------------------------------------------------
            elif opcao == "7":
                print("\n--- RELATÓRIOS ---")
                print("1 - Total arrecadado no mês por linha")
                print("2 - Ocupação média por dia da semana")

                try:
                    sub = input("Escolha: ").strip()

                    if sub == "1":
                        print("Gerando relatório de arrecadação...")
                        # relatório arrecadação

                    elif sub == "2":
                        print("Gerando relatório de ocupação...")
                        # relatório ocupação

                    else:
                        print("Opção inválida no submenu de relatórios!")

                except Exception:
                    print("Erro no submenu de relatórios!")

            # -----------------------------------------------------------
            # OPÇÃO 0 - SAIR
            # -----------------------------------------------------------
            elif opcao == "0":
                print("Encerrando o sistema...")
                break

            else:
                print("Opção inválida! Tente novamente.")

        except Exception:
            print("Erro inesperado! Tente novamente.")