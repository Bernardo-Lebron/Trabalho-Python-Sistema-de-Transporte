import datetime
import consultarassentos
import os 
import relatorios

def processar_arquivo_reservas(linhas, relatorio_vendas_list, nome_arquivo="reservas.txt"):
    """
    Lê um arquivo de reservas e processa cada linha.
    Formato esperado: CIDADE_DESTINO, HORARIO, DATA, ASSENTO
    """
    
    pasta_do_script = os.path.dirname(os.path.abspath(__file__))
    
    caminho_completo = os.path.join(pasta_do_script, nome_arquivo)

    print(f"\n\t Processando arquivo ")
    if not os.path.exists(caminho_completo) and pasta_do_script == '':
         caminho_completo = os.path.join(os.getcwd(), nome_arquivo)

    print(f"Procurando em: {caminho_completo}")
    
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.readlines()
    except FileNotFoundError:
        print(f"\nERRO CRÍTICO: O arquivo '{nome_arquivo}' não foi encontrado!")
        print(f"O Python tentou ler neste local: {caminho_completo}")
        print("Dica: Verifique se o nome do arquivo está correto e se ele está na pasta do projeto.")
        return

    erros_log = []
    sucessos = 0
    linha_num = 0
    hoje = datetime.date.today()

    print(f"Arquivo encontrado! Processando {len(conteudo)} linhas...\n")

    for linha_texto in conteudo:
        linha_num += 1
        linha_texto_original = linha_texto.strip()
        
        if not linha_texto_original:
            continue

        id_linha_encontrada = None
        data_str = None
        assento_num = None
        dados_linha = None
        
        try:
            partes = linha_texto_original.split(',')
            
            if len(partes) != 4:
                raise ValueError("Formato incorreto (esperado: Cidade, Horário, Data, Assento)")
            
            cidade_destino = partes[0].strip().title()
            horario = partes[1].strip()
            data_str = partes[2].strip()
            
            try:
                assento_num = int(partes[3].strip())
            except ValueError:
                raise ValueError("Número do assento inválido")
            
            for id_linha, dados in linhas.items():
                if dados[1] == cidade_destino and dados[2] == horario:
                    id_linha_encontrada = id_linha
                    dados_linha = dados
                    break
            
            if not id_linha_encontrada:
                raise ValueError(f"Linha não encontrada para {cidade_destino} às {horario}")
            
            try:
                data_viagem = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Data inválida (use dd/mm/aaaa)")

            if data_viagem < hoje:
                raise ValueError("Data já passou")
            
            if data_viagem > hoje + datetime.timedelta(days=30):
                raise ValueError("Data excede 30 dias")
                
            if data_viagem == hoje:
                agora = datetime.datetime.now()
                try:
                    hh, mm = map(int, horario.split(':'))
                    if hh < agora.hour or (hh == agora.hour and mm <= agora.minute):
                        raise ValueError("Ônibus já partiu hoje")
                except:
                    pass 

            if isinstance(dados_linha, tuple):
                dados_linha = list(dados_linha)
                linhas[id_linha_encontrada] = dados_linha

            onibus = consultarassentos.pegar_ou_criar_onibus_por_data(linhas, id_linha_encontrada, data_str)

            if not (1 <= assento_num <= 20):
                raise ValueError(f"Assento {assento_num} inexistente")

            if onibus.get(assento_num) == False:  
                raise ValueError(f"Assento {assento_num} ocupado")
            

            onibus[assento_num] = False 
            sucessos += 1
            print(f"[OK] Linha {id_linha_encontrada} | {data_str} | Assento {assento_num}")

            try:
                preco = dados_linha[3] 
                relatorios.registrar_venda(id_linha_encontrada, data_str, preco)
            except Exception as e_venda:
                print(f"[AVISO] Erro ao registrar venda no relatório: {e_venda}")
                pass

        except Exception as e:
            msg_erro = str(e)
            print(f"[ERRO] Linha {linha_num}: {msg_erro} -> '{linha_texto_original}'")
            
            relatorios.registrar_erro(msg_erro, id_linha_encontrada or "-", data_str or "-", assento_num if 'assento_num' in locals() else "-")
            erros_log.append(f"LINHA {linha_num}: {linha_texto_original} | MOTIVO: {msg_erro}\n")

    print(f"\n\t RESUMO \n")
    print(f"Sucessos: {sucessos}")
    print(f"Falhas:    {len(erros_log)}")
    
    if erros_log:
        caminho_log = os.path.join(pasta_do_script, "reservas_nao_realizadas.txt")
        try:
            with open(caminho_log, 'w', encoding='utf-8') as arquivo_log:
                arquivo_log.write("\n\t RESERVAS NÃO REALIZADAS DURANTE PROCESSAMENTO DE ARQUIVO \n\n")
                arquivo_log.writelines(erros_log)
            print(f"\nO arquivo de falhas do processamento foi salvo em:\n{caminho_log}")
        except:
            print("Erro ao gravar arquivo de log 'reservas_nao_realizadas.txt'.")