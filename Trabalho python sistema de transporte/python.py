import random

if __name__ == "__main__":
    while True:
        print("\n===== SISTEMA DE TRANSPORTE DE PASSAGEIROS =====\n")
        print("1 - Cadastro de Linhas")
        print("    1.1 - Inserir Linha")
        print("    1.2 - Remover Linha")
        print("    1.3 - Alterar Linha")
        print("\n-----------------------------------------------\n")
        print("2 - Consultar horários disponíveis por cidade")
        print("3 - Consultar assentos disponíveis")
        print("4 - Reservar assento (manual)")
        print("5 - Ler reservas de arquivo texto")
        print("6 - Relatórios")
        print("    6.1 - Total arrecadado no mês por linha")
        print("    6.2 - Ocupação média por dia da semana")
        print("\n-----------------------------------------------\n")
        print("7 - Sair")
        print("===============================================\n")

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

                try:
                    sub = input("Escolha: ").strip()

                    if sub == "1":
                        print("Inserindo linha...")
                        # inserir linha

                    elif sub == "2":
                        print("Removendo linha...")
                        # remover linha

                    elif sub == "3":
                        print("Alterando linha...")
                        # alterar linha

                    else:
                        print("Opção inválida no submenu de linhas!")

                except Exception:
                    print("Erro no submenu de cadastro!")

            # -----------------------------------------------------------
            # OPÇÃO 2 - CONSULTAR HORÁRIOS
            # -----------------------------------------------------------
            elif opcao == "2":
                print("\nConsultar horários disponíveis por cidade...")
                # lógica

            # -----------------------------------------------------------
            # OPÇÃO 3 - CONSULTAR ASSENTOS
            # -----------------------------------------------------------
            elif opcao == "3":
                print("\nConsultar assentos disponíveis...")
                # lógica

            # -----------------------------------------------------------
            # OPÇÃO 4 - RESERVA MANUAL
            # -----------------------------------------------------------
            elif opcao == "4":
                print("\nReserva manual de assento...")
                # lógica

            # -----------------------------------------------------------
            # OPÇÃO 5 - LER ARQUIVO DE RESERVAS
            # -----------------------------------------------------------
            elif opcao == "5":
                print("\nLer reservas de arquivo texto...")
                # lógica

            # -----------------------------------------------------------
            # OPÇÃO 6 - RELATÓRIOS
            # -----------------------------------------------------------
            elif opcao == "6":
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
            # OPÇÃO 7 - SAIR
            # -----------------------------------------------------------
            elif opcao == "7":
                print("Encerrando o sistema...")
                break

            else:
                print("Opção inválida! Tente novamente.")

        except Exception:
            print("Erro inesperado! Tente novamente.")
