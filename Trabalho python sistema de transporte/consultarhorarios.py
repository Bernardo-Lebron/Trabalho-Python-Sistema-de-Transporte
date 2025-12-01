def consultar_horarios(linhas):
    """ Consulta horários de linhas por cidade de DESTINO. """

    print("\n\t CONSULTA DE HORÁRIOS POR CIDADE DE DESTINO \n")

    if not linhas:
        print("Nenhuma linha cadastrada!")
        return

    # MUDANÇA AQUI: Agora pedimos a cidade de destino
    cidade = input("Digite a cidade de destino: ").strip().title()

    encontrados = []

    for ID, dados in linhas.items():
        # MUDANÇA AQUI: Agora comparamos com a cidade de destino (índice 1)
        destino = dados[1] 

        if destino == cidade:
            encontrados.append((ID, dados))

    if not encontrados:
        print(f"\nNenhuma linha encontrada com destino a: '{cidade}'\n")
        return

    print(f"\nLinhas encontradas com destino a {cidade}:\n")

    for ID, dados in encontrados:
        origem, destino, horario, preco = dados[:4]
        # Exibimos a Origem e o Horário (já que o Destino é a cidade buscada)
        print(f"{ID} – Origem: {origem} | Destino: {destino} | Horário: {horario} | Preço: R${preco:.2f}")

    print()