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


map_data=pd.read_csv(path+"map_data.csv", keep_default_na=False,index_col=0)
map_data['lat'] = map_data['lat'].astype(float)
map_data['lon'] = map_data['lon'].astype(float)

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
    get_size=10,
    size_scale=3,
    get_position=["lon", "lat"],
    pickable=True,
)











st.pydeck_chart(pdk.Deck(layers=[Nav_Points,origin_layer], map_style='road',initial_view_state=INITIAL_VIEW_STATE, tooltip={"text": "{name}"}))

st.markdown("# Presenze")




col0, col1= st.columns(2)

nome = col0.text_input('Nome' )
data = col1.text_input('Data' )

run = st.button('Submit')
                

if "mdf" not in st.session_state:
    st.session_state.mdf = pd.DataFrame(columns=['Nome', 'Data'])
dizionario = {nome:data}
df_new = pd.DataFrame({'Nome': list(dizionario.values()), 'Data': list(dizionario.keys())})
   
        
if run:
    st.session_state.mdf = pd.concat([st.session_state.mdf, df_new], axis=0)

st.write(st.session_state.mdf)