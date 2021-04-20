#!/usr/bin/python3
# coding=utf-8 


from mysql_python import MysqlPython
import datetime, urllib.request, json,logging

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

def get_cotacaous(self,_host, _database, _user, _password):

    try:
        ## Conexao
        connect_mysql = MysqlPython(host=_host, user=_user, password=_password, database=_database)

        ## Select com mais de uma condição
        sql_query = 'SELECT PapelPapel FROM vwCarteiras where Carteira COLLATE utf8mb4_0900_ai_ci = %s'
        rows = connect_mysql.select_advanced(sql_query, ('Carteira','Stocks'))

        # creating an instance of list       
        lista = [] 
        
        for row in rows:
            # Pegar o json
            url = "https://query2.finance.yahoo.com/v7/finance/options/" + row
            req = urllib.request.Request(url)

            ## parsing response
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            
            # verifica se tem retorno com o conteudo desejado
            if len(cont['optionChain']['result']) > 0:
                # appending instances of sql result to the list 
                lista.append( Dados(row, datetime.datetime.today(), cont['optionChain']['result'][0]['quote']['regularMarketPrice'],'') )
                # jsonData.seats[jsonData.seats.length-1].countryid
        
        ucount = 0
        rowsupdated = 0
        result = '0 Registros US Alterados.'

        #Agora gravar no banco de dados
        for objlista in lista:
            ## Update
            conditional_query = 'PapelPapel = %s'
            rowsupdated = connect_mysql.update('Papeis', conditional_query, objlista.ticker, PapelUltimoPreco=objlista.valor, PapelUltimoPrecoData=objlista.data)
            ucount = ucount + rowsupdated
            result = str(ucount)+" Registro(s) US Alterado(s)"

        #  Limpeza de objetos
        del lista
        del cont
        del rows
        del connect_mysql

        return result
    except Exception as e:
        logging.error("Erro no getcotacaous: {0}\n".format(str(e)), exc_info=True)
        return "Houve um erro e os dados das acoes americas nao foram atualizados"