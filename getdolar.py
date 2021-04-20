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

def get_dolar(self,_host, _database, _user, _password):
    try:
        ### Primeiro pego o valor do ultimo dolar na base de dados
        ## Conexao
        connect_mysql = MysqlPython(host=_host, user=_user, password=_password, database=_database)

        ## Select com mais de uma condição
        sql_query = 'SELECT date(CotacaoMoedaDt) as CotacaoMoedaDt FROM CotacaoMoeda Order by CotacaoMoedaDt desc Limit 1'
        cotacaomoeda = Dados('',connect_mysql.select_advanced(sql_query),0,'')
    
        ### depois abrir um laco e capturar todas as cotacoes entre a data acima e hoje
        data_atual = datetime.date.today()

        if cotacaomoeda.data[0] < data_atual:
            cotacaomoeda.data[0] = cotacaomoeda.data[0] + datetime.timedelta(days=1)
            cotacaomoeda.acao = 'insert'

        # creating an instance of list       
        lista = [] 
        
        # Abertura do laco que ira buscar as cotacoes entre a data do BD e hoje
        while (cotacaomoeda.data[0] <= data_atual):
            # arruma as datas
            strdia = '0'+str(cotacaomoeda.data[0].day)
            strdia = strdia[-2:]
            strmes = '0'+str(cotacaomoeda.data[0].month)
            strmes = strmes[-2:]
            strano = str(cotacaomoeda.data[0].year)
            # Pegar o json
            url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=%27" + strmes + "-" + strdia + "-" + strano + "%27&$top=100&$format=json"
            req = urllib.request.Request(url)

            ## parsing response
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            
            icount=0
            ucount=0
            rowsaffected=0

            if len(cont['value']) > 0:
                # appending instances of my object to the list 
                lista.append( Dados('USD', cont['value'][0]['dataHoraCotacao'], cont['value'][0]['cotacaoVenda'], '') )

            cotacaomoeda.data[0] = cotacaomoeda.data[0] + datetime.timedelta(days=1)

        result = '0 Registros Dolar Alterados.'

        for obj in lista:
            data = datetime.datetime.strptime(obj.data,'%Y-%m-%d %H:%M:%S.%f')
            if ((data.date() < data_atual) or (cotacaomoeda.ticker == 'insert')):
                ## Se a data for anterior, fazer insert
                ## Insert
                connect_mysql.insert('CotacaoMoeda', CotacaoMoedaSimbolo='USD', CotacaoMoedaDt=obj.data, CotacaoMoedaValor=obj.valor)
                icount = icount + 1
            else:
                ## Se a data for hoje, fazer update
                ## Update
                conditional_query = 'CotacaoMoedaDt = %s'
                rowsaffected = connect_mysql.update('CotacaoMoeda', conditional_query, obj.data, CotacaoMoedaValor=obj.valor, CotacaoMoedaDt=obj.data)
                ucount = ucount + rowsaffected
            
            result = str(icount)+" Registro(s) Dolar Inserido(s) / " + str(ucount)+" Registro(s) Dolar Alterado(s)"

        #  Limpeza de objetos
        del lista
        del cotacaomoeda
        del connect_mysql

        return result
    except Exception as e:
        logging.error("Erro no getdolar: {0}\n".format(str(e)), exc_info=True)
        return "Houve um erro e os dados das cotacoes de Dolar nao foram atualizados"
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