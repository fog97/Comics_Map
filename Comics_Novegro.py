import time
import base64

import streamlit as st
import pandas as pd
import geopandas as gpd

import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import plotly_express as px

def main():
    file = st.file_uploader("Choose a file")
    if file is not None:
        file.seek(0)
        df = pd.read_csv(file, low_memory=False)
        with st.spinner("Reading CSV File..."):
            time.sleep(5)
            st.success("Done!")
        st.write(df.head())
        st.write(df.shape)

        cols = df.columns.tolist()

        st.subheader("Choose Address Columns from the Sidebar")
        st.info("Example correct address: Karlaplan 13,115 20,STOCKHOLM, Sweden")

        if st.checkbox("Address Formatted correctly (Example Above)"):
            df_address = choose_geocode_column(df)
            st.write(df_address["geocode_col"].head())
            geocoded_df = geocode(df_address)
            display_results(geocoded_df)

        if st.checkbox("Not Correctly Formatted"):
            df_address = create_address_col(df)
            st.write(df_address["geocode_col"].head())
            geocoded_df = geocode(df_address)
            display_results(geocoded_df)


if __name__ == "__main__":
    main()