#from programclass.TitulosDao import TitulosDao
#from programclass.ConexaoBanco import DB
#from db.ConexaoBanco import DB
from model_dao.TitulosDao import TitulosDao

teste = TitulosDao()
print(teste.consultaPagamentoTitulo(1, "1234"))