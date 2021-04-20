#!/usr/bin/python3
# coding=utf-8

from mysql_python import MysqlPython        ## Classe para acesso ao banco de dados
from readfile import get_parameter          ## Classe para ler arquivo ini de parametrizacao
import datetime, urllib.request, json, logging       ## classes para Manipular data, HTTP Request e arquivo json

## Posicao Inicial e final para parse na pagina html do resultado da consulta do BCB
_ini = int(get_parameter('ini','IPCA','pos_ini'))
_fim = int(get_parameter('ini','IPCA','pos_fim'))

# Python3 code here creating class
# https://www.geeksforgeeks.org/how-to-create-a-list-of-object-in-python-class/
class Dados: 
    # constructor
    def __init__(self, ticker, data, valor, acao): 
        self.ticker = ticker 
        self.data = data
        self.valor = valor
        self.acao = acao
    # Close
    def close(self):
        print('Close Dados')
    # destructor
    def __del__(self):
        self.close()
## Fim da classe dados

def get_ipca(self,_host, _database, _user, _password):
    try:
        ## Conexao
        connect_mysql = MysqlPython(host=_host, user=_user, password=_password, database=_database)

        ## Select com mais de uma condição
        sql_query = 'select t.TransacoesID, t.TransacoesData from Transacoes t inner join TransacoesRF trf on t.TransacoesID = trf.TransacoesID where trf.TransacoesRFIndexador = %s;'
        rv = connect_mysql.select_advanced(sql_query, ('TransacoesRFIndexador', 'IPCA'))

        # creating an instance of list       
        lista = [] 

        if len(rv)>0:
            json_sql = []
            content = {}
            for result in rv:
                content = {'TransacoesID': result[0], 'TransacoesData': result[1]}
                json_sql.append(content)
   
            # Abertura do laco que ira buscar as cotacoes entre a data do BD e hoje
            for objsql in json_sql:
                data = objsql['TransacoesData']
                # arruma as datas
                i_strmes = '0' + str(data.month)
                i_strmes = i_strmes[-2:]
                i_strano = str(data.year)
                f_strmes = '0' + str(datetime.date.today().month - 1) # no site do BCB sempre tem que ser mes anterior
                f_strmes = f_strmes[-2:]
                f_strano = str(datetime.date.today().year)
                
                # Prepara o POST
                url = "https://www3.bcb.gov.br/CALCIDADAO/publico/corrigirPorIndice.do?method=corrigirPorIndice"
                data = "aba=1&selIndice=00433IPCA&dataInicial=" + i_strmes + "%2F" + i_strano + "&dataFinal=" + f_strmes + "%2F" + f_strano + "&valorCorrecao=1%2C00&idIndice=&nomeIndicePeriodo="
                data = data.encode('ascii') # data should be bytes
                req = urllib.request.Request(url, data)
                
                with urllib.request.urlopen(req) as response:
                    result = response.read()
                    result = str(result)
                    valor = result[_ini:_fim]
                    if valor.replace(',','',1).isdigit():
                        valor = valor.replace(',','.')
                        # appending instances of my object to the list 
                        lista.append( Dados(objsql['TransacoesID'], datetime.datetime.today(), valor, '') )

        # Contador para o return
        ucount = 0
        rowsupdated = 0
        result = '0 Registros IPCA Alterados.'

        # Laço pra o update
        for obj in lista:
            ## Update
            conditional_query = 'TransacoesID = %s'
            rowsupdated = connect_mysql.update('TransacoesRF', conditional_query, obj.ticker, TransacoesRFTaxaPeriodo=obj.valor, TransacoesRFLastUpdate=obj.data)
            ucount = ucount + rowsupdated
            
            result = str(ucount)+" Registro(s) IPCA Alterado(s)"

        #  Limpeza de objetos
        del lista
        del json_sql
        del response
        del content
        del connect_mysql

        #  Retorno para o Main
        return result
    except Exception as e:
        logging.error("Erro no getipca: {0}\n".format(str(e)), exc_info=True)
        return "Houve um erro e os dados da IPCA nao foram atualizados"
    ### FIM

    ## Select com mais de uma condição
    #  sql_query = 'SELECT CotacaoMoedaDt FROM CotacaoMoeda where CotacaoMoedaID = %s and CotacaoMoedaSimbolo = %s'
    #  result = connect_mysql.select_advanced(sql_query, ('CotacaoMoedaID', '317'),('CotacaoMoedaSimbolo','USD'))
    #  return result

    ## Select com uma condição apenas
    #  conditional_query = 'CotacaoMoedaID = %s '
    #  result = connect_mysql.select('CotacaoMoeda', conditional_query, 'CotacaoMoedaID', 'CotacaoMoedaValor', CotacaoMoedaID='317')
    #  print(result)

    ## Insert
    #  result = connect_msyql.insert('car', car_make='ford', car_model='escort', car_year='2005')
    #  print(result)

    ## Update
    #  conditional_query = 'car_make = %s'
    #  result = connect_mysql.update('car_table', conditional_query, 'nissan', car_model='escort', car_year='2005')
    #  print(result)

    ## Delete
    #  conditional_query = 'car_make = %s'
    #  result = connect_mysql.delete('car', conditional_query, 'nissan')
    #  print(result)
## End da Funcao