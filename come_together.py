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
from PIL import Image
path='/app/comics_map/'

st.set_page_config(
    page_title="Come Together",
    layout="wide",
    initial_sidebar_state="expanded")

st.header(" _Come Together_ ")

st.image(image.imread(path+'Copertina2.jpg'))

with st.sidebar:
    st.markdown("#### Powered By _Foggy_")
st.sidebar.image(image.imread(path+'profilo.jpg'), use_column_width=True)
