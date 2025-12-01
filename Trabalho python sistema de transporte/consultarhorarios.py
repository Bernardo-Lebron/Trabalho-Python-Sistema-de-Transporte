def consultar_horarios(linhas):
    """ Consultar horários de linhas por cidade de origem. """

    print("\n\t CONSULTA DE HORÁRIOS POR CIDADE DE ORIGEM \n")

    if not linhas:
        print("Nenhuma linha cadastrada!")
        return

    cidade = input("Digite a cidade de origem: ").strip().title()

    encontrados = []

    for ID, dados in linhas.items():
        origem = dados[0]

        if origem == cidade:
            encontrados.append((ID, dados))

    if not encontrados:
        print(f"\nNenhuma linha encontrada partindo de: '{cidade}'\n")
        return

    print(f"\nLinhas encontradas partindo de {cidade}:\n")

    for ID, dados in encontrados:
        origem, destino, horario, preco = dados[:4]
        print(f"{ID} – Origem: {origem} | Destino: {destino} | Horário: {horario} | Preço: R${preco:.2f}")

    print()