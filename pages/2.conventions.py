import streamlit as st
import matplotlib.image as image
import pandas as pd
import joblib
import geopy
from geopy.distance import distance
import shapefile
from shapely.geometry import Point
from shapely.geometry import shape
import pydeck as pdk
from bs4 import BeautifulSoup
import requests
import sqlite3
st.set_page_config(
    page_title='Convetions',
    layout="wide",
    initial_sidebar_state="expanded"
)

Fiera_Selector='Novegro'
Fiera_Selector= st.selectbox(
    'Seleziona Fiera',
    ('Novegro', 'Torino'))




path=f'./{Fiera_Selector}/'
conn = sqlite3.connect(path+f"{Fiera_Selector}.db")

import streamlit as st



st.header(f" **PAGINA IN COSTRUZIONE** ")



from pymongo import MongoClient

us_name=st.secrets["mongo"]["db_username"]
us_pw=st.secrets["mongo"]["db_pswd"]
cl_name=st.secrets["mongo"]["cluster_name"]

def init_connection():
    return MongoClient(f"mongodb+srv://{us_name}:{us_pw}@{cl_name}.zisso.mongodb.net/test")
client = init_connection()
db = client.PresenzeComics
collection_friends = db.Friends
filter_friends = { 'user': st.session_state.utente }

try:
    friends =collection_friends.find(filter_friends)
    fr=pd.DataFrame(list(friends))
    list_friend=fr.loc[0,"friend"].split(";")
except:
    first_data={'user': st.session_state.utente, 'friend': ''}
    collection_friends.insert_one(first_data)
    friends =collection_friends.find(filter_friends)
    fr=pd.DataFrame(list(friends))
    list_friend=fr.loc[0,"friend"].split(";")

if st.session_state.autenticazione:
    with st.sidebar:
        st.markdown("Powered by : *Foggy.cos*")
 
    from datetime import datetime
    from io import StringIO


    data = st.date_input("Data Presenza",
        datetime.now())
    data = data.strftime("%m/%d/%Y")
    data_def=data

    data_to=''
    piudate = st.checkbox('Inserire più giorni')

    if piudate:
        data_to = st.date_input("Data Fine Presenza",datetime.now())
        data_to = data_to.strftime("%m/%d/%Y")
        
    if data_to!='' and data_to!=data_def:
        data_def=data_def+"-"+data_to


    uploaded_files = st.file_uploader("Carica la foto del tuo cosplay", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()


    import gridfs
    from io import BytesIO

    db = client.PresenzeComics

    #Create an object of GridFs for the above database.
    fs = gridfs.GridFS(db)

    immagine=''
    try:
        with BytesIO(bytes_data) as f:
            contents = f.read()
            st.image(contents, caption='Immagine Caricata')
            immagine=contents
    except NameError:
        immagine=''

        


    add = st.button('Aggiungi')

    if add:
        mydict = { "Nome": st.session_state.utente, "Data": data_def, "Foto":immagine }
        db = client.PresenzeComics
        mycol = db[Fiera_Selector]
        mycol.insert_one(mydict)


    db_name=Fiera_Selector
    db = client.PresenzeComics
    collection = db.db_name
    presenze = pd.DataFrame(list(db[Fiera_Selector].find()))

    #text_pass = st.text_input("Password per Eliminazione",key='1AB') 

    col1, col2,col3,col4 = st.columns((10, 10, 15,10))
    col1.write('Nome')
    col2.write('Data')
    col3.write('Cosplay')
    col4.write('Elimina Presenza')


    for index, row in presenze.iterrows():
        if row['Nome'] in list_friend or row['Nome']==st.session_state.utente:
            col1, col2,col3,col4 = st.columns((10, 10, 15,10))
            col1.write(row['Nome'])
            col2.write(row['Data'])
            if row['Foto']!='':
                col3.image(row['Foto'], width=100)
            else:
                with st.container():
                    col3.write(row['Foto'])   
            button_phold = col4.empty() 
            do_action = button_phold.button(key=index,label="Delete")
            if do_action:
                mydict = {"_id":row["_id"]}
                db = client.PresenzeComics
                mycol = db[Fiera_Selector]
                mycol.delete_one(mydict)
                db = client.PresenzeComics
                collection = db.db_name





    st.markdown("*Refresh della pagina per verificare l'effettiva cancellazione*")



else:
    st.write("Autenticati o registrati per favore")


