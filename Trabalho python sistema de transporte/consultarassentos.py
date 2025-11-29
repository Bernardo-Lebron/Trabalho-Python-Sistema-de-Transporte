import random

def gerar_onibus(prob_ocupado=0.3):
    """Gera um dicionário representando os assentos do ônibus."""

    return {i: (random.random() >= prob_ocupado) for i in range(1, 21)}


def fmt_assento(n, livre):
    """Formata a string de um assento conforme seu estado."""

    return f"[{n:02d}]" if livre else "[XX]"


def linha_fileira(onibus, base):
    """Gera a string de uma fileira do ônibus."""

    esq_janela   = fmt_assento(base,     onibus[base])
    esq_corredor = fmt_assento(base + 1, onibus[base + 1])
    dir_corredor = fmt_assento(base + 3, onibus[base + 3])
    dir_janela   = fmt_assento(base + 2, onibus[base + 2])
    return f"{esq_janela} {esq_corredor}  |     |  {dir_corredor} {dir_janela}"


def imprimir_onibus(onibus):
    """Imprime o mapa de assentos do ônibus."""

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

def reservar_assento_interativo(onibus):
    """Interação para escolher e reservar um assento. Modifica onibus e retorna assento ou None."""

    while True:
        imprimir_onibus(onibus)
        escolha = input("\nEscolha o assento (1-20) ou 's' para sair: ").strip().lower()
        if escolha == "s":
            print("Operação cancelada.\n")
            return None
        if not escolha.isdigit():
            print("Entrada inválida! Digite o número do assento (1-20) ou 's' para sair.\n")
            continue
        escolha = int(escolha)
        if not (1 <= escolha <= 20):
            print("Assento inexistente!\n")
            continue
        if not onibus.get(escolha, False):
            print("Assento ocupado!\n")
            continue
        confirmar = input(f"Confirmar assento {escolha:02d}? (s/n): ").strip().lower()
        if confirmar == "s":
            onibus[escolha] = False
            print(f"✔ Assento {escolha:02d} reservado com sucesso!\n")
            return escolha
        else:
            print("Reserva não confirmada.\n")

# ---------------------------
# função principal do módulo
# ---------------------------
def consultar_assentos(linhas):
    """
    Exibe linhas cadastradas, solicita ID, e mostra/permite reservar assentos
    Cada linha receberá a chave 'onibus' (se for lista, será adicionada como 5º elemento;
    se for dict, será salvo em dados['onibus']).
    """

    try:
        print("\n=== CONSULTA E RESERVA DE ASSENTOS ===\n")

        if not linhas:
            print("Nenhuma linha cadastrada!\n")
            return

        # Lista as linhas (tolerante ao formato)
        print("Linhas cadastradas:")
        for ID, dados in linhas.items():
            if isinstance(dados, dict):
                origem = dados.get("origem", "")
                destino = dados.get("destino", "")
                horario = dados.get("horario", "")
                preco = dados.get("preco", "")
            else:
                # lista/tupla: [origem,destino,horario,preco] (possivelmente com onibus como 5º)
                origem = dados[0] if len(dados) > 0 else ""
                destino = dados[1] if len(dados) > 1 else ""
                horario = dados[2] if len(dados) > 2 else ""
                preco = dados[3] if len(dados) > 3 else ""
            print(f"{ID} - {origem} → {destino}  ({horario})  R${preco}")

        idlinha = input("\nDigite o ID da linha que deseja consultar (ex: L1) ou 's' para sair: ").strip().upper()
        if idlinha.lower() == 's':
            print("Voltando ao menu...\n")
            return

        if idlinha not in linhas:
            print("ID não encontrado!\n")
            return

        # Recupera ou cria o onibus vinculado à linha
        dados = linhas[idlinha]
        # Se for dict e já tem 'onibus', use; se for lista com 5º elemento (mapa), use; senão crie e salve.
        onibus = None
        if isinstance(dados, dict):
            onibus = dados.get("onibus")
            if onibus is None:
                onibus = gerar_onibus()
                dados["onibus"] = onibus  # salva no dicionário da linha
        else:
            # lista/tupla
            if len(dados) >= 5 and isinstance(dados[4], dict):
                onibus = dados[4]
            else:
                onibus = gerar_onibus()
                # se for lista, anexar; se for tupla (improvável), converter para lista
                if isinstance(dados, tuple):
                    dados = list(dados)
                # garante que salvamos o mapa como 5º elemento
                if len(dados) >= 5:
                    dados[4] = onibus
                else:
                    dados.append(onibus)
                linhas[idlinha] = dados  # atualiza entrada no dicionário principal

        # Mostrar mapa e perguntar se deseja reservar
        print(f"\nMapa de assentos da linha {idlinha}:")
        imprimir_onibus(onibus)

        op = input("Deseja reservar um assento nessa linha? (s/n): ").strip().lower()
        if op == "s":
            reservar_assento_interativo(onibus)
            print("Reserva processada. Voltando ao menu...\n")
        else:
            print("Nenhuma reserva feita. Voltando ao menu...\n")

    except Exception as e:
        # nunca deixar quebrar o programa — mostra erro amigável e continua
        print("Ocorreu um erro ao consultar assentos:", e)
        print("Voltando ao menu...\n")
