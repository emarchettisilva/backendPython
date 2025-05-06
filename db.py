# db.py
import psycopg2
import logging
from config import DB_CONFIG
import enum

class Mode(enum.Enum):
    SELECT = 1
    BEGIN = 2
    DEFAULT = 3
    COMMIT = 4
    

"""
    Executa uma comando SQL com tratamento de erros e
    controle de transação. 
    retorna os resultados (se houver).

    Args:
        sql (str): A consulta SQL com placeholders.
        params (tuple ou dict): Os parâmetros a serem substituídos na consulta.
        mode: pode ser uma das 4 constantes
          BEGIN -> só conecta ou inicia uma transaçao explicita)
          DEFAULT -> conecta se não houver conexão e commita se not inTransactio
          COMMIT -> só comita (fim de transação explicita)
          SELECT -> espera retornar dados
                 
    Returns:
        list: Uma lista de resultados da consulta 
        (se for um SELECT), ou None em caso de erro ou outras consultas.
    """
class Db:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.inTransaction = False
        self.erro = None
        self.qtdeAtu = None

    def execSql(self, sql, params=None, mode=Mode.DEFAULT):
        results = None
        try:
            if mode == Mode.BEGIN:
                self.inTransaction = True
                sql = "BEGIN;\n" + sql
                
            if not self.conn:    
                self.conn = self._get_connection()
                self.cursor = self.conn.cursor()
            
            full_sql = self.cursor.mogrify(sql, params).decode("utf-8")
            print("Mostrando SQL")
            print(full_sql)

            self.cursor.execute(sql, params)
            self.qtdAtu += self.cursor.rowcount
            
            if mode == Mode.SELECT:
                results = self.cursor.fetchall()
            else:
                if self.inTransaction:
                    results = ''
                else:
                    results = {"mensagem": "Atualização realizada com sucesso",
                               "qtdAtu": self.qtdAtu}

            if mode == Mode.COMMIT:
                self.conn.commit()
                self.inTransaction = False
                results = {"mensagem": "Transação realizada com sucesso",
                           "qtdAtu": self.qtdAtu}

            if not self.inTransaction:
                self._finalizar()

        except Exception as e:
            results = {"mensagem": f"{e}"}
            self.erro = results
            logging.error(results)
            if self.conn:
                self.conn.rollback()
            self._finalizar()
        finally:
            # sempre retorna um dict ou string vazia
            return results 

    def getErro(self):
        return self.erro

    def _finalizar(self):
        self.conn.commit()
        if self.conn:
            self.cursor.close()
            self.conn.close()
        self.cursor = None
        self.conn = None

    def _get_connection(self):
        self.qtdAtu = 0
        return psycopg2.connect(**DB_CONFIG)

