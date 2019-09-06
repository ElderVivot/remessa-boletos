def analisaArquivosRemessa(caminho):
    titulos = []
    titulo = []
    with open(caminho, 'rt') as txtfile:
        for linha in txtfile:
            linha = str(linha).replace("\n", "")

            if linha[0] == "1":
                    
                cnpj = linha[8:22]

                nome = linha[22:92].strip()

                vencimento = linha[200:207]

                valor = linha[216:227]

                faturamento_parcela = linha[253:262]

                nosso_numero = linha[262:278]

                #print(cnpj, nome, vencimento, valor, faturamento_parcela, nosso_numero)
                titulo.append(cnpj)
                titulo.append(nome)
                titulo.append(vencimento)
                titulo.append(valor)
                titulo.append(faturamento_parcela)
                titulo.append(nosso_numero)

                titulos.append(titulo[:])

                titulo.clear()
        
    return titulos

