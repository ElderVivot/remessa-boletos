# coding: utf-8

import pyodbc

user='EXTERNO'
password='EXTERNO'
host='Contabil'
port='2638'

class DB(object):

    connection = None

    @staticmethod
    def getConnection():
        if DB.connection is None:
            try:
                DB.connection = pyodbc.connect(DSN=host,UID=user,PWD=password,PORT=port)
                print('- Conexão com a Domínio realizada com sucesso.')
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
        return DB.connection

    @staticmethod
    def closeConnection():
        if DB.connection is not None:
            try:
                DB.connection.close()
                print('- Conexão fechada com sucesso')
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")