def consultar_horarios(linhas):
    """ Consulta horários de linhas por cidade de DESTINO. """

    print("\n\t CONSULTA DE HORÁRIOS POR CIDADE DE DESTINO \n")

    if not linhas:
        print("Nenhuma linha cadastrada!")
        return

    cidade = input("Digite a cidade de destino: ").strip().title()

    encontrados = [] #Lista para armazenar linhas encontradas

    for ID, dados in linhas.items(): #Percorre todas as linhas cadastradas
        destino = dados[1] 

        if destino == cidade: #Se o destino da linha corresponder à cidade desejada
            encontrados.append((ID, dados)) #Adiciona a linha à lista de encontrados

    if not encontrados:
        print(f"\nNenhuma linha encontrada com destino a: '{cidade}'\n")
        return

    print(f"\nLinhas encontradas com destino a {cidade}:\n") #Imprime as linhas encontradas

    for ID, dados in encontrados: #Percorre as linhas encontradas
        origem, destino, horario, preco = dados[:4] #Insere os dados da linha
        print(f"{ID}  Origem: {origem} | Destino: {destino} | Horário: {horario} | Preço: R${preco:.2f}") #Imprime os dados formatados

    print()