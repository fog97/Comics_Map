from selenium import webdriver
import sys
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import json
import pprint
#Download dei dati di novegro
########################################################################################################################
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

wd = webdriver.Chrome('chromedriver',options=options)

wd.get("https://parcoesposizioninovegro.it/biglietti/festival-del-fumetto-web-1giorno-198372-2/")
list_projects = wd.find_elements(by=By.CSS_SELECTOR, value="p")
if len(list_projects)>0:
    ## Costo e tipologia dei biglietti
    biglietti=pd.DataFrame(columns=["Tipologia","Prezzo"])
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

    biglietti.to_csv("C:/Users/lucaf/OneDrive/Desktop/Esercizi/Comics_Map/Novegro/biglietti_novegro.csv",sep=";")

else:
    biglietti=pd.DataFrame(columns=["Tipologia","Prezzo"])
    biglietti.to_csv("C:/Users/lucaf/OneDrive/Desktop/Esercizi/Comics_Map/Novegro/biglietti_novegro.csv",sep=";")
