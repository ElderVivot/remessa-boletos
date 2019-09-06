# -*- coding: utf-8 -*-

import os
from model_entities.TitulosPagos import TitulosPagos
from model_services.TitulosPagosServices import TitulosPagosServices
import utils.leArquivos

def processaTitutosPagos():

    for raiz, diretorios, arquivos in os.walk("D:\\temp\\REMESSA - NEGATIVAÇÃO\\INCLUSÃO"):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz,arquivo)
            caminho_arquivo_dividido = str(caminho_arquivo).upper().split('\\')

            if caminho_arquivo_dividido.count('SOMA') > 0:
                codi_emp = 1
            elif caminho_arquivo_dividido.count('SOMANDO') > 0:
                codi_emp = 123
            elif caminho_arquivo_dividido.count('RESULTE') > 0:
                codi_emp = 2
            else:
                codi_emp = 0

            ainda_tem_pagamentos_em_aberto = 0

            if arquivo.endswith(".TXT"):
            
                with open(caminho_arquivo, 'rt') as txtfile:

                    for linha in txtfile:
                        linha = str(linha).replace("\n", "")

                        if linha[0] == "1":
                                
                            cnpj = linha[8:22]

                            nome = linha[22:92].strip()

                            vencimento = f"{linha[206:208]}/{linha[204:206]}/{linha[200:204]}"

                            valor = f"{linha[216:225]}.{linha[225:227]}"
                            valor = float(valor)

                            faturamento_parcela = int(linha[253:262])

                            nosso_numero = linha[262:279]

                            titulosPagosServices = 
                    



processaTitutosPagos()