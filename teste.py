import random

def gerar_onibus(prob_ocupado=0.3):
    return {i: (random.random() >= prob_ocupado) for i in range(1, 21)}

def fmt_assento(n, livre):
    if livre:
        return f"[{n:02d}]"
    else:
        return "[XX]"

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

    # LEGENDA FORA DO RETÂNGULO
    print("  [nn] = assento livre")
    print("  [XX] = assento ocupado")

def reservar_assento_interativo(onibus):
    while True:
        imprimir_onibus(onibus)

        escolha = input("\nEscolha o assento (1-20) ou 's' para sair: ").strip().lower()

        if escolha == "s":
            print("Reserva cancelada.\n")
            return None

        if not escolha.isdigit():
            print("Entrada inválida!\n")
            continue

        escolha = int(escolha)

        if not (1 <= escolha <= 20):
            print("Assento inexistente!\n")
            continue

        if not onibus[escolha]:
            print("Assento ocupado!\n")
            continue

        confirmar = input(f"Confirmar assento {escolha:02d}? (s/n): ").strip().lower()

        if confirmar == "s":
            onibus[escolha] = False
            print(f"✔ Assento {escolha:02d} reservado com sucesso!\n")
            return escolha
        else:
            print("Reserva não confirmada.\n")

# Teste independente
if __name__ == "__main__":
    bus = gerar_onibus()
    reservar_assento_interativo(bus)
