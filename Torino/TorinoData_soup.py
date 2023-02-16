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
conn = sqlite3.connect("Torino/Torino.db")
table_name = 'info'
query = f'Create table if not Exists {table_name} (data,luogo)'
conn.execute(query)
table_name = 'biglietti'
query = f'Create table if not Exists {table_name} (Tipologia,Prezzo,Note)'
conn.execute(query)
conn.commit()

page=requests.get("https://torinocomics.com/")
soup = BeautifulSoup(page.content, "html.parser")



if len(soup)>0:
    all_soup = soup.find_all("div", {"class": "text-center"})
    list_data=str(all_soup[0]).split(">")[len(str(all_soup[0]).split(">"))-2].replace("."," ").split(" ")
    data=list_data[7]+" - "+list_data[9]+" "+list_data[10]+" "+list_data[11]
    soup = BeautifulSoup(page.content, "html.parser")
    all_soup = soup.find_all("p")
    list_luogo=str(all_soup).split(">")[len(str(all_soup).split(">"))-2].replace(".","|").split("|")
    luogo=list_luogo[0].replace("Â© ","")+" "+list_luogo[1].replace(",","")
    infodict={'data':data,"luogo":luogo}
    infodf=pd.DataFrame(infodict,index=[1])
    infodf.to_sql('info',conn,if_exists='replace',index=False)
else:
    pass

page=requests.get("https://torinocomics.com/82454/info-pratiche")
soup = BeautifulSoup(page.content, "html.parser")
all_soup = soup.find_all("p")


if all_soup[0].text!='':
    ## Costo e tipologia dei biglietti
    biglietti=pd.DataFrame(columns=["Tipologia","Prezzo","Note"])
    for nome in all_soup:
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

