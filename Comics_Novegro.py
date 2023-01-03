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

path='/app/comics_map/'

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

#st.map(df)

import pandas as pd
import numpy as np
import pydeck as pdk

chart_data = pd.read_csv(path+"locations_tomap.csv")

chart_data=chart_data[["lat","lon"]]



INITIAL_VIEW_STATE=pydeck.ViewState(
  latitude=start_lat,
  longitude=start_lng,
  zoom=11,
  max_zoom=16,
  pitch=45,
  bearing=0
)

ScatterplotLayer=[
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color=[180, 0, 200, 140],
            get_radius=200,
        )]


st.pydeck_chart(pydeck.Deck(
    layers=[ScatterplotLayer],
    initial_view_state=INITIAL_VIEW_STATE))


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
