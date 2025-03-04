import pandas as pd 
import numpy as np
import requests 

def desacum(X):
    a = [X[0]]
    for i in range(len(X)-1):
        a.append(X[i+1]-X[i])
    return a

def baixar_arquivo(url, endereco):
    resposta = requests.get(url)
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
        print("Download finalizado. Arquivo salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()

link = 'https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/5d1f3f2a7f43ed55a26ac467d468219f_HIST_PAINEL_COVIDBR_23mai2020.xlsx'
file = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/att.xlsx'
baixar_arquivo(link,file)
 
df = pd.read_excel(file,header = 0)
df = df.fillna(-1)

A = df[(df.codmun == -1)&(df.data == '2020-05-23')]
estados = A[['regiao','estado']].values
path_out = 'C:/Users/ravellys/Documents/GitHub/COVID-19-Brasil/COVID-19-Brasil/data/DADOS/'

for i in estados:
    regiao, estado = i
    df2 = df[(df.regiao == regiao)&(df.estado == estado)&(df.codmun == -1)]

    df_ = df2[['regiao','estado','data','casosAcumulado','obitosAcumulado']]
    df_.columns = ['regiao','estado','DateRep','cum-Cases','cum-Deaths']
    df_['Cases'] = desacum(df_['cum-Cases'].values)
    df_['Deaths'] = desacum(df_['cum-Deaths'].values)
    
    if i[1] == -1:
        s_e = 'Brazil'
    else: 
        s_e = i[1]    
    
    df_.to_csv(path_out+ "COVID-19 "+ s_e + ".csv", sep = ";",index = False)


   
