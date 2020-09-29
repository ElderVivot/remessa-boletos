# -*- coding: utf-8 -*-

import os
import datetime
from model_entities.TitulosPagos import TitulosPagos
from model_services.TitulosPagosServices import TitulosPagosServices
import utils.leArquivos as leArquivos
import utils.funcoesUteis as funcoesUteis

absPath = os.path.dirname(os.path.abspath(__file__))

caminho_base_remessa = os.path.join(absPath, 'INCLUSÃO')
caminho_base_retorno = os.path.join(absPath, 'EXCLUSÃO')

def identificaEmpresaPeloNomeCaminho(caminho, texto):
    caminho_pasta_dividido = caminho.upper().split('\\')

    if caminho_pasta_dividido.count('SOMA') > 0:
        codi_emp = 1
        print(f'{texto} da SOMA')
    elif caminho_pasta_dividido.count('SOMANDO') > 0:
        codi_emp = 123
        print(f'{texto} da SOMANDO')
    elif caminho_pasta_dividido.count('SOMANDO UNIPESSOAL') > 0:
        codi_emp = 1965
        print(f'{texto} da SOMANDO UNIPESSOAL')
    elif caminho_pasta_dividido.count('RESULTE') > 0:
        codi_emp = 20
        print(f'{texto} da RESULTE')
    else:
        codi_emp = 0

    return codi_emp

def analisaArquivosRemessa(linhas_arquivo, codi_emp):

    lista_linha_retorno = []
    lista_linha_remessa = []

    for linha in linhas_arquivo:
        linha = str(linha)

        try:
            ja_processado_pagamento_anteriormente = linha[355]
            if ja_processado_pagamento_anteriormente == " ":
                ja_processado_pagamento_anteriormente = "0"
        except Exception:
            ja_processado_pagamento_anteriormente = "0"

        # somente os titulos e os que ainda não foram pagos
        if linha[0] == "1" and ja_processado_pagamento_anteriormente == "0":
                
            faturamento_parcela = str(int(linha[253:262]))

            tituloPago = TitulosPagosServices()
            dadosTituloPago = tituloPago.analisaTitulosPagosFaturamento(codi_emp, faturamento_parcela)

            valorPago = dadosTituloPago[0]
            dataPagamento = dadosTituloPago[1]
            valorParcela = dadosTituloPago[2]
            alteradoVenc = dadosTituloPago[3]
            renegociado = dadosTituloPago[4]

            if ( dataPagamento is not None and valorPago >= valorParcela ) or ( alteradoVenc == 'alterado' or renegociado == 'renegociado' ):
                dataPagamento = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(dataPagamento)

                motivo_exclusao = "01"
                if renegociado == 'renegociado':
                    motivo_exclusao = "02"
                if alteradoVenc == 'alterado':
                    motivo_exclusao = "08"
                    
                linha_retorno = f"2{linha[1:227]}{motivo_exclusao}{linha[229:355]}{valorPago:>14.2f}{dataPagamento:<10}{valorParcela:>14.2f}"
                lista_linha_retorno.append(linha_retorno)
                #print(linha_retorno)

                linha = f"{linha[0:355]}1"
                lista_linha_remessa.append(linha)
            else:
                linha = f"{linha[0:355]}0"
                lista_linha_remessa.append(linha)

        else: 
            lista_linha_remessa.append(linha[0:356])
        
    return [lista_linha_remessa, lista_linha_retorno]

def processaTitutosPagos():

    pastas = leArquivos.buscaSubpastas(caminho_base_remessa)

    lista_arquivos_retorno = {}
    lista_retorno = []

    lista_arquivos_remessa = {}

    print('\n- ETAPA 1: Leitura dos arquivos de remessa')

    for pasta in pastas:

        pasta = str(pasta)
        
        codi_emp = identificaEmpresaPeloNomeCaminho(pasta, '    - Lendo arquivos de remessa')
            
        for raiz, diretorios, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                if arquivo.upper().endswith('.TXT'):

                    print(f"        - Lendo o arquivo {arquivo}")

                    caminho_arquivo = os.path.join(raiz,arquivo)

                    linhas_arquivo = leArquivos.leTxt(caminho_arquivo)

                    analiseArquivoRemessa = analisaArquivosRemessa(linhas_arquivo, codi_emp)

                    lista_linha_remessa = analiseArquivoRemessa[0]
                    lista_arquivos_remessa[caminho_arquivo] = lista_linha_remessa[:]

                    lista_linha_retorno = analiseArquivoRemessa[1]
                    lista_retorno.append(lista_linha_retorno[:])
                else:
                    continue

            lista_arquivos_retorno[codi_emp] = lista_retorno[:]
            lista_retorno.clear()

    return [lista_arquivos_retorno, lista_arquivos_remessa]

def pegaUltimoSequencialRemessa(*pastasLeitura):
    
    maior = 0

    for pastas in pastasLeitura:

        arquivos = leArquivos.buscaArquivosEmPasta(pastas, buscarSubpastas=False)

        for arquivo in arquivos:
            with open(arquivo, 'rt') as txtfile:
                for linha in txtfile:
                    if linha[0] == '0':
                        maior_atual = int(linha[9:15])
                        if maior < maior_atual:
                            maior = maior_atual
    
    return maior
            
def geraArquivoRetorno(lista_arquivo_retorno):

    print('\n- ETAPA 2: Gerando arquivo de retorno')

    for codi_emp, dados_retorno in lista_arquivo_retorno.items():
        caminho_retorno = caminho_base_retorno

        if codi_emp == 1:
            caminho_retorno = os.path.join(caminho_retorno,'SOMA')
            print('    - Gerando arquivos de retorno da SOMA')
        elif codi_emp == 123:
            caminho_retorno = os.path.join(caminho_retorno,'SOMANDO')
            print('    - Gerando arquivos de retorno da SOMANDO')
        elif codi_emp == 1965:
            caminho_retorno = os.path.join(caminho_retorno,'SOMANDO UNIPESSOAL')
            print('    - Gerando arquivos de retorno da SOMANDO UNIPESSOAL')
        elif codi_emp == 20:
            caminho_retorno = os.path.join(caminho_retorno,'RESULTE')
            print('    - Gerando arquivos de retorno da RESULTE')
        else:
            print(f'    - Gerando arquivos de retorno da {codi_emp}')

        # subtituiu pois preciso procurar nas pastas de inclusão e exclusão o sequencial
        caminho_remessa = caminho_retorno.replace('EXCLUSÃO', 'INCLUSÃO')

        ultimo_sequencial = pegaUltimoSequencialRemessa(caminho_retorno, caminho_remessa)
        # print(ultimo_sequencial)
        ultimo_sequencial += 1
        #print(ultimo_sequencial)

        dia_e_horario_atual = datetime.datetime.now()

        nome_arquivo = f"{dia_e_horario_atual.strftime('%Y%m%d %H%M')}.txt"
        nome_arquivo_excel = f"{dia_e_horario_atual.strftime('%Y%m%d %H%M')}.csv"
        data_atual = dia_e_horario_atual.strftime('%Y%m%d')

        caminho_retorno_excel = os.path.join(caminho_retorno, nome_arquivo_excel)
        caminho_retorno = os.path.join(caminho_retorno, nome_arquivo)
        
        arquivo_retorno = open(caminho_retorno, 'w', encoding='Windows-1252')
        arquivo_retorno_excel = open(caminho_retorno_excel, 'w', encoding='Windows-1252')

        arquivo_retorno.write(f"0{data_atual}{ultimo_sequencial:0>6d}P0100PP{' '*271}E{' '*61}\n")
        arquivo_retorno_excel.write("Seq. Faturamento Parcela;CNPJ;Nome;Vencimento;Data Pagamento;Valor Gerado na Remessa;Valor Total Parcela;Valor Total Pago;Nosso Numero\n")

        qtd_registros = 0
        for retorno in dados_retorno:
            if len(retorno) > 0:
                for linha_retorno in retorno:

                    cnpj = f"'{linha_retorno[8:22]}"

                    nome = linha_retorno[22:92].strip()

                    vencimento = f"{linha_retorno[206:208]}/{linha_retorno[204:206]}/{linha_retorno[200:204]}"

                    valor_remessa = f"{linha_retorno[216:225]}.{linha_retorno[225:227]}"
                    valor_remessa = float(valor_remessa)

                    faturamento_parcela = int(linha_retorno[253:262])

                    nosso_numero = f"'{linha_retorno[262:278]}"

                    valor_pago = float(linha_retorno[355:369].strip())

                    data_pagamento = linha_retorno[369:380]

                    valor_parcela = float(linha_retorno[380:394].strip())

                    qtd_registros += 1

                    arquivo_retorno.write(f"{linha_retorno[0]}{qtd_registros:0>6d}{linha_retorno[7:355]}\n")

                    arquivo_retorno_excel.write(f"{faturamento_parcela};{cnpj};{nome};{vencimento};{data_pagamento};{valor_remessa};{valor_parcela};{valor_pago};{nosso_numero}\n")

        arquivo_retorno.write(f"9{qtd_registros:0>6d}{' '*287}{' '*61}\n")

        arquivo_retorno.close()
        arquivo_retorno_excel.close()

        if qtd_registros == 0:
            os.remove(caminho_retorno)
            os.remove(caminho_retorno_excel)
            print(f"        - Não há nenhum pagamento realizado após o processamento do último arquivo.")

def modificaRemessa(lista_arquivo_remessa):

    print('\n- ETAPA 3: Atualizando arquivo de remessa.')

    for arquivo, linhas in lista_arquivo_remessa.items():

        identificaEmpresaPeloNomeCaminho(arquivo, '    - Atualizando arquivos de remessa')

        arquivo_saida = open(arquivo, 'w', encoding='Windows-1252')
        for linha in linhas:
            arquivo_saida.write(f'{linha}\n')
        arquivo_saida.close()

processamentoTitulosPagos = processaTitutosPagos()

#print(processamentoTitulosPagos[1])

geraArquivoRetorno(processamentoTitulosPagos[0])
modificaRemessa(processamentoTitulosPagos[1])

print('\n- Processo finalizado, aperte qualquer tecla pra sair.')
os.system('pause > nul')
