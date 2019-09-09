# -*- coding: utf-8 -*-

import os
import datetime
from model_entities.TitulosPagos import TitulosPagos
from model_services.TitulosPagosServices import TitulosPagosServices
import utils.leArquivos as leArquivos
import utils.funcoesUteis as funcoesUteis

def analisaArquivosRemessa(linhas_arquivo, codi_emp):

    lista_linha_retorno = []
    lista_linha_remessa = []

    for linha in linhas_arquivo:
        linha = str(linha)

        try:
            ja_processado_pagamento_anteriormente = linha[356]
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

            if valorPago > 0 or dataPagamento is not None:
                dataPagamento = funcoesUteis.transformaCampoDataParaFormatoBrasileiro(dataPagamento)

                motivo_exclusao = "01"
                linha_retorno = f"2{linha[1:227]}{motivo_exclusao}{linha[230:355]}{valorPago:>12.2f}{dataPagamento:<10}"
                lista_linha_retorno.append(linha_retorno)
                print(linha_retorno)

                linha = f"{linha[0:355]}1"
                lista_linha_remessa.append(linha)
            else:
                linha = f"{linha[0:355]}0"
                lista_linha_remessa.append(linha)

        else: 
            lista_linha_remessa.append(linha[0:355])
        
    return [lista_linha_remessa, lista_linha_retorno]

def processaTitutosPagos():

    pastas = leArquivos.buscaSubpastas("D:\\temp\\REMESSA - NEGATIVAÇÃO\\INCLUSÃO")

    lista_arquivos_retorno = {}
    lista_retorno = []

    for pasta in pastas:

        pasta = str(pasta)
        
        caminho_pasta_dividido = pasta.upper().split('\\')

        if caminho_pasta_dividido.count('SOMA') > 0:
            codi_emp = 1
            print('- Processando arquivos de remessa da SOMA')
        elif caminho_pasta_dividido.count('SOMANDO') > 0:
            codi_emp = 123
            print('- Processando arquivos de remessa da SOMANDO')
        elif caminho_pasta_dividido.count('RESULTE') > 0:
            codi_emp = 338
            print('- Processando arquivos de remessa da RESULTE')
        else:
            codi_emp = 0
            
        for raiz, diretorios, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                print(f"     - Lendo o arquivo {arquivo}")

                caminho_arquivo = os.path.join(raiz,arquivo)

                linhas_arquivo = leArquivos.leTxt(caminho_arquivo)

                analiseArquivoRemessa = analisaArquivosRemessa(linhas_arquivo, codi_emp)

                lista_linha_remessa = analiseArquivoRemessa[0]
                #print(lista_linha_remessa)

                lista_linha_retorno = analiseArquivoRemessa[1]
                #print(lista_linha_retorno)

                lista_retorno.append(lista_linha_retorno[:])

            lista_arquivos_retorno[codi_emp] = lista_retorno[:]
            lista_retorno.clear()

    return lista_arquivos_retorno
            
def geraArquivoRetorno(lista_arquivo_retorno):
    for codi_emp, dados_retorno in lista_arquivo_retorno.items():
        caminho_retorno = 'D:\\temp\REMESSA - NEGATIVAÇÃO\\EXCLUSÃO'

        if codi_emp == 1:
            caminho_retorno = os.path.join(caminho_retorno,'SOMA')
            print('- Gerando arquivos de retorno da SOMA')
        elif codi_emp == 123:
            caminho_retorno = os.path.join(caminho_retorno,'SOMANDO')
            print('- Gerando arquivos de retorno da SOMANDO')
        elif codi_emp == 338:
            caminho_retorno = os.path.join(caminho_retorno,'RESULTE')
            print('- Gerando arquivos de retorno da RESULTE')
        else:
            print(f'- Gerando arquivos de retorno da {codi_emp}')

        dia_e_horario_atual = datetime.datetime.now()

        nome_arquivo = f"{dia_e_horario_atual.strftime('%Y%m%d %H%M')}.txt"
        data_atual = dia_e_horario_atual.strftime('%Y%m%d')

        caminho_retorno = os.path.join(caminho_retorno, nome_arquivo)

        arquivo_retorno = open(caminho_retorno, 'w', encoding='Windows-1252')

        arquivo_retorno.write(f"0{data_atual}00001P0100PP{' '*271}E{' '*60}\n")

        for retorno in dados_retorno:
            for linha_retorno in retorno:

                cnpj = linha_retorno[8:22]

                nome = linha_retorno[22:92].strip()

                vencimento = f"{linha_retorno[206:208]}/{linha_retorno[204:206]}/{linha_retorno[200:204]}"

                valor = f"{linha_retorno[216:225]}.{linha_retorno[225:227]}"
                valor = float(valor)

                faturamento_parcela = int(linha_retorno[253:262])

                nosso_numero = linha_retorno[262:279]

                arquivo_retorno.write(f"{linha_retorno}\n")

        arquivo_retorno.write(f"9000009{' '*287}{' '*60}\n")

        arquivo_retorno.close()

geraArquivoRetorno(processaTitutosPagos())