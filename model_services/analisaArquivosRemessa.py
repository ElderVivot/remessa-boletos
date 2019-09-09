def analisaArquivosRemessa(linhas_arquivo, codi_emp):

    lista_linha_retorno = []
    lista_linha_remessa = []

    for linha in linhas_arquivo:
        linha = str(linha)

        try:
            ja_processado_pagamento_anteriormente = linha[356]
        except Exception:
            ja_processado_pagamento_anteriormente = "0"

        # somente os titulos e os que ainda não foram pagos
        if linha[0] == "1" and ja_processado_pagamento_anteriormente == "0":
                
            faturamento_parcela = str(int(linha[253:262]))

            tituloPago = TitulosPagosServices()
            dadosTituloPago = TitulosPagosServices.analisaTitulosPagosFaturamento(codi_emp, faturamento_parcela)

            if dadosTituloPago[0] > 0 or dadosTituloPago[1] is not None:
                motivo_exclusao = "01"
                linha_retorno = f"2{linha[1:227]}{motivo_exclusao}{linha[230:]}"
                lista_linha_retorno.append(linha_retorno)

                linha = f"{linha}1"
                lista_linha_remessa.append(linha)
            else:
                linha = f"{linha}0"
                lista_linha_remessa.append(linha)

        else: 
            lista_linha_remessa.append(linha)
        
    return [lista_linha_remessa, lista_linha_retorno]

