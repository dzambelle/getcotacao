#!/usr/bin/python3
# coding=utf-8

from mysql_python import MysqlPython
import datetime, urllib.request, json, os, ssl,logging

#  codigo abaixo depende também de uma alteração no arquivo /usr/lib/ssl/openssl.conf
#  https://askubuntu.com/questions/1233186/ubuntu-20-04-how-to-set-lower-ssl-security-level
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# Python3 code here creating class
# https://www.geeksforgeeks.org/how-to-create-a-list-of-object-in-python-class/
class Dados: 
    # constructor
    def __init__(self, ticker, data, valor): 
        self.ticker = ticker 
        self.data = data
        self.valor = valor
    # Close
    def close(self):
        print('Close Dados')
    # destructor
    def __del__(self):
        self.close()
## Fim da classe dados

def get_tesouro(self,_host, _database, _user, _password):
    try:
        ### Primeiro pego o valor do ultimo dolar na base de dados
        ## Conexao
        connect_mysql = MysqlPython(host=_host, user=_user, password=_password, database=_database)

        ## Select com mais de uma condição
        sql_query = 'SELECT PapelID, PapelNome FROM Papeis where TipoInvID = %s and PapelSetor = %s'
        rv = connect_mysql.select_advanced(sql_query, ('TipoInvID', '3'), ('PapelSetor', 'Tesouro'))

        json_sql = []
        content = {}
        for result in rv:
            content = {'PapelID': result[0], 'PapelNome': result[1]}
            json_sql.append(content)

        # Pegar o json do tesouro direto
        url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
        response = urllib.request.urlopen(url)
        json_site = json.loads(response.read())

        # creating an instance of list       
        lista = [] 
        # Abertura do laco que ira buscar cada resultado do select dentro do json do site do tesouro
        for objsql in json_sql:
            for objsite in json_site['response']['TrsrBdTradgList']:
                if objsql['PapelNome'] == objsite['TrsrBd']['nm']:
                    # appending instances of my object to the list 
                    lista.append( Dados(objsql['PapelID'], datetime.datetime.today(), objsite['TrsrBd']['untrRedVal']) )
        
        ucount = 0
        rowsupdated = 0
        result = '0 Registros Tesouro Alterados.'

        #Agora gravar no banco de dados
        for objlista in lista:
            ## Update
            conditional_query = 'PapelID = %s'
            rowsupdated = connect_mysql.update('Papeis', conditional_query, objlista.ticker, PapelUltimoPreco=objlista.valor, PapelUltimoPrecoData=objlista.data)
            ucount = ucount + rowsupdated
            
            result = str(ucount)+" Registro(s) Tesouro Alterado(s)"

        #  Limpeza de objetos
        del lista
        del json_site
        del json_sql
        del response
        del content
        del connect_mysql

        #  Retorno para o Main
        return result

    except Exception as e:
        logging.error("Erro no gettesouro: {0}\n".format(str(e)), exc_info=True)
        return "Houve um erro e os dados do Tesouro nao foram atualizados"
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