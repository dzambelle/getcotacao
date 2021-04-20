#!/usr/bin/python3
# coding=utf-8

import configparser, logging, os

def get_parameter(self,section,item,log=False):
    # Instantiate
    config = configparser.ConfigParser()
    
    # gettrace = getattr(sys, 'gettrace', None)

    # https://stackoverflow.com/questions/29426483/python3-configparser-keyerror-when-run-as-cronjob
    # pra resolver o problea quando executando o py pelo cron
    arquivoini = os.path.join(os.path.dirname(__file__), 'getcotacao.ini')

    config.read(arquivoini)

    value = config[section][item]

    # read values from a section
    # Mesma solucao do cron, mas para o log
    if log == True:
        value = os.path.join(os.path.dirname(__file__), value)

    return value
## End function 