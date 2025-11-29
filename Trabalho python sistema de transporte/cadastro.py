def validar_horario(h):
    """ Validar se o horário está no formato HH:MM e é um horário real. """


    try:
        # Formato precisa ser exatamente HH:MM
        if len(h) != 5 or h[2] != ":":
            return False

        hh, mm = h.split(":")

        # Converter para número
        hh = int(hh)
        mm = int(mm)

        # Regras reais de tempo
        return 0 <= hh <= 23 and 0 <= mm <= 59
    except:
        return False


def inserirlinha(linhas):
    """ Inserir nova linha no dicionário de linhas. """


    print("\n-----------------------------------------------\n")

    origem = input('Digite a cidade de origem da linha: ').strip().title()
    destino = input('Digite a cidade de destino da linha: ').strip().title()

    # --- VALIDAR HORÁRIO ---
    while True:
        horario = input('Digite o horário de saída da linha [ex: 19:00]: ').strip()
        try:
            if validar_horario(horario):
                break
            else:
                print("Horário inválido! Use o formato HH:MM e valores reais (00–23:00–59).")
        except:
            print("Erro ao ler horário, tente novamente.")

    # --- VALIDAR PREÇO ---
    while True:
        preco_str = input('Digite o preço da linha [ex: 59.90]: R$ ')
        try:
            preco = float(preco_str.replace(",", "."))
            if preco >= 0:
                break
            else:
                print("O preço não pode ser negativo!")
        except:
            print("Preço inválido! Digite apenas números.")

    info = [origem, destino, horario, preco]

    ID = f"L{len(linhas) + 1}"
    linhas[ID] = info

    imprimirlinhaatual(linhas, ID)
    print("Linha cadastrada com sucesso!\n")


def imprimirlinhaatual(linhas, ID):
    """ Imprimir os dados de uma linha específica. """


    origem, destino, horario, preco = linhas[ID]
    print(f'\nLinha {ID}: Origem: {origem} | Destino: {destino} | Horário: {horario} | Preço: R${preco:.2f}\n')


def imprimirlinhas(linhas):
    """ Imprimir todas as linhas cadastradas. """


    print("\n=== LINHAS CADASTRADAS ===")
    if not linhas:
        print("Nenhuma linha cadastrada.\n")
        return

    for k, v in linhas.items():
        origem, destino, horario, preco = v
        print(f'{k}: Origem: {origem} | Destino: {destino} | Horário: {horario} | Preço: R${preco:.2f}')
    print()


def alterarlinha(linhas):
    """ Alterar dados de uma linha existente. """


    imprimirlinhas(linhas)

    idalterar = input("Digite o ID da linha que deseja alterar (ex: L1): ").strip().upper()

    if idalterar not in linhas:
        print("ID não encontrado!")
        return

    print("\n1 - Alterar a linha inteira")
    print("2 - Alterar apenas um campo\n")

    resposta = input("Escolha: ").strip()

    if resposta == "1":

        nova_origem = input(f"Nova origem [Atual: {linhas[idalterar][0]}]: ").strip().title()
        novo_destino = input(f"Novo destino [Atual: {linhas[idalterar][1]}]: ").strip().title()

        # Validar horário novamente
        while True:
            novo_horario = input(f"Novo horário [Atual: {linhas[idalterar][2]}]: ").strip()
            if validar_horario(novo_horario):
                break
            print("Horário inválido!")

        # Validar preço com try/except
        while True:
            preco_str = input(f"Novo preço [Atual: {linhas[idalterar][3]}]: R$ ")
            try:
                novo_preco = float(preco_str.replace(",", "."))
                if novo_preco >= 0:
                    break
                print("Preço não pode ser negativo!")
            except:
                print("Preço inválido!")

        linhas[idalterar] = [nova_origem, novo_destino, novo_horario, novo_preco]
        print("\n✔ Alterações salvas!")

    # ---------------------------------------------------------------------
    # ALTERAR APENAS UM CAMPO
    # ---------------------------------------------------------------------
    elif resposta == "2":
        print("\n1 - Origem\n2 - Destino\n3 - Horário\n4 - Preço\n")

        try:
            opcao = int(input("Escolha o campo: "))
        except:
            print("Opção inválida!")
            return

        if opcao == 1:
            linhas[idalterar][0] = input("Nova origem: ").strip().title()

        elif opcao == 2:
            linhas[idalterar][1] = input("Novo destino: ").strip().title()

        elif opcao == 3:
            # Garantir que o novo horário seja válido
            while True:
                novo_horario = input("Novo horário: ").strip()
                if validar_horario(novo_horario):
                    linhas[idalterar][2] = novo_horario
                    break
                print("Horário inválido! Use o formato HH:MM e valores reais (00–23:00–59).")

        elif opcao == 4:
            while True:
                preco_str = input("Novo preço R$: ")
                try:
                    novo_preco = float(preco_str.replace(",", "."))
                    if novo_preco >= 0:
                        linhas[idalterar][3] = novo_preco
                        break
                    print("Preço não pode ser negativo!")
                except:
                    print("Preço inválido!")

        else:
            print("Opção inválida!")
            return

        print("\nAlteração feita com sucesso!")

    else:
        print("Opção inválida!")


def removerlinha(linhas):
    """ Remover uma linha do dicionário de linhas. """

    
    imprimirlinhas(linhas)
    idrem = input("Digite o ID da linha que deseja remover: ").strip().upper()

    if idrem in linhas:
        del linhas[idrem]
        print("Linha removida!")
    else:
        print("ID não encontrado!")
