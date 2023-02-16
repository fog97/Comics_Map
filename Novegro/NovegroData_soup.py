from selenium import webdriver
import sys
import logging
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import json
import pprint
import sqlite3
conn = sqlite3.connect("Novegro/Novegro.db")
table_name = 'info'
query = f'Create table if not Exists {table_name} (data,luogo)'
conn.execute(query)
table_name = 'biglietti'
query = f'Create table if not Exists {table_name} (Tipologia,Prezzo,Note)'
conn.execute(query)
conn.commit()

#Download dei dati di novegro
########################################################################################################################

page=requests.get("https://parcoesposizioninovegro.it/biglietti/festival-del-fumetto-web-1giorno-198372-2/")
soup = BeautifulSoup(page.content, "html.parser")
list_projects = soup.find_all("p")

if list_projects[0].text !='Sembra che non riusciamo a trovare la risorsa che cerchi. Forse una ricerca potrebbe aiutare.':
    ## Costo e tipologia dei biglietti
    biglietti=pd.DataFrame(columns=["Tipologia","Prezzo","Note"])
    for nome in list_projects:
        testo=nome.text
        test=testo.split(" ")
        if (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]!="ridotto" and len(test)>7 and test[1]!="gratuito:" :
            tipologia=test[0]+" "+test[1]+" "+test[2]+" "+test[3].replace(":","")
            prezzo=test[4]+" "+test[6]+" "+test[7]
            row=pd.DataFrame([[tipologia,prezzo]],columns=["Tipologia","Prezzo"])
            biglietti=pd.concat([biglietti,row])
        elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]!="ridotto" and test[1]!="gratuito:" :
            tipologia=test[0]+" "+test[2]+" "+test[3]+" "+test[4].replace(":","")
            prezzo=test[5]+" "
            row=pd.DataFrame([[tipologia,prezzo]],columns=["Tipologia","Prezzo"])
            biglietti=pd.concat([biglietti,row])
        elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]=="ridotto" and len(test)>8 and test[1]!="gratuito:" :
            tipologia=test[0]+" "+test[1]+" "+test[2]+" "+test[3]+" "+test[4].replace("*","").replace(":","")
            prezzo=test[5]+"  "+test[7]+"  "+test[8]
            row=pd.DataFrame([[tipologia,prezzo]],columns=["Tipologia","Prezzo"])
            biglietti=pd.concat([biglietti,row])
        elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]=="ridotto" and test[1]!="gratuito:" :
            tipologia=test[0]+" "+test[1]+" "+test[3]+" "+test[3]+" "+test[5].replace("*","").replace(":","")
            prezzo=test[6]
            row=pd.DataFrame([[tipologia,prezzo]],columns=["Tipologia","Prezzo"])
            biglietti=pd.concat([biglietti,row])
        elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]=="gratuito:" :
            tipologia=test[0]+" "+test[1].replace("*","").replace(":","")+" "+test[4]+" "+test[6]+"-"+test[8]+" "+test[9]+" e "+test[12]+" con "+test[14]+" "+test[16].replace("l’","")+"-"+test[19].replace(".","")+ " e accompagnatore"
            prezzo="0"
            row=pd.DataFrame([[tipologia,prezzo]],columns=["Tipologia","Prezzo"])    
            biglietti=pd.concat([biglietti,row])

    biglietti.to_sql('biglietti',conn,if_exists='replace',index=False)



# data e luogo
#indirizzo

page=requests.get("https://parcoesposizioninovegro.it/biglietti/festival-del-fumetto-web-1giorno-198372-2/")
soup = BeautifulSoup(page.content, "html.parser")
list_projects = soup.find_all("p")

luogo=str(list_projects[1]).split(">")[6].replace("<br/","")+str(list_projects[1]).split(">")[7].replace("<br/","")




if list_projects[0].text =='Sembra che non riusciamo a trovare la risorsa che cerchi. Forse una ricerca potrebbe aiutare.':
    data=''
#infoevento
infodict={'data':data,"luogo":luogo}
infodf=pd.DataFrame(infodict,index=[1])
infodf.to_sql('info',conn,if_exists='replace',index=False)



conn.close()



