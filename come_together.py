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

st.markdown("# Come Together ")

st.image(path+"copertina.jpg")