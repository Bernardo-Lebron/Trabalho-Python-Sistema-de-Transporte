from datetime import datetime, timedelta

# ==========================
#  GERAÇÃO DO ÔNIBUS
# ==========================
def gerar_onibus():
    """Gera um ônibus com os 20 assentos livres."""
    return {i: True for i in range(1, 21)}


# ==========================
#  FORMATAÇÃO E IMPRESSÃO
# ==========================
def fmt_assento(n, livre):
    return f"[{n:02d}]" if livre else "[XX]"


def linha_fileira(onibus, base):
    esq_janela   = fmt_assento(base,     onibus[base])
    esq_corredor = fmt_assento(base + 1, onibus[base + 1])
    dir_corredor = fmt_assento(base + 3, onibus[base + 3])
    dir_janela   = fmt_assento(base + 2, onibus[base + 2])
    return f"{esq_janela} {esq_corredor}  |     |  {dir_corredor} {dir_janela}"


def imprimir_onibus(onibus):
    linhas = [linha_fileira(onibus, base) for base in range(1, 20, 4)]
    largura = max(len(l) for l in linhas)

    print("\n+" + "-" * (largura + 2) + "+")
    print("|" + " MAPA DO ÔNIBUS ".center(largura + 2) + "|")
    print("|" + " " * (largura + 2) + "|")

    for l in linhas:
        print("| " + l.ljust(largura) + " |")

    print("+" + "-" * (largura + 2) + "+\n")
    print("  [nn] = assento livre")
    print("  [XX] = assento ocupado\n")


# ==========================
#  Compatibilidade: pega/cria ônibus POR DATA
# ==========================
def pegar_ou_criar_onibus_por_data(linhas, idlinha, data):
    """
    Garante que a linha (que pode ser lista ou dict) tenha um mapa de ônibus por data.
    - linhas: dicionário principal (para poder reatribuir se converter tuple->list)
    - idlinha: chave da linha (ex: 'L1')
    - data: string 'dd/mm/aaaa'
    Retorna o mapa de assentos (dict 1..20 -> bool).
    """
    dados = linhas[idlinha]

    # Se for tupla (improvável), converte para lista e salva
    if isinstance(dados, tuple):
        dados = list(dados)
        linhas[idlinha] = dados

    # Caso seja dicionário (estrutura alternativa), usamos chaves legíveis
    if isinstance(dados, dict):
        if "onibus" not in dados:
            dados["onibus"] = {}
        if data not in dados["onibus"]:
            dados["onibus"][data] = gerar_onibus()
        return dados["onibus"][data]

    # Caso seja lista (o seu formato atual: [orig,dest,horario,preco] possivelmente com onibus como 5º elem)
    if isinstance(dados, list):
        # Se o 5º elemento existe e é um dict, assumimos que é o mapa de onibus por data
        if len(dados) >= 5 and isinstance(dados[4], dict):
            # dados[4] deve ser um dict de datas -> onibus
            mapa = dados[4]
            if data not in mapa:
                mapa[data] = gerar_onibus()
            return mapa[data]
        else:
            # ainda não há campo 'onibus' — criamos como 5º elemento
            mapa = {}
            mapa[data] = gerar_onibus()
            if len(dados) >= 5:
                dados[4] = mapa
            else:
                dados.append(mapa)
            linhas[idlinha] = dados  # garante atualização no dicionário principal
            return mapa[data]

    # Se for outro tipo inesperado, lançamos erro para depuração
    raise TypeError(f"Formato de dados da linha '{idlinha}' inesperado: {type(dados)}")


# ==========================
#  RESERVA INTERATIVA
# ==========================
def reservar_assento_interativo(onibus):
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
            return assento
        else:
            print("Reserva não confirmada.\n")


# ==========================
#  CONSULTA DE ASSENTOS
# ==========================
def consultar_assentos(linhas):
    """
    Exibe as linhas, pergunta a data e o ID da linha,
    cria o ônibus daquela data se necessário e permite reservar assento.
    Agora com validação:
    - data passada proibida
    - data acima de 30 dias proibida
    - se for hoje, horário deve ser futuro
    """

    try:
        print("\n=== CONSULTA E RESERVA DE ASSENTOS ===\n")

        if not linhas:
            print("Nenhuma linha cadastrada!\n")
            return

        # Lista as linhas existentes
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
        horario_linha = dados_linha[2]  # HH:MM do ônibus

        # ===========================
        # VALIDAR DATA
        # ===========================
        data_str = input("Digite a data da viagem (dd/mm/aaaa): ").strip()

        # Tentar converter para datetime
        try:
            data_usuario = datetime.strptime(data_str, "%d/%m/%Y").date()
        except:
            print("Data inválida! Use o formato dd/mm/aaaa.\n")
            return

        hoje = datetime.today().date()

        # Verificar se data é passada
        if data_usuario < hoje:
            print("\nNão é permitido consultar/reservar um ônibus de uma data que já passou!\n")
            return

        # Verificar se é mais de 30 dias à frente
        if data_usuario > hoje + timedelta(days=30):
            print("\nA data deve estar dentro de 30 dias a partir de hoje.\n")
            return

        # ===========================
        # CASO A DATA SEJA HOJE → CHECAR HORÁRIO
        # ===========================
        agora = datetime.now()
        if data_usuario == hoje:
            hora_atual = agora.hour
            minuto_atual = agora.minute

            hh, mm = map(int, horario_linha.split(":"))

            if (hh < hora_atual) or (hh == hora_atual and mm <= minuto_atual):
                print("\nEssa linha já partiu hoje! Não é possível reservar.\n")
                return

        # ===========================
        # PEGAR / CRIAR ÔNIBUS DA DATA
        # ===========================
        onibus = pegar_ou_criar_onibus_por_data(linhas, idlinha, data_str)

        print(f"\nMapa de assentos da linha {idlinha} em {data_str}:")
        imprimir_onibus(onibus)

        op = input("Deseja reservar um assento nessa linha? (s/n): ").strip().lower()
        if op == "s":
            reservar_assento_interativo(onibus)
            print("Reserva processada. Voltando ao menu...\n")
        else:
            print("Nenhuma reserva feita. Voltando ao menu...\n")

    except Exception as e:
        print("Ocorreu um erro ao consultar assentos:", repr(e))
        print("Voltando ao menu...\n")