# coding: utf-8

import pyodbc

user='EXTERNO'
password='EXTERNO'
host='Contabil'
port='2638'

class Connection:

    connection = None

    @staticmethod
    def getConnection():
        if Connection.connection is None:
            try:
                Connection.connection = pyodbc.connect(DSN=host,UID=user,PWD=password,PORT=port)
                print('- Conexão com a Domínio realizada com sucesso.')
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
        return Connection.connection

    @staticmethod
    def closeConnection():
        if Connection.connection is not None:
            try:
                Connection.connection.close()
                print('- Conexão fechada com sucesso')
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")
        #return Connection.connection