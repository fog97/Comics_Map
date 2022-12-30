import streamlit as st
import pandas as pd
import numpy as np

location = {'lat': 45.4688535, 'lon': 9.2776371 }
df = pd.DataFrame(data=location,index=[1])

st.map(df)