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

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

wd = webdriver.Chrome('chromedriver',options=options)

wd.get("https://parcoesposizioninovegro.it/biglietti/festival-del-fumetto-web-1giorno-198372-2/")

list_projects = wd.find_elements(by=By.CSS_SELECTOR, value="p")

date=list_projects[0].text
date
for nome in list_projects:
    testo=nome.text
    test=testo.split(" ")
    if (test[0]=="Abbonamento" or test[0]=="Ingresso"):
        print(test)


for nome in list_projects:
    testo=nome.text
    test=testo.split(" ")
    if (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]!="ridotto" and len(test)>7 and test[1]!="gratuito:" :
        tipologia=test[0]+" "+test[1]+" "+test[2]+" "+test[3]
        prezzo=test[4]+" "+test[6]+" "+test[7]+" "+test[8]
        print(tipologia,prezzo)
    elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]!="ridotto" and test[1]!="gratuito:" :
        tipologia=test[0]+" "+test[2]+" "+test[3]+" "+test[4]
        prezzo=test[5]+" "+test[6]
        print(tipologia,prezzo)
    elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]=="ridotto" and len(test)>7 and test[1]!="gratuito:" :
        print(test)
    elif (test[0]=="Abbonamento" or test[0]=="Ingresso") and test[1]=="ridotto" and test[1]!="gratuito:" :
        print(test)