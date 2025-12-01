import datetime

# ============================================================
#   ESTRUTURAS GLOBAIS PARA REGISTRO DE EVENTOS
# ============================================================

historico_vendas = []     # Armazena vendas confirmadas
historico_erros = []      # Armazena erros de reserva


# ============================================================
#   REGISTRO DE EVENTOS
# ============================================================

def registrar_venda(id_linha, data, valor):
    """Registra uma venda confirmada na lista historico_vendas."""
    historico_vendas.append({
        "linha": id_linha,
        "data": data,
        "valor": valor
    })


def registrar_erro(motivo, id_linha, data, assento=None):
    """Registra um erro ocorrido ao tentar reservar."""
    historico_erros.append({
        "motivo": motivo,
        "linha": id_linha,
        "data": data,
        "assento": assento
    })


# ============================================================
#   RELATÓRIO 6.1 – FATURAMENTO DO MÊS CORRENTE
# ============================================================

def relatorio_faturamento(linhas, imprimir_na_tela=True):
    """
    Mostra o total arrecadado por linha no mês atual.
    Se imprimir_na_tela=False, salva em 'relatorio_faturamento.txt'.
    """

    hoje = datetime.date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    # Somar por linha
    totals = {}

    for venda in historico_vendas:
        data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y").date()

        if data_venda.month == mes_atual and data_venda.year == ano_atual:
            linha = venda["linha"]
            totals[linha] = totals.get(linha, 0) + venda["valor"]

    # Montar resultado
    texto = []
    texto.append("=== RELATÓRIO DE FATURAMENTO – MÊS ATUAL ===\n")

    if not totals:
        texto.append("Nenhuma venda registrada neste mês.\n")
    else:
        for linha_id, total in totals.items():
            origem, destino, horario, preco = linhas[linha_id][:4]
            texto.append(
                f"{linha_id} ({origem} → {destino} às {horario})  →  R$ {total:.2f}"
            )

    conteudo = "\n".join(texto)

    if imprimir_na_tela:
        print(conteudo)
    else:
        with open("relatorio_faturamento.txt", "w", encoding="utf-8") as arq:
            arq.write(conteudo)
        print("\nArquivo 'relatorio_faturamento.txt' gerado com sucesso!\n")


# ============================================================
#   RELATÓRIO 6.2 – OCUPAÇÃO MÉDIA POR DIA DA SEMANA
# ============================================================

def relatorio_ocupacao(linhas, imprimir_na_tela=True):
    try:
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

        # matriz ocupação: linha -> [[],[],...,[]]
        matriz = {lid: [[] for _ in range(7)] for lid in linhas}

        # Coleta de dados
        for lid, dados in linhas.items():
            try:
                if len(dados) >= 5 and isinstance(dados[4], dict):
                    for data_str, onibus in dados[4].items():
                        try:
                            data = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
                            dia = data.weekday()
                        except:
                            continue

                        ocupados = 0
                        for livre in onibus.values():
                            try:
                                if not livre:
                                    ocupados += 1
                            except:
                                pass

                        percentual = (ocupados / 20) * 100
                        matriz[lid][dia].append(percentual)
            except:
                pass

        # ----------------------------------------------
        #   Construção do texto (sempre mostra tudo)
        # ----------------------------------------------
        texto = []
        texto.append("=== OCUPAÇÃO MÉDIA POR DIA DA SEMANA ===\n")

        if not linhas:
            texto.append("Nenhuma linha cadastrada.\n")
        else:
            for lid in linhas:
                try:
                    origem, destino, horario, preco = linhas[lid][:4]
                    texto.append(f"\n{lid} – {origem} → {destino} ({horario})")
                except:
                    texto.append(f"\n{lid}")

                # Sempre exibir os 7 dias
                for i in range(7):
                    try:
                        if matriz[lid][i]:
                            media = sum(matriz[lid][i]) / len(matriz[lid][i])
                            texto.append(f"  {dias_semana[i]}: {media:.2f}%")
                        else:
                            texto.append(f"  {dias_semana[i]}: sem dados")
                    except:
                        texto.append(f"  {dias_semana[i]}: erro ao ler dados")

        conteudo = "\n".join(texto)

        if imprimir_na_tela:
            print(conteudo)
        else:
            try:
                with open("relatorio_ocupacao.txt", "w", encoding="utf-8") as arq:
                    arq.write(conteudo)
                print("\nArquivo 'relatorio_ocupacao.txt' gerado com sucesso!\n")
            except:
                print("\nErro ao salvar arquivo de relatório!\n")

    except Exception as e:
        print("Erro ao gerar relatório de ocupação:", e)



# ============================================================
#   RELATÓRIO 6.3 – ERROS
# ============================================================

def relatorio_erros(imprimir_na_tela=True):
    """
    Mostra todos os erros registrados em tentativas de reserva.
    """

    texto = []
    texto.append("=== RELATÓRIO DE ERROS ===\n")

    if not historico_erros:
        texto.append("Nenhum erro registrado.")
    else:
        for e in historico_erros:
            texto.append(
                f"{e['data']} | Linha {e['linha']} | Assento {e.get('assento', '-')}"
                f" → Motivo: {e['motivo']}"
            )

    conteudo = "\n".join(texto)

    if imprimir_na_tela:
        print(conteudo)
    else:
        with open("relatorio_erros.txt", "w", encoding="utf-8") as arq:
            arq.write(conteudo)
        print("\nArquivo 'relatorio_erros.txt' gerado com sucesso!\n")

# ============================================================
#  FUNÇÕES PARA SALVAR RESERVAS INVÁLIDAS EM ARQUIVO
# ============================================================

def _formatar_erro_linha(e, linhas):
    """
    Retorna uma string formatada contendo as informações do erro.
    e: um dicionário com chaves 'motivo','linha','data','assento' (assento pode ser None ou '-')
    linhas: dicionário de linhas (para pegar origem/destino/horario se existir)
    """
    linha_id = e.get("linha", "-")
    data = e.get("data", "-")
    assento = e.get("assento", "-")
    motivo = e.get("motivo", "-")

    # Tentar obter horário / origem->destino se a linha existir no dicionário
    horario = "-"
    origem_destino = "-"
    try:
        if linha_id in linhas:
            dados = linhas[linha_id]
            # suportar list ou dict
            if isinstance(dados, (list, tuple)):
                if len(dados) >= 3:
                    origem = dados[0]
                    destino = dados[1]
                    horario = dados[2]
                    origem_destino = f"{origem} → {destino}"
            elif isinstance(dados, dict):
                origem = dados.get("origem", "-")
                destino = dados.get("destino", "-")
                horario = dados.get("horario", "-")
                origem_destino = f"{origem} → {destino}"
    except:
        pass

    return f"{data} | Linha: {linha_id} | Horário: {horario} | {origem_destino} | Assento: {assento} | Motivo: {motivo}"


def salvar_reservas_invalidas(linhas, filename="reservas_invalidas.txt", imprimir_na_tela=False):
    """
    Salva todas as entradas de historico_erros em um arquivo texto (substitui o arquivo).
    linhas: dicionário de linhas (para mostrar horário/origem/destino)
    filename: nome do arquivo a ser gerado
    imprimir_na_tela: se True imprime o conteúdo na tela também
    """
    try:
        if not historico_erros:
            conteudo = "Nenhuma reserva inválida registrada.\n"
        else:
            linhas_texto = []
            linhas_texto.append("=== RESERVAS INVÁLIDAS ===\n")
            for e in historico_erros:
                linhas_texto.append(_formatar_erro_linha(e, linhas))
            conteudo = "\n".join(linhas_texto) + "\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(conteudo)

        if imprimir_na_tela:
            print("\n" + conteudo)

        print(f"\nArquivo '{filename}' gerado/salvo com sucesso!\n")
    except Exception as ex:
        print("Erro ao salvar reservas inválidas em arquivo:", ex)


def append_erro_arquivo(e, linhas, filename="reservas_invalidas.txt"):
    """
    Anexa um único erro 'e' ao arquivo (modo append). Útil para gravar erros imediatamente
    quando ocorrerem (por exemplo, enquanto processa um arquivo de reservas).
    e: dicionário com campos como em historico_erros
    """
    try:
        linha_texto = _formatar_erro_linha(e, linhas) + "\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(linha_texto)
    except Exception as ex:
        # Não interromper a execução por causa do log
        print("Erro ao gravar (append) reserva inválida:", ex)