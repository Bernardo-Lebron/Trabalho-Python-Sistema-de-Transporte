import cadastro
from consultarhorarios import consultar_horarios
import consultarassentos
import reservarassento
import consultarassentos

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
        print("5 - Reserva automatica de assentos")
        print("6 - Relatórios")
        print("    6.1 - Total arrecadado no mês por linha")
        print("    6.2 - Ocupação média por dia da semana")
        print("7 - Ler reservas de arquivo texto")
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
            # OPÇÃO 5 - RESERVA AUTOMÁTICA
            # -----------------------------------------------------------
            elif opcao == "5":
                import traceback
                try:
                    print("\n=== RESERVA AUTOMÁTICA ===\n")

                    if not linhas:
                        print("Nenhuma linha cadastrada!\n")
                        continue

                    cadastro.imprimirlinhas(linhas)

                    entrada = input("Digite o ID da linha (ex: L1 ou 1) ou 's' para sair: ").strip()
                    if entrada.lower() == 's':
                        continue

                    # Normalizar ID simples: aceita "1" ou "L1" ou "l1"
                    ent = entrada.upper()
                    if ent.startswith("L") and ent[1:].isdigit():
                        linha_id = "L" + str(int(ent[1:]))
                    elif ent.isdigit():
                        linha_id = "L" + str(int(ent))
                    else:
                        print("ID inválido. Use 'L1' ou '1'.\n")
                        continue

                    if linha_id not in linhas:
                        print("Linha não encontrada!\n")
                        continue

                    dados = linhas[linha_id]

                    # Garantir que 'dados' seja lista mutável (alguma função pode ter salvo tupla)
                    if isinstance(dados, tuple):
                        dados = list(dados)

                    # Se ainda não tem ônibus criado para essa linha, cria e salva
                    # Esperamos estrutura inicial: [orig, destino, horario, preco] (len==4)
                    if not (isinstance(dados, list) and len(dados) >= 5 and isinstance(dados[4], dict)):
                        onibus = consultarassentos.gerar_onibus()
                        # converte para lista se preciso e anexa o onibus
                        if isinstance(dados, list):
                            if len(dados) >= 5:
                                dados[4] = onibus
                            else:
                                dados.append(onibus)
                        else:
                            # caso inesperado, sobrescreve com formato padrão
                            dados = [dados[0] if len(dados)>0 else "", 
                                     dados[1] if len(dados)>1 else "",
                                     dados[2] if len(dados)>2 else "",
                                     dados[3] if len(dados)>3 else 0.0,
                                     onibus]
                        linhas[linha_id] = dados
                    else:
                        onibus = dados[4]

                    # Agora chama a função de reserva automática
                    import reservarassento as rauto  # seu arquivo com a função
                    escolhido = rauto.reservar_assento_automatico(onibus)

                    if escolhido is None:
                        print("Nenhum assento disponível!\n")
                    else:
                        print(f"Assento {escolhido:02d} reservado automaticamente na linha {linha_id}!\n")

                except Exception as e:
                    # mostra o erro real (útil para depurar)
                    print("Erro ao processar reserva automática:")
                    traceback.print_exc()
                    print()


            # -----------------------------------------------------------
            # OPÇÃO 6 - RELATÓRIOS
            # -----------------------------------------------------------
            elif opcao == "6":
                print("implementar relatórios...")


            # -----------------------------------------------------------
            # OPÇÃO 7 - LER ARQUIVO DE RESERVAS
            # -----------------------------------------------------------
            elif opcao == "7":
                print("Lendo arquivo de reservas...")
                # lógica

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