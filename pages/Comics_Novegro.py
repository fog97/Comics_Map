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

path='/app/comics_map/Novegro/'

import streamlit as st

st.set_page_config(
    page_title="Novegro comics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header(" _Comics Novegro_ ")

with st.sidebar:
    st.markdown("#### Powered By _Foggy_")
st.sidebar.image(image.imread('/app/comics_map/profilo.jpg'), width=300)

with st.container():
    st.markdown("## Info")
    biglietti=pd.read_csv(path+"biglietti_novegro.csv",sep=";")
    info=pd.read_csv(path+"info_novegro.csv",sep=";")
    col1, col2 = st.columns((10, 10))
    col1.write('Date')
    col2.write('Indirizzo')
    for index, row in info.iterrows():
        col1, col2 = st.columns((10, 10))
        if len(biglietti)>0:
            col1.write(row['data'])
        else:
            st.markdown("* Date non dipsonibili*")
        col2.write(row['luogo'])  

with st.container():
    st.markdown("## Biglietti")
    #st.write(biglietti.loc[:, ["Tipologia","Prezzo"]])
    if len(biglietti)>0: 
        col1, col2 = st.columns((10, 10))
        col1.write('Tipologia')
        col2.write('Prezzo (€)')
        for index, row in biglietti.iterrows():
            col1, col2 = st.columns((10, 10))
            col1.write(row['Tipologia'])
            col2.write(row['Prezzo'])
    else:
        st.markdown("* Biglietteria non dipsonibile*")

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

    from geopy.geocoders import Nominatim
    locator = Nominatim(user_agent = "myapp")
    location = locator.geocode("Via Novegro 20090 Segrate")
    start_lat=location.latitude 
    start_lng=location.longitude
    dic={"lat":start_lat,"lon":start_lng,"name":"Esposizioni Novegro"}
    origin=pd.DataFrame(dic,index=[1])

    import pandas as pd

    import matplotlib.pyplot as plt
    import pydeck as pdk
    INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=45.47185532715593, 
    longitude=9.275071955673953,
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


    origin=pd.DataFrame({"lon":9.275071955673953,"lat":45.47185532715593,"name":"Esposizioni Novegro"}, index=[0])
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


# Al punto di interesse vicino



import geopy.distance

origin_lat=45.47185532715593
orining_lon=9.275071955673953

map_data["Distance"]=""

for index,row in map_data.iterrows():
  distance=round(geopy.distance.geodesic((row["lat"],row["lon"]), (origin_lat,orining_lon)).km,3)
  map_data.loc[index,"Distance"]=distance

restricted_db=pd.DataFrame(columns=map_data.columns)
for classe in map_data["Classe"].unique():
  temp=map_data[map_data.Classe==classe].sort_values(by="Distance",ascending=True)
  restricted_db=pd.concat([restricted_db,temp.head()])


import networkx as nx
import osmnx as ox
from IPython.display import IFrame
import streamlit.components.v1 as components

import pandas as pd
restricted_db=pd.read_csv("restricted_db.csv", keep_default_na=False,index_col=0)
restricted_db['lat'] = restricted_db['lat'].astype(float)
restricted_db['lon'] = restricted_db['lon'].astype(float)


restricted_db2=restricted_db[restricted_db.Classe.isin(list_values)]


if len(set(list_values))>1:
    st.markdown("# Indicazioni Stradali")
    col1, col2,col3 = st.columns((10, 10, 15))
    col1.write('Tipo')
    col2.write('Nome')
    col3.write('Mostra Indicazioni')

    for index, row in restricted_db2.iterrows():
        col1, col2,col3 = st.columns((10, 10, 15))
        col1.write(row['Classe'])
        col2.write(row['name'])
        button_phold = col3.empty()
        chiave=str(index)+"a"
        do_action = button_phold.button(key=chiave,label="Info")
        if do_action:
            temp=row['Classe']
            p=open(path+f"mappa_novegro_{temp}_{index}.html")
            components.html(p.read())








st.markdown("# Presenze")



#Uso mongoDB
from pymongo import MongoClient

us_name=st.secrets["mongo"]["db_username"]
us_pw=st.secrets["mongo"]["db_pswd"]
cl_name=st.secrets["mongo"]["cluster_name"]


@st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return MongoClient(f"mongodb+srv://{us_name}:{us_pw}@{cl_name}.zisso.mongodb.net/test")


col0, col1= st.columns(2)

nome = col0.text_input('Nome' )

st.text_input("Password ", key="password")
input_pas=st.session_state.password

from pymongo import MongoClient
import pandas as pd
def init_connection():
    return MongoClient(f"mongodb+srv://{us_name}:{us_pw}@{cl_name}.zisso.mongodb.net/test")
client = init_connection()
import gridfs
from io import BytesIO
db = client.PresenzeComics
fs = gridfs.GridFS(db)
collection = db.Novegro 
passwords = pd.DataFrame(list(collection.find()))
try:
    passwords_list = passwords['Password'].tolist()
except KeyError:
    passwords_list = []

if input_pas not in passwords_list and input_pas!=''  :
    st.write("Buona Password ✓")
elif input_pas in passwords_list:
    st.write("Password Usata")
    del(input_pas)
else:
    pass



st.markdown("*La password serve per eliminare la presenza*")


from datetime import datetime
from io import StringIO


data = st.date_input("Data Presenza",
    datetime.now())
data = data.strftime("%m/%d/%Y")
data_def=data
data_to=''
with st.expander("Inserire più giorni"):
    data_to = st.date_input("Data Fine Presenza",
        datetime.now())
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
    mydict = { "Nome": nome, "Data": data_def, "Foto":immagine,"Password":input_pas }
    db = client.PresenzeComics
    mycol = db["Novegro"]
    mycol.insert_one(mydict)


 
db = client.PresenzeComics
collection = db.Novegro 
presenze = pd.DataFrame(list(collection.find()))

text_pass = st.text_input("Password per Eliminazione",key='1AB') 

col1, col2,col3,col4 = st.columns((10, 10, 15,10))
col1.write('Nome')
col2.write('Data')
col3.write('Cosplay')
col4.write('Elimina Presenza')

for index, row in presenze.iterrows():
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
        if text_pass==row["Password"]:
            mydict = {"_id":row["_id"]}
            db = client.PresenzeComics
            mycol = db["Novegro"]
            mycol.delete_one(mydict)
            db = client.PresenzeComics
            collection = db.Novegro 
            presenze = pd.DataFrame(list(collection.find()))
        else:
            st.write("Password Errata")





st.markdown("*Refresh della pagina per verificare l'effettiva cancellazione*")



