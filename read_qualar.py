# -*- coding: utf-8 -*-

# carlagama@ua.pt
# 2015.02.25

"""
to be used with data downloaded from http://qualar.apambiente.pt/
"Dados de todas as estações para um poluente num dado ano"
(one file per pollutant and per year for all the network sites)
"""

import os, csv
import pandas as pd
import datetime as dt

def _sub(a):
    virgulas_para_pontos = lambda x:float(x.replace(',','.'))
    try:
        return virgulas_para_pontos(a)
    except ValueError:
        return float('NaN')

def raios(directory, filename):
    """
    lê um determinado ficheiro da qualar
    devolve o resultado como uma DataFrame
    """
    i=[]
    conc=[]
     
    with open(os.path.join(os.getcwd(), directory, filename), 'rb') as f:
        header = f.readline()[:-2] #para eliminar '\t\n' (ficheiros APA...)
        header = header.split("\t")
        ncol = len(header)
        f.readline()
        f.readline()

        reader = csv.reader(f, dialect='excel-tab')
        for row in reader:            
            i.append(dt.datetime.strptime(row[0], "%Y/%m/%d %H:%M:%S")) #2007/01/01 00:00:00
            conc.append(tuple([_sub(element) for element in row[1:ncol]]))
            
    return pd.DataFrame(conc, index=i, columns=header[1:])

def ler_qualar(directory, lista_ficheiros):
    """
    usar quando se pretende juntar vários anos de dados da qualar
    (um ficheiro por ano de dados)
    devolve o resultado como uma única DataFrame
    """ 
    df_pol = raios(directory, lista_ficheiros[0])
    for f in lista_ficheiros[1:]:
        df = raios(directory, f)
        try:
            df_pol = pd.concat([df_pol, df])
        except ValueError:
            print "problemas (resolvidos) no ficheiro "+ f
            df_pol = pd.concat([df_pol, df.T.drop_duplicates().T])
    return df_pol


d_qualar = '2003-2013'
path_dados_qualar = os.path.join(os.getcwd(),d_qualar)
ficheiros_O3 = [i for i in os.listdir(path_dados_qualar) if i.startswith('_O3')]
ficheiros_PM = [i for i in os.listdir(path_dados_qualar) if i.startswith('_PM')]

df_O3 = ler_qualar(d_qualar, ficheiros_O3)
df_PM = ler_qualar(d_qualar, ficheiros_PM)
