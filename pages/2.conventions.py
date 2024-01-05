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


st.header(f" **Convetions** ", divider='rainbow')



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
    with st.expander("Crea la tua Convention", expanded=False):
        titolo=st.text_input("Inserisci il Titolo della Convention : ")

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


        uploaded_files = st.file_uploader("Carica una foto per la tua Convention", accept_multiple_files=True)
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

        location=st.text_input("Inserisci Location : ")
        note=st.text_input("Inserisci eventuali note : ")

        add = st.button('Aggiungi')

        if add:
            mydict = {"Titolo":titolo, "Organizzatore": st.session_state.utente, "Data": data_def, "Foto":immagine,"Note":note ,"Location":location,'Partecipanti':st.session_state.utente+";" }
            db = client.PresenzeComics
            mycol = db["Convention"]
            mycol.insert_one(mydict)


        db = client.PresenzeComics
        presenze = pd.DataFrame(list(db["Convention"].find()))



    with st.expander("Visualizza le Convention tue e dei tuoi amici", expanded=False):
        st.markdown("**Dettagli Convetion**")
        col1, col2,col3,col4,col5,col6,col7,col8 = st.columns((10, 15, 10, 10,10,15,10,10))
        col1.write('Titolo')
        col2.write('Foto')
        col3.write('Organizzatore')
        col4.write('Data')
        col5.write('Location')
        col6.write('Note')
        col7.write('Partecianti')
        col8.write('Elimina Convention')

        
        for index, row in presenze.iterrows():
            if row['Organizzatore'] in list_friend or row['Organizzatore']==st.session_state.utente:
                col1, col2,col3,col4,col5,col6,col7,col8 = st.columns((10, 15, 10, 10,10,15,10,10))
                col1.write(row['Titolo'])
                if row['Foto']!='':
                    col2.image(row['Foto'], width=100)
                else:
                    with st.container():
                        col2.write(row['Foto'])   
                col3.write(row['Organizzatore'])
                col4.write(row['Data'])
                col5.write(row['Location'])
                col6.write(row['Note'])
                col7.write(row['Partecipanti'].replace(";",","))
                button_phold = col8.empty() 
                do_action = button_phold.button(key=index,label="Delete")
                if do_action and row['Organizzatore']==st.session_state.utente:
                    mydict = {"_id":row["_id"]}
                    db = client.PresenzeComics
                    mycol = db["Convention"]
                    mycol.delete_one(mydict)
                    db = client.PresenzeComics


        st.markdown("*Refresh della pagina per verificare l'effettiva cancellazione*")

    lista_conv=[]
    partecipazioni_keys = pd.DataFrame(list(db["Convention"].find()))
    partecipazioni_keys["Nome_Conv"]=partecipazioni_keys["Organizzatore"]+' -- '+partecipazioni_keys["Titolo"]
    
    st.markdown("**Conferma Partecipazione**")
    st.write("Selezione la Convention")
    Conv_Selector=partecipazioni_keys["Nome_Conv"].unique()[0]
    Conv_Selector= st.selectbox('Convention Disponibili',partecipazioni_keys["Nome_Conv"].unique())

    col1, col2 = st.columns((10, 10))
    with col1:
        do_action = st.button(key='1a',label="Conferma Presenza")
        if do_action:
            db = client.PresenzeComics
            mycol = db["Convention"]
            db = client.PresenzeComics
            filter={"_id":partecipazioni_keys[partecipazioni_keys.Nome_Conv==Conv_Selector]["_id"][0]}
            partecipanti=partecipazioni_keys[partecipazioni_keys.Nome_Conv==Conv_Selector]["Partecipanti"][0]+st.session_state.utente+';'
            newvalues={ "$set": { 'Partecipanti': partecipanti } }
            mycol.update_one(filter, newvalues)
    with col2:
        do_action = st.button(key='1b',label="Elimina Presenza")
        if do_action:
            db = client.PresenzeComics
            mycol = db["Convention"]
            db = client.PresenzeComics
            filter={"_id":partecipazioni_keys[partecipazioni_keys.Nome_Conv==Conv_Selector]["_id"][0]}
            partecipanti=partecipazioni_keys[partecipazioni_keys.Nome_Conv==Conv_Selector]["Partecipanti"][0].replace(st.session_state.utente+';',"")
            newvalues={ "$set": { 'Partecipanti': partecipanti } }
            mycol.update_one(filter, newvalues)   


    if  st.session_state.utente in partecipazioni_keys[partecipazioni_keys.Nome_Conv==Conv_Selector]["Partecipanti"][0].split(";"):
        st.markdown("**Aggiungi Note o Foto**")

        uploaded_files = st.file_uploader(key='Foto_appendice',label="Carica una Foto", accept_multiple_files=True)
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

        note_appendice_text=st.text_input(key='Note_appendice',label="Inserisci nota : ")




        add = st.button(key='Nota_Aggiunta',label='Aggiungi')

        if add:
            mydict = { "Autore": st.session_state.utente, "Nota": note_appendice_text, "Foto":immagine, "Id_Conv": partecipazioni_keys[partecipazioni_keys.Nome_Conv==Conv_Selector]["_id"][0]}
            db = client.PresenzeComics
            mycol = db["Appendice_Convention"]
            mycol.insert_one(mydict)









        with st.expander("**Note dai Partecipanti**", expanded=False):
            Note_appendice = pd.DataFrame(list(db["Appendice_Convention"].find()))
            col1, col2,col3,col4 = st.columns((10, 15, 15,10))
            col1.write('Autore')
            col2.write('Foto')
            col3.write('Nota')
            col4.write('Elimina Nota')    
            for index, row in Note_appendice.iterrows():        
                col1, col2,col3,col4 = st.columns((10, 15, 15,10))
                col1.write(row['Autore'])
                if row['Foto']!='':
                    col2.image(row['Foto'], width=100)
                else:
                    with st.container():
                        col2.write(row['Foto'])   
                col3.write(row['Nota'])
                button_phold = col4.empty() 
                do_action = button_phold.button(key='appendice_delete'+str(index),label="Delete")
                if do_action and row['Autore']==st.session_state.utente:
                    mydict = {"_id":row["_id"]}
                    db = client.PresenzeComics
                    mycol = db["Appendice_Convention"]
                    mycol.delete_one(mydict)
                    db = client.PresenzeComics


else:
    st.write("Autenticati o registrati per favore")


