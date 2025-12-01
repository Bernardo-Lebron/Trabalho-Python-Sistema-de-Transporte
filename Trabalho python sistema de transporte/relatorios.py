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

    #Data atual
    hoje = datetime.date.today() 
    mes_atual = hoje.month 
    ano_atual = hoje.year

    totals = {} #Dicionário para armazenar o total por linha

    for venda in historico_vendas: #Percorre todas as vendas registradas
        try:
            data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y").date() 
        except:
            continue

        if data_venda.month == mes_atual and data_venda.year == ano_atual: #Se a venda for do mês e ano atual
            linha = venda["linha"] #ID da linha vendida
            totals[linha] = totals.get(linha, 0) + venda["valor"] #Acumula o valor da venda no total da linha


    texto = [] #Lista para armazenar as linhas do relatório
    texto.append(f"\n\t RELATÓRIO DE FATURAMENTO - {mes_atual:02d}/{ano_atual} \n") 

    if not totals:
        texto.append("\nNenhuma venda registrada neste mês.\n") 
    else:
        texto.append("")
        for linha_id, total in totals.items(): #Percorre cada linha e seu total arrecadado
            try:
                origem, destino, horario, preco = linhas[linha_id][:4] #Pega os dados da linha
                texto.append(
                    f"{linha_id} (Origem: {origem} | Destino: {destino} | Horário: {horario}) | R$ {total:.2f}" #Imprime os dados formatados
                )
            except:
                texto.append(
                    f"{linha_id} (Dados da linha indisponíveis) | R$ {total:.2f}" 
                )
        texto.append("\n")

    conteudo = "\n".join(texto) #Concatena as linhas do relatório

    if imprimir_na_tela:
        print(conteudo) 
    else:
        try:
            with open("relatorio_faturamento.txt", "w", encoding="utf-8") as arq: #Salva o relatório em um arquivo
                arq.write(conteudo)
            print("\nArquivo 'relatorio_faturamento.txt' gerado com sucesso!\n") 
        except:
            print("\nErro ao salvar arquivo de relatório de faturamento!\n")



def relatorio_ocupacao(linhas, imprimir_na_tela=True):
    """Mostra a ocupação média por dia da semana para cada linha."""

    try:
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

        matriz = {lid: [[] for _ in range(7)] for lid in linhas} #Matriz para armazenar percentuais de ocupação por linha e dia da semana

        for lid, dados in linhas.items(): #Percorre cada linha cadastrada
            try:
                if len(dados) >= 5 and isinstance(dados[4], dict): #Verifica se há dados de ônibus por data
                    mapa_onibus_por_data = dados[4] 
                else:
                    continue

                for data_str, onibus in mapa_onibus_por_data.items(): #Percorre cada data e seu mapa de assentos
                    try:
                        data = datetime.datetime.strptime(data_str, "%d/%m/%Y").date() #Converte a string da data para objeto date
                        dia = data.weekday() #Obtém o dia da semana (0=Segunda, 6=Domingo)
                    except:
                        continue

                    ocupados = 0 #Contador de assentos ocupados
                    total_assentos = 0 #Contador de assentos totais
                    for livre in onibus.values(): #Percorre o mapa de assentos
                        total_assentos += 1 #Conta o total de assentos
                        if not livre: #Se o assento estiver ocupado 
                            ocupados += 1 #Incrementa o contador de ocupados
                    
                    if total_assentos > 0: 
                        percentual = (ocupados / total_assentos) * 100 #Calcula o percentual de ocupação
                        matriz[lid][dia].append(percentual) #Adiciona o percentual à matriz
            except Exception as e:
                pass

        texto = []
        texto.append("\n\t OCUPAÇÃO MÉDIA POR DIA DA SEMANA \n")

        if not linhas:
            texto.append("Nenhuma linha cadastrada.\n")
        else:
            for lid in linhas: #Percorre cada linha cadastrada
                try:
                    origem, destino, horario, preco = linhas[lid][:4] #Pega os dados da linha
                    texto.append(f"\n{lid} - Origem: {origem} | Destino: {destino} ({horario})") #Imprime o cabeçalho da linha
                except:
                    texto.append(f"\n{lid}") 

                for i in range(7): #Percorre os dias da semana
                    if matriz[lid][i]: #Se houver dados para aquele dia
                        media = sum(matriz[lid][i]) / len(matriz[lid][i]) #Calcula a média dos percentuais
                        texto.append(f"  {dias_semana[i]}: {media:.2f}%") #Imprime a média formatada
                    else:
                        texto.append(f"  {dias_semana[i]}: sem dados") #Indica que não há dados para aquele dia

        conteudo = "\n".join(texto) #Concatena as linhas do relatório

        if imprimir_na_tela: #Imprime o relatório na tela
            print(conteudo)
        else:
            try:
                with open("relatorio_ocupacao.txt", "w", encoding="utf-8") as arq: #Salva o relatório em um arquivo
                    arq.write(conteudo) #Escreve o conteúdo no arquivo
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
        for e in historico_erros: #Percorre cada erro registrado
            texto.append(f"{e['data']} | Linha {e['linha']} | Assento {e.get('assento', '-')}"f" | Motivo: {e['motivo']}") #Adiciona a linha formatada ao relatório

    conteudo = "\n".join(texto) #Concatena as linhas do relatório

    if imprimir_na_tela:
        print(conteudo) #Imprime o relatório na tela
    else:
        try:
            with open("relatorio_erros.txt", "w", encoding="utf-8") as arq: #Salva o relatório em um arquivo
                arq.write(conteudo) #Escreve o conteúdo no arquivo
            print("\nArquivo 'relatorio_erros.txt' gerado com sucesso!\n")
        except:
            print("\nErro ao salvar arquivo de relatório de erros!\n")


def _formatar_erro_linha(e, linhas):
    """
    Retorna uma string formatada contendo as informações do erro.
    um dicionário com chaves 'motivo','linha','data','assento' (assento pode ser None ou '-')
    linhas: dicionário de linhas (para pegar origem/destino/horario se existir)
    """

    linha_id = e.get("linha", "-") 
    data = e.get("data", "-")
    assento = e.get("assento", "-")
    motivo = e.get("motivo", "-")

    horario = "-" 
    origem_destino = "-"
    try: #Checa se a linha existe para pegar mais detalhes
        if linha_id in linhas: 
            dados = linhas[linha_id] 
            if isinstance(dados, (list, tuple)): #Verifica se os dados da linha são uma lista ou tupla
                if len(dados) >= 3: #Pega horário, origem e destino
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
            linhas_texto = [] #Lista para armazenar as linhas do relatório
            linhas_texto.append("\n\t RESERVAS INVÁLIDAS \n") #Cabeçalho do relatório
            for e in historico_erros:
                linhas_texto.append(_formatar_erro_linha(e, linhas)) #Adiciona a linha formatada ao relatório
            conteudo = "\n".join(linhas_texto) + "\n" #Concatena as linhas do relatório

        with open(filename, "w", encoding="utf-8") as f: #Abre o arquivo em modo escrita
            f.write(conteudo) #Escreve o conteúdo no arquivo

        if imprimir_na_tela: 
            print("\n" + conteudo) #Imprime o conteúdo na tela

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
        linha_texto = _formatar_erro_linha(e, linhas) + "\n" #Formata a linha do erro
        with open(filename, "a", encoding="utf-8") as f: #Abre o arquivo em modo append
            f.write(linha_texto) #Escreve a linha do erro no arquivo
    except Exception as ex:
        print("Erro ao gravar (append) reserva inválida:", ex)