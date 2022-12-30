import streamlit as st
import pandas as pd
import numpy as np
import geopy
from geopy.geocoders import Nominatim

df = pd.DataFrame(
    np.array(45.4688535,9.2776371),
    columns=['lat', 'lon'])

st.map(df)