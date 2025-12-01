from datetime import datetime, timedelta
import relatorios 

def gerar_onibus():
    """Gera um ônibus com os 20 assentos livres. (Assento: True/Livre)"""

    return {i: True for i in range(1, 21)}


def fmt_assento(n, livre):
    """Formata o assento para exibição."""

    return f"[{n:02d}]" if livre else "[XX]"


def linha_fileira(onibus, base):
    """Formata uma fileira (4 assentos) do ônibus."""

    esq_janela   = fmt_assento(base,      onibus[base])
    esq_corredor = fmt_assento(base + 1, onibus[base + 1])
    dir_corredor = fmt_assento(base + 3, onibus[base + 3])
    dir_janela   = fmt_assento(base + 2, onibus[base + 2])
    return f"{esq_janela} {esq_corredor}  |      |  {dir_corredor} {dir_janela}"


def imprimir_onibus(onibus):
    """Imprime o mapa de assentos do ônibus."""

    linhas_bus = [linha_fileira(onibus, base) for base in range(1, 20, 4)]
    largura = max(len(l) for l in linhas_bus)

    print("\n+" + "-" * (largura + 2) + "+")
    print("|" + " MAPA DO ÔNIBUS ".center(largura + 2) + "|")
    print("|" + " " * (largura + 2) + "|")

    for l in linhas_bus:
        print("| " + l.ljust(largura) + " |")

    print("+" + "-" * (largura + 2) + "+\n")
    print("  [nn] = assento livre")
    print("  [XX] = assento ocupado\n")


def pegar_ou_criar_onibus_por_data(linhas, idlinha, data):
    """
    Garantes que a linha tenha um mapa de ônibus para a data. 
    Inicializa se não existir.
    """

    dados = linhas[idlinha]

    if isinstance(dados, tuple):
        dados = list(dados)
        linhas[idlinha] = dados

    if len(dados) >= 5 and isinstance(dados[4], dict):
        mapa_datas = dados[4]
        if data not in mapa_datas:
            mapa_datas[data] = gerar_onibus()
        return mapa_datas[data]
    else:
        mapa_datas = {data: gerar_onibus()}
        if len(dados) >= 5:
            dados[4] = mapa_datas
        else:
            dados.append(mapa_datas)
        linhas[idlinha] = dados
        return mapa_datas[data]


def reservar_assento_interativo(onibus, id_linha, data_str, preco):
    """
    Permite ao usuário escolher e reservar um assento.
    Agora recebe ID, data e preço para registrar a venda.
    """

    while True:
        imprimir_onibus(onibus)
        escolha = input("\nEscolha o assento (1-20) ou 's' para sair: ").strip().lower()

        if escolha == "s":
            print("Operação cancelada.\n")
            return None

        if not escolha.isdigit():
            print("Entrada inválida!\n")
            continue

        assento = int(escolha)
        if not (1 <= assento <= 20):
            print("Assento inexistente!\n")
            continue

        if not onibus.get(assento, False):
            print("Assento ocupado!\n")
            continue

        confirmar = input(f"Confirmar assento {assento:02d}? (s/n): ").strip().lower()
        if confirmar == "s":
            onibus[assento] = False
            print(f"Assento {assento:02d} reservado com sucesso!\n")

            relatorios.registrar_venda(id_linha, data_str, preco)

            return assento
        else:
            print("Reserva não confirmada.\n")


def consultar_assentos(linhas):
    """
    Exibe as linhas, pergunta a data e o ID da linha,
    cria o ônibus daquela data se necessário e permite reservar assento.
    """

    try:
        print("\n\t CONSULTA E RESERVA DE ASSENTOS \n")

        if not linhas:
            print("Nenhuma linha cadastrada!\n")
            return

        print("Linhas cadastradas:")
        for ID, dados in linhas.items():
            origem = dados[0]
            destino = dados[1]
            horario = dados[2]
            preco = dados[3]
            print(f"{ID} - {origem} → {destino}  ({horario})  R${preco}")

        idlinha = input("\nDigite o ID da linha que deseja consultar (ex: L1) ou 's' para sair: ").strip().upper()
        if idlinha.lower() == 's':
            print("Voltando ao menu...\n")
            return

        if idlinha not in linhas:
            print("ID não encontrado!\n")
            return

        dados_linha = linhas[idlinha]
        horario_linha = dados_linha[2] 
        preco_linha = dados_linha[3] 

        data_str = input("Digite a data da viagem (dd/mm/aaaa): ").strip()

        try:
            data_usuario = datetime.strptime(data_str, "%d/%m/%Y").date()
        except:
            print("Data inválida! Use o formato dd/mm/aaaa.\n")
            return

        hoje = datetime.today().date()

        if data_usuario < hoje:
            print("\nNão é permitido consultar/reservar um ônibus de uma data que já passou!\n")
            relatorios.registrar_erro("Data já passou", idlinha, data_str, "-")
            return

        if data_usuario > hoje + timedelta(days=30):
            print("\nA data deve estar dentro de 30 dias a partir de hoje.\n")
            relatorios.registrar_erro("Data acima de 30 dias", idlinha, data_str, "-")
            return

        agora = datetime.now()
        if data_usuario == hoje:
            hora_atual = agora.hour
            minuto_atual = agora.minute

            hh, mm = map(int, horario_linha.split(":"))

            if (hh < hora_atual) or (hh == hora_atual and mm <= minuto_atual):
                print("\nEssa linha já partiu hoje! Não é possível reservar.\n")
                relatorios.registrar_erro("Ônibus já partiu", idlinha, data_str, "-")
                return

        onibus = pegar_ou_criar_onibus_por_data(linhas, idlinha, data_str)

        print(f"\nMapa de assentos da linha {idlinha} em {data_str}:")
        imprimir_onibus(onibus)

        op = input("Deseja reservar um assento nessa linha? (s/n): ").strip().lower()
        if op == "s":
            reservar_assento_interativo(onibus, idlinha, data_str, preco_linha) 
            print("Reserva processada. Voltando ao menu...\n")
        else:
            print("Nenhuma reserva feita. Voltando ao menu...\n")

    except Exception as e:
        print("Ocorreu um erro ao consultar assentos:", repr(e))
        print("Voltando ao menu...\n")