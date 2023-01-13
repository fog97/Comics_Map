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

st.markdown("# Novegro comics")

st.markdown("## Biglietti")

biglietti=pd.read_csv(path+"biglietti_novegro.csv",sep=";")
st.write(biglietti.loc[:, ["Tipologia","Prezzo"]])


st.markdown("## Mappa")
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent = "myapp")
location = locator.geocode("Via Novegro 20090 Segrate")
start_lat=location.latitude 
start_lng=location.longitude
dic={"lat":start_lat,"lon":start_lng}
df=pd.DataFrame(dic,index=[1])

map_data=pd.read_csv(path+"map_data.csv",dtype=object, index_col=0)

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
import geopandas
import folium
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




origin=pd.DataFrame({"lon":9.275071955673953,"lat":45.47185532715593,"name":"Esposizioni Novegro"}, index=[0])
import pydeck as pdk
import pandas as pd


# Data from OpenStreetMap, accessed via osmpy

ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/9/9e/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Pin_%E2%80%93_Tourism_%E2%80%93_Light.png"

icon_data = {

    "url": ICON_URL,
    "width": 32,
    "height": 37,
    "anchorY": 'auto',
}


data=origin

data["icon_data"] = None
for i in data.index:
    data["icon_data"][i] = icon_data

data=data[["lat","lon","name","icon_data"]]



view_state = INITIAL_VIEW_STATE

origin_layer = pdk.Layer(
    type="IconLayer",
    data=data,
    get_icon="icon_data",
    get_size=10,
    size_scale=3,
    get_position=["lon", "lat"],
    pickable=True,
)


pdk.Deck(layers=[Nav_Points,origin_layer], map_style='road',initial_view_state=INITIAL_VIEW_STATE, tooltip={"text": "{name}"})

st.markdown("## Presenze")



st.text_input("Nome ", key="eadd")
add_e=st.session_state.eadd


st.text_input("Data Presenza ", key="padd")
add_p=st.session_state.padd

info_dict={"Nome":add_e,"Data":add_p}
infopres=pd.DataFrame(info_dict,index=[1])




col1, col2 = st.columns(2)
with col1:
    if st.button("Aggiungi Presenza"):
        infopres.to_csv(path+"presenze_novegro.csv", mode='a', index = False, header=False)

with col2:
    if st.button("Elimina Presenza"):   
        old=pd.read_csv(path+"presenze_novegro.csv")
        old2=old[(old["Nome"] !=add_e) & (old["Data"] !=add_p)]
        new=pd.DataFrame(columns=["Nome","Data"])
        final=pd.concat([new,old2] , ignore_index=True)
        final.to_csv(path+"presenze_novegro.csv", mode='w', index = False, header=True)
                



if st.button("Vedi Presenze"): 
    presenze=pd.read_csv(path+"presenze_novegro.csv")
    st.write(presenze)


#from git import Repo

#PATH_OF_GIT_REPO = r'path\to\your\project\folder\.git'  # make sure .git folder is properly configured
#COMMIT_MESSAGE = 'comment from python script'

#def git_push():
#    try:
#        repo = Repo(PATH_OF_GIT_REPO)
#        repo.git.add(update=True)
#        repo.index.commit(COMMIT_MESSAGE)
#        origin = repo.remote(name='origin')
#        origin.push()
#    except:
#        print('Some error occured while pushing the code')    

#git_push()