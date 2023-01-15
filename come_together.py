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

st.markdown("# Come Together ")
st.image(image.imread(path+'copertina.jpg'))


image = Image.open('copertina.jpg')
st.image(image)