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
    page_title='Fiere',
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



st.header(f" **Comics {Fiera_Selector}** ", divider='rainbow')



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
        st.markdown("Powered by : **Foggy.cos**")
        st.markdown("_NB : Refresh della pagina per rendere effettive le modifiche_")
 
    with st.container():
        st.markdown("## Mappa")


        map_data=pd.read_csv(path+"map_data.csv", keep_default_na=False,index_col=0)
        map_data['lat'] = map_data['lat'].astype(float)
        map_data['lon'] = map_data['lon'].astype(float)

        #['Parcheggio', 'Bus', 'Train', 'Metro']

        bus = st.checkbox('Bus')
        bus_l=''
        if bus:
            bus_l="Bus"

        parcheggio = st.checkbox('Parcheggio')
        parcheggio_l=''
        if parcheggio:
            parcheggio_l="Parcheggio"

        treno = st.checkbox('Treno')
        treno_l=''
        if treno:
            treno_l="Train"

        metro = st.checkbox('Metro')
        metro_l=''
        if metro:
            metro_l="Metro"

        list_values=[metro_l,parcheggio_l,treno_l,bus_l]
        map_data=map_data[map_data.Classe.isin(list_values)]

        import pandas as pd
        import numpy as np
        import pydeck as pdk

        Bus_icon = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Bus_Stop_%E2%80%93_Transportation_%E2%80%93_Light.png"

        Bus_icon_data = {

            "url": Bus_icon,
            "width": 32,
            "height": 37,
            "anchorY": 'auto',
        }

        Metro_icon = "https://upload.wikimedia.org/wikipedia/commons/5/57/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Subway_%E2%80%93_Transportation_%E2%80%93_Light.png"

        Metro_icon_data = {

            "url": Metro_icon,
            "width": 32,
            "height": 37,
            "anchorY": 'auto',
        }

        Train_icon = "https://upload.wikimedia.org/wikipedia/commons/1/16/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Train_%E2%80%93_Transportation_%E2%80%93_Light.png"

        Train_icon_data = {

            "url": Train_icon,
            "width": 32,
            "height": 37,
            "anchorY": 'auto',
        }

        Parcheggi_icon = "https://upload.wikimedia.org/wikipedia/commons/c/c7/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Parking_%E2%80%93_Transportation_%E2%80%93_Light.png"

        Parcheggi_icon_data = {

            "url": Parcheggi_icon,
            "width": 32,
            "height": 37,
            "anchorY": 'auto',
        }

        icon_data = []
        for index,row in map_data.iterrows():
            if row["Classe"]=="Parcheggio":
                icon_data.append(Parcheggi_icon_data)
            elif row["Classe"]=="Bus":
                icon_data.append(Bus_icon_data)
            elif row["Classe"]=="Train":
                icon_data.append(Train_icon_data)
            elif row["Classe"]=="Metro":
                icon_data.append(Metro_icon_data)   

        map_data["icon_data"]=icon_data

        Nav_Points = pdk.Layer(
            type="IconLayer",
            data=map_data,
            get_icon="icon_data",
            get_size=10,
            size_scale=3,
            get_position=["lon", "lat"],
            pickable=True,
        )


        import pandas as pd


        import matplotlib.pyplot as plt
        import pydeck as pdk

        import pandas as pd

        import matplotlib.pyplot as plt
        import pydeck as pdk
        
        map_data=pd.read_csv(path+"map_data.csv", keep_default_na=False,index_col=0)
        map_data['lat'] = map_data['lat'].astype(float)
        map_data['lon'] = map_data['lon'].astype(float)
        Latitudine_iniziale=map_data.iloc[0,1]
        Longitudine_iniziale=map_data.iloc[0,2]
        
        INITIAL_VIEW_STATE = pdk.ViewState(
        latitude=Latitudine_iniziale, 
        longitude=Longitudine_iniziale, 
        zoom=10,
        max_zoom=16,
        pitch=45,
        bearing=0
        )

        origin_url = "https://upload.wikimedia.org/wikipedia/commons/9/9e/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Pin_%E2%80%93_Tourism_%E2%80%93_Light.png"

        origin_icon = {

            "url": origin_url,
            "width": 32,
            "height": 37,
            "anchorY": 'auto',
        }


        origin=pd.DataFrame({"lon":Longitudine_iniziale, "lat":Latitudine_iniziale ,"name":f"Esposizioni {Fiera_Selector}"}, index=[0])
        import pydeck as pdk
        import pandas as pd

        icon_data = []
        for index,row in origin.iterrows():
            if index==0:
                icon_data.append(origin_icon)

        origin["icon_data"]=icon_data




        data=origin[["lat","lon","name","icon_data"]]

        view_state = INITIAL_VIEW_STATE

        origin_layer = pdk.Layer(
            type="IconLayer",
            data=data,
            get_icon="icon_data",
            get_size=15,
            size_scale=3,
            get_position=["lon", "lat"],
            pickable=True,
        )











        st.pydeck_chart(pdk.Deck(layers=[Nav_Points,origin_layer], map_style='road',initial_view_state=INITIAL_VIEW_STATE, tooltip={"text": "{name}"}))

    st.markdown("# Presenze")



    #Uso mongoDB
    from pymongo import MongoClient

    us_name=st.secrets["mongo"]["db_username"]
    us_pw=st.secrets["mongo"]["db_pswd"]
    cl_name=st.secrets["mongo"]["cluster_name"]



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
            if do_action and row['Organizzatore']==st.session_state.utente:
                mydict = {"_id":row["_id"]}
                db = client.PresenzeComics
                mycol = db[Fiera_Selector]
                mycol.delete_one(mydict)
                db = client.PresenzeComics
                collection = db.db_name





    st.markdown("*Refresh della pagina per verificare l'effettiva cancellazione*")



else:
    st.write("Autenticati o registrati per favore")


