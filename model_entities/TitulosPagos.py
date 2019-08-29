class TitulosPagos:

    def __init__(self, inscricaoCliente, nomeCliente, emissao, vencimento, faturamentoParcela, nossoNumero):
        self.__inscricaoCliente = inscricaoCliente
        self.__nomeCliente = nomeCliente
        self.__emissao = emissao
        self.__vencimento = vencimento
        self.__faturamentoParcela = faturamentoParcela
        self.__nossoNumero = nossoNumero

    @property
    def getFaturamentoParcela(self):
        return self.__faturamentoParcela