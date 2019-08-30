from model_dao.TitulosDao import TitulosDao
from model_entities.TitulosPagos import TitulosPagos
from utils import funcoesUteis

class TitulosPagosServices:

    def __init__(self):
        self.__valor_pago = 0
        
    def analisaTitulosPagosFaturamento(self, codi_emp, i_faturamento_e_parcela):
        self.__titulosDao = TitulosDao()

        self.__valor_pago = self.__titulosDao.consultaPagamentoTitulo(codi_emp, i_faturamento_e_parcela)
        self.__valor_pago = funcoesUteis.trataCampoDecimal(self.__valor_pago)
        return self.__valor_pago

        

