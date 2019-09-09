from db.ConexaoBanco import DB
import pyodbc

class TitulosDao:

    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None

    def consultaPagamentoTitulo(self, codi_emp, i_faturamento_e_parcela):
        try:
            self._cursor = self._connection.cursor()
            self._cursor.execute("SELECT SUM(COALESCE(rec.valor_recebido, 0) - COALESCE(rec.valor_refaturado, 0) - COALESCE(rec.valor_reparcelado, 0) - COALESCE(rec.valor_quitado, 0)) AS valor_recebido,"
                                f"       MAX(rec.data_recebimento) as data_recebimento"
                                f"  FROM bethadba.hrrecebimento AS rec "
                                f" WHERE rec.codi_emp = {codi_emp}"
                                f"   AND STRING(rec.i_faturamento) || STRING(rec.i_parcela) = {i_faturamento_e_parcela}")
            self._data = self._cursor.fetchall()
            return self._data
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
    