import datetime

historico_vendas = []
historico_erros = []


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


def relatorio_faturamento(linhas, imprimir_na_tela=True):
    """
    Mostra o total arrecadado por linha no mês atual.
    Se imprimir_na_tela=False, salva em 'relatorio_faturamento.txt'.
    """

    hoje = datetime.date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    totals = {}

    for venda in historico_vendas:
        try:
            data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y").date()
        except:
            continue

        if data_venda.month == mes_atual and data_venda.year == ano_atual:
            linha = venda["linha"]
            totals[linha] = totals.get(linha, 0) + venda["valor"]


    texto = []
    texto.append(f"\n\t RELATÓRIO DE FATURAMENTO – {mes_atual:02d}/{ano_atual} \n")

    if not totals:
        texto.append("\nNenhuma venda registrada neste mês.\n")
    else:
        texto.append("")
        for linha_id, total in totals.items():
            try:
                origem, destino, horario, preco = linhas[linha_id][:4]
                texto.append(
                    f"{linha_id} (Origem: {origem} | Destino: {destino} | Horário: {horario})  |  R$ {total:.2f}"
                )
            except:
                texto.append(
                    f"{linha_id} (Dados da linha indisponíveis)  |  R$ {total:.2f}"
                )
        texto.append("\n")

    conteudo = "\n".join(texto)

    if imprimir_na_tela:
        print(conteudo)
    else:
        try:
            with open("relatorio_faturamento.txt", "w", encoding="utf-8") as arq:
                arq.write(conteudo)
            print("\nArquivo 'relatorio_faturamento.txt' gerado com sucesso!\n")
        except:
            print("\nErro ao salvar arquivo de relatório de faturamento!\n")



def relatorio_ocupacao(linhas, imprimir_na_tela=True):
    """Mostra a ocupação média por dia da semana para cada linha."""

    try:
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

        matriz = {lid: [[] for _ in range(7)] for lid in linhas}

        for lid, dados in linhas.items():
            try:
                if len(dados) >= 5 and isinstance(dados[4], dict):
                    mapa_onibus_por_data = dados[4]
                else:
                    continue

                for data_str, onibus in mapa_onibus_por_data.items():
                    try:
                        data = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
                        dia = data.weekday()
                    except:
                        continue

                    ocupados = 0
                    total_assentos = 0
                    for livre in onibus.values():
                        total_assentos += 1
                        if not livre:
                            ocupados += 1
                    
                    if total_assentos > 0:
                        percentual = (ocupados / total_assentos) * 100
                        matriz[lid][dia].append(percentual)
            except Exception as e:
                pass

        texto = []
        texto.append("\n\t OCUPAÇÃO MÉDIA POR DIA DA SEMANA \n")

        if not linhas:
            texto.append("Nenhuma linha cadastrada.\n")
        else:
            for lid in linhas:
                try:
                    origem, destino, horario, preco = linhas[lid][:4]
                    texto.append(f"\n{lid} – {origem} → {destino} ({horario})")
                except:
                    texto.append(f"\n{lid}")

                for i in range(7):
                    if matriz[lid][i]:
                        media = sum(matriz[lid][i]) / len(matriz[lid][i])
                        texto.append(f"  {dias_semana[i]}: {media:.2f}%")
                    else:
                        texto.append(f"  {dias_semana[i]}: sem dados")

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


def relatorio_erros(imprimir_na_tela=True):
    """Mostra todos os erros registrados em tentativas de reserva."""

    texto = []
    texto.append("\n\t RELATÓRIO DE ERROS \n")

    if not historico_erros:
        texto.append("Nenhum erro registrado.")
    else:
        for e in historico_erros:
            texto.append(f"{e['data']} | Linha {e['linha']} | Assento {e.get('assento', '-')}"f" | Motivo: {e['motivo']}")

    conteudo = "\n".join(texto)

    if imprimir_na_tela:
        print(conteudo)
    else:
        try:
            with open("relatorio_erros.txt", "w", encoding="utf-8") as arq:
                arq.write(conteudo)
            print("\nArquivo 'relatorio_erros.txt' gerado com sucesso!\n")
        except:
            print("\nErro ao salvar arquivo de relatório de erros!\n")


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

    horario = "-"
    origem_destino = "-"
    try:
        if linha_id in linhas:
            dados = linhas[linha_id]
            if isinstance(dados, (list, tuple)):
                if len(dados) >= 3:
                    origem = dados[0]
                    destino = dados[1]
                    horario = dados[2]
                    origem_destino = f"Origem: {origem} | Destino: {destino}"
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
            conteudo = "\n\t RESERVAS INVÁLIDAS \n\nNenhuma reserva inválida registrada.\n"
        else:
            linhas_texto = []
            linhas_texto.append("\n\t RESERVAS INVÁLIDAS \n")
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
        print("Erro ao gravar (append) reserva inválida:", ex)