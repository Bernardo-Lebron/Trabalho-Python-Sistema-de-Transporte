import datetime
import consultarassentos
import os 
import relatorios

def processar_arquivo_reservas(linhas, relatorio_vendas_list, nome_arquivo="reservas.txt"): 
    """
    Lê um arquivo de reservas e processa cada linha.
    Formato esperado: CIDADE_DESTINO, HORARIO, DATA, ASSENTO
    """
    
    pasta_do_script = os.path.dirname(os.path.abspath(__file__)) #Pega o diretório do script atual
    caminho_completo = os.path.join(pasta_do_script, nome_arquivo) #Caminho completo do arquivo a ser lido

    print(f"\n\t Processando arquivo ")
    if not os.path.exists(caminho_completo) and pasta_do_script == '': #Se o arquivo não for encontrado no diretório do script, tenta o diretório atual
         caminho_completo = os.path.join(os.getcwd(), nome_arquivo) #Caminho no diretório atual

    print(f"Procurando em: {caminho_completo}") #Informa o local onde o Python está procurando o arquivo
    
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as arquivo: #Abre o arquivo para leitura
            conteudo = arquivo.readlines() #Lê todas as linhas do arquivo
    except FileNotFoundError:
        print(f"\nERRO CRÍTICO: O arquivo '{nome_arquivo}' não foi encontrado!")
        print(f"O Python tentou ler neste local: {caminho_completo}")
        print("Dica: Verifique se o nome do arquivo está correto e se ele está na pasta do projeto.")
        return

    erros_log = [] #Lista para armazenar erros durante o processamento
    sucessos = 0 #Contador de reservas bem-sucedidas
    linha_num = 0 #Número da linha atual sendo processada
    hoje = datetime.date.today() 

    print(f"Arquivo encontrado! Processando {len(conteudo)} linhas...\n") 

    for linha_texto in conteudo: #Percorre cada linha do arquivo
        linha_num += 1
        linha_texto_original = linha_texto.strip()
        
        if not linha_texto_original: #Ignora linhas vazias
            continue

        id_linha_encontrada = None 
        data_str = None
        assento_num = None
        dados_linha = None
        
        try:
            partes = linha_texto_original.split(',') #Divide a linha em partes separadas por vírgula
            
            if len(partes) != 4: 
                raise ValueError("Formato incorreto (esperado: Cidade, Horário, Data, Assento)") #Verifica se há 4 partes na linha
            
            cidade_destino = partes[0].strip().title() #Pega a cidade de destino e formata
            horario = partes[1].strip() #Pega o horário
            data_str = partes[2].strip() #Pega a data
             
            try:
                assento_num = int(partes[3].strip()) #Converte o número do assento para inteiro
            except ValueError:
                raise ValueError("Número do assento inválido")
            
            for id_linha, dados in linhas.items(): #Procura a linha correspondente ao destino e horário
                if dados[1] == cidade_destino and dados[2] == horario: #Se destino e horário corresponderem
                    id_linha_encontrada = id_linha #Guarda o ID da linha encontrada
                    dados_linha = dados #Guarda os dados da linha encontrada
                    break
            
            if not id_linha_encontrada: #Se nenhuma linha foi encontrada
                raise ValueError(f"Linha não encontrada para {cidade_destino} às {horario}")
            
            try:
                data_viagem = datetime.datetime.strptime(data_str, "%d/%m/%Y").date() #Converte a string da data para um objeto date
            except ValueError:
                raise ValueError("Data inválida (use dd/mm/aaaa)") #Valida a data

            if data_viagem < hoje:
                raise ValueError("Data já passou") #Verifica se a data já passou
            
            if data_viagem > hoje + datetime.timedelta(days=30):
                raise ValueError("Data excede 30 dias") #Verifica se a data está dentro do limite de 30 dias
                
            if data_viagem == hoje: #Se a data for hoje
                agora = datetime.datetime.now()
                try:
                    hh, mm = map(int, horario.split(':')) #Pega horas e minutos do horário da linha
                    if hh < agora.hour or (hh == agora.hour and mm <= agora.minute): #Verifica se o horário já passou hoje
                        raise ValueError("Ônibus já partiu hoje")
                except:
                    pass 

            if isinstance(dados_linha, tuple): #Se os dados da linha estiverem em tupla (imutável)
                dados_linha = list(dados_linha) #Converte para lista (mutável)
                linhas[id_linha_encontrada] = dados_linha #Atualiza o dicionário de linhas com a lista mutável

            onibus = consultarassentos.pegar_ou_criar_onibus_por_data(linhas, id_linha_encontrada, data_str) #Obtém ou cria o mapa de assentos para a data desejada

            if not (1 <= assento_num <= 20): #Verifica se o assento está dentro do intervalo válido
                raise ValueError(f"Assento {assento_num} inexistente")

            if onibus.get(assento_num) == False: #Verifica se o assento já está ocupado
                raise ValueError(f"Assento {assento_num} ocupado")
            

            onibus[assento_num] = False  
            sucessos += 1
            print(f"[OK] Linha {id_linha_encontrada} | {data_str} | Assento {assento_num}") #Confirmação de reserva bem-sucedida

            try:
                preco = dados_linha[3] 
                relatorios.registrar_venda(id_linha_encontrada, data_str, preco) #Registra a venda no relatório
            except Exception as e_venda:
                print(f"[AVISO] Erro ao registrar venda no relatório: {e_venda}") 
                pass

        except Exception as e:
            msg_erro = str(e)
            print(f"[ERRO] Linha {linha_num}: {msg_erro} -> '{linha_texto_original}'")
            
            relatorios.registrar_erro(msg_erro, id_linha_encontrada or "-", data_str or "-", assento_num if 'assento_num' in locals() else "-") #Registra o erro no relatório
            erros_log.append(f"LINHA {linha_num}: {linha_texto_original} | MOTIVO: {msg_erro}\n") #Adiciona o erro ao log 

    print(f"\n\t RESUMO \n") 
    print(f"Sucessos: {sucessos}") #Contador de reservas bem-sucedidas
    print(f"Falhas:    {len(erros_log)}") #Contador de falhas
    
    if erros_log:
        caminho_log = os.path.join(pasta_do_script, "reservas_nao_realizadas.txt") 
        try:
            with open(caminho_log, 'w', encoding='utf-8') as arquivo_log:
                arquivo_log.write("\n\t RESERVAS NÃO REALIZADAS DURANTE PROCESSAMENTO DE ARQUIVO \n\n")
                arquivo_log.writelines(erros_log)
            print(f"\nO arquivo de falhas do processamento foi salvo em:\n{caminho_log}")
        except:
            print("Erro ao gravar arquivo de log 'reservas_nao_realizadas.txt'.")