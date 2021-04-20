#!/usr/bin/python3
# coding=utf-8

import logging , datetime                   ## Para gerar arquivo de log 
from mysql_python import MysqlPython        ## Classe Conexao Generica com o Banco MySQL
from readfile import get_parameter          ## Classe para ler arquivo ini de parametrizacao
from getdolar import get_dolar              ## Funcao para inserir o dolar no BD
from gettesouro import get_tesouro          ## Funcao para inserir o valor do Tesouro especifico no BD
from getselic import get_selic              ## Funcao para inserir a SELIC no BD
from getipca import get_ipca                ## Funcao para inserir o IPCA no periodo no BD
from getcotacaobr import get_cotacaobr      ## Funcao para inserir Acoes e FII no BD
from getcotacaous import get_cotacaous      ## Funcao para inserir Stocks/ETF/REIT no BD

def main():
    # logging
    # em modo debug o log fica em : /home/<usuario>/.vscode/extensions
    logging.basicConfig(filename=get_parameter('ini','LOG','logfile',True), level=logging.DEBUG)
    logging.info('Inicio em: ' + str(datetime.datetime.today()))

    try:
        ## arquivo INI com os dados de conexao que será usado em todas as chamadas
        _host = get_parameter('ini','MySQL','dbserver')
        _user = get_parameter('ini','MySQL','dbuser')
        _password = get_parameter('ini','MySQL','dbpwd')
        _database = get_parameter('ini','MySQL','dbname')

        ## Chamada do get_dolar - OK
        result = get_dolar('getcotacao', _host, _database, _user, _password)
        logging.info(result)
        # print(result)

        ## Chamada do get_tesouro - OK
        result = get_tesouro('getcotacao', _host, _database, _user, _password)
        logging.info(result)
        # print(result)

        ## Chamada do get_selic - OK
        result = get_selic('getcotacao', _host, _database, _user, _password)
        logging.info(result)
        # print(result)

        ## Chamada do get_ipca - OK
        result = get_ipca('getcotacao', _host, _database, _user, _password)
        logging.info(result)
        # print(result)

        ## Chamada do get_b3 - OK
        result = get_cotacaobr('getcotacao', _host, _database, _user, _password)
        logging.info(result)
        # print(result)

        ## Chamada do get_stocks - OK
        result = get_cotacaous('getcotacao', _host, _database, _user, _password)
        logging.info(result)
        # print(result)

        logging.info('Fim em: ' + str(datetime.datetime.today()))

    except Exception as e:
        logging.error("Erro no getcotacao: {0}\n".format(str(e)), exc_info=True)
if __name__ == '__main__':
    main()
### FIM