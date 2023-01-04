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

#st.map(df)

import pandas as pd
import numpy as np
import pydeck as pdk


INITIAL_VIEW_STATE = pdk.ViewState(
  latitude=45.47185532715593, 
  longitude=9.275071955673953,
  zoom=11,
  max_zoom=16,
  pitch=45,
  bearing=0
)


origin=pd.DataFrame({"lon":9.275071955673953,"lat":45.47185532715593}, index=[0])
Origin_layer = pdk.Layer(
    'ScatterplotLayer',
    origin,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=100,
    get_color='[39, 71, 245,140]',
    pickable=True)


train2=pd.read_csv(path+"train_latlon.csv")
train2["lat"]=train2["lat"].apply(lambda x : float(x))
train2["lon"]=train2["lon"].apply(lambda x : float(x))
Train_Layer = pdk.Layer(
    'ScatterplotLayer',
    train2,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=50,
    get_color='[20, 232, 62, 140]',
    pickable=True)

metro2=pd.read_csv(path+"metro_latlon.csv")
metro2["lat"]=metro2["lat"].apply(lambda x : float(x))
metro2["lon"]=metro2["lon"].apply(lambda x : float(x))
Metro_Layer = pdk.Layer(
    'ScatterplotLayer',
    metro2,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=50,
    get_color='[225, 232, 21, 140]',
    pickable=True)

bus2=pd.read_csv(path+"bus_latlon.csv")
bus2["lat"]=bus2["lat"].apply(lambda x : float(x))
bus2["lon"]=bus2["lon"].apply(lambda x : float(x))
Bus_Layer = pdk.Layer(
    'ScatterplotLayer',
    bus2,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=50,
    get_color='[180, 0, 200, 140]',
    pickable=True)

st.pydeck_chart(pdk.Deck(
    layers=[Origin_layer,Bus_Layer,Metro_Layer,Train_Layer],
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