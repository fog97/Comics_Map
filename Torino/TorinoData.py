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
import sqlite3
conn = sqlite3.connect("Torino/Torino.db")
table_name = 'info'
query = f'Create table if not Exists {table_name} (data,luogo)'
conn.execute(query)
table_name = 'biglietti'
query = f'Create table if not Exists {table_name} (Tipologia,Prezzo,Note)'
conn.execute(query)
conn.commit()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

wd = webdriver.Chrome('chromedriver',options=options)

wd.get("https://torinocomics.com/")

list_projects = wd.find_elements(by=By.CLASS_NAME, value="text-center")

if len(list_projects)>0:
    testo=list_projects[0].text
    testo=testo.split(" ")

    import datetime
    today = datetime.date.today()
    year = today.year
    print(year)
    data=testo[7]+" - "+testo[9]+" "+testo[10]+" "+str(year)
    data
    search_place = wd.find_elements(by=By.CSS_SELECTOR, value="p")
    testo= search_place[len(search_place)-1].text
    testo
    testo=testo.split("|")
    luogo=testo[0].replace("© ","")+" "+testo[1].replace(",","")
    #infoevento
    infodict={'data':data,"luogo":luogo}
    infodf=pd.DataFrame(infodict,index=[1])
    infodf.head()
    infodf.to_sql('info',conn,if_exists='replace',index=False)
else:
    pass


wd.get("https://torinocomics.com/82454/info-pratiche")
list_projects = wd.find_elements(by=By.CSS_SELECTOR, value="p")


if list_projects[0].text!='':
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
else:  
    pass


conn.close()

