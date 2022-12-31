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

st.map(df)

st.markdown("## Presenze")

col1, col2 = st.columns(2)
from datetime import datetime
with col1:
    st.text_input("Nome ", key="eadd")
    add_e=st.session_state.eadd

with col2:
    st.text_input("Data Presenza ", key="padd")
    add_p=st.session_state.padd

    infopres={"Nome":add_e,"Data":add_p}
    df_pres=pd.DataFrame(infopres,index=[1])

    with open("presenze.csv", "a") as file1:
        # Writing data to a file
        file1.write(df_pres)



presenze=pd.read_csv(path+"presenze.csv")
st.write(presenze.loc[:, ["Nome","Data"]])
