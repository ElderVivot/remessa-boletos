from model_dao.TitulosDao import TitulosDao
from model_entities.TitulosPagos import TitulosPagos
from utils import funcoesUteis

class TitulosPagosServices:

    def __init__(self):
        self.__valorPago = 0
        self.__dataPagamento = None
        self.__valorParcela = 0
        
    def analisaTitulosPagosFaturamento(self, codi_emp, i_faturamento_e_parcela):
        self.__titulosDao = TitulosDao()

        try:
            self.__dados_titulo = self.__titulosDao.consultaPagamentoTitulo(codi_emp, i_faturamento_e_parcela)

            self.__valorPago = funcoesUteis.trataCampoDecimal(self.__dados_titulo[0][0])
            self.__dataPagamento = funcoesUteis.retornaCampoComoData(self.__dados_titulo[0][1],2)
            self.__valorParcela = funcoesUteis.trataCampoDecimal(self.__dados_titulo[0][2])
            self.__alteradoVenc = self.__dados_titulo[0][3]
            self.__renegociado = self.__dados_titulo[0][4]
        except Exception as e:
            print(e)

        #return self.__dados_titulo
        return [self.__valorPago,self.__dataPagamento,self.__valorParcela,self.__alteradoVenc,self.__renegociado]

        

