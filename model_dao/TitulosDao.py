from db.ConexaoBanco import DB
import pyodbc
import decimal

class TitulosDao:

    def __init__(self):
        self._DB = DB()
        self._connection = self._DB.getConnection()
        self._cursor = None

    def consultaPagamentoTitulo(self, codi_emp, i_faturamento_e_parcela):
        try:
            self._cursor = self._connection.cursor()
            self._cursor.execute("SELECT SUM(COALESCE(rec.valor_recebido, 0)) AS valor_recebido,"
                                f"       MAX(rec.data_recebimento) as data_recebimento, "
                                f"       SUM( COALESCE(par.valor_original, 0) - COALESCE(par.valor_desconto, 0) - COALESCE(par.valor_desconto_adimplente, 0) ) AS valor_parcela, "
                                f"       MAX(CASE WHEN par.vencimento <> par.vencimento_original THEN 'alterado' ELSE 'nao_alterado' END) AS alterado_venc, "
                                f"       MAX(CASE WHEN rec.valor_refaturado > 0 OR rec.valor_reparcelado > 0 THEN 'renegociado' ELSE 'nao_renegociado' END) AS renegociado "
                                f"  FROM bethadba.hrrecebimento AS rec "
                                f"       INNER JOIN bethadba.hrfaturamento_parcela AS par"
                                f"            ON    par.codi_emp = rec.codi_emp "
                                f"              AND par.i_faturamento = rec.i_faturamento "
                                f"              AND par.i_parcela = rec.i_parcela "
                                f"       LEFT OUTER JOIN bethadba.hrrenegociacao_faturamento AS renfat "
                                f"                 ON    renfat.codi_emp = par.codi_emp "
                                f"                   AND renfat.i_faturamento_destino = par.i_faturamento "
                                f"                   AND renfat.i_parcela_destino = par.i_parcela "
                                f"       LEFT OUTER JOIN bethadba.hrrenegociacao AS ren "
                                f"                 ON    ren.codi_emp = renfat.codi_emp "
                                f"                   AND ren.i_renegociacao = renfat.i_renegociacao "
                                f"       LEFT OUTER JOIN bethadba.hrfaturamento_parcela AS par_ant "
                                f"                 ON    par_ant.codi_emp = renfat.codi_emp "
                                f"                   AND par_ant.i_faturamento = renfat.i_faturamento_origem "
                                f"                   AND par_ant.i_parcela = renfat.i_parcela_origem "
                                f" WHERE rec.codi_emp = {codi_emp}"
                                f"   AND CASE WHEN ren.i_renegociacao IS NOT NULL THEN STRING(renfat.i_faturamento_origem) || STRING(renfat.i_parcela_origem) "
                                f"            ELSE STRING(par.i_faturamento) || STRING(par.i_parcela) "
                                f"       END = {i_faturamento_e_parcela}")
            self._data = self._cursor.fetchall()
            return self._data
        except Exception as e:
            print(f"Erro ao executar a consulta. O erro é: {e}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            self._DB.closeConnection()
    