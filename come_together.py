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
import streamlit_authenticator as stauth
from PIL import Image
import yaml
path='/app/comics_map/'

st.set_page_config(
    page_title="Come Together",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit_authenticator as stauth

with open(path+'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login('Login', 'main')


st.session_state.authentication_status=authentication_status

face="🐱"

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}* {face}')
elif authentication_status is False:
    st.error('Username/password is incorrect')
    col1,col2=st.columns(2)
    with col1:
        with st.expander("Passowrd Dimenticata?"):
            try:
                username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                if username_forgot_pw:
                    st.success('New password sent securely')
                # Random password to be transferred to user securely
                else:
                    st.error('Username not found')
            except Exception as e:
                st.error(e)
    with col2:
        with st.expander("Username Dimenticatao?"): 
            try:
                username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                if username_forgot_username:
                    st.success('Username sent securely')
            # Username to be transferred to user securely
                else:
                    st.error('Email not found')
            except Exception as e:
                st.error(e)      
elif authentication_status is None:
    st.warning('Please enter your username and password')
    col1,col2=st.columns(2)
    with col1:
        with st.expander("Non hai un Accout?"):
            try:
                if authenticator.register_user('Register user', preauthorization=False):
                    st.success('User registered successfully')
            except Exception as e:
                st.error(e)
    with col2:
        with st.expander("Aggiorna Informazioni Account"):
            try:
                if authenticator.update_user_details(username, 'Update user details'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)







# st.set_page_config(
#     page_title="Come Together",
#     layout="wide",
#     initial_sidebar_state="expanded")

st.header(" _Come Together_ ")

st.image(image.imread(path+'Copertina2.jpg'))

with st.sidebar:
    st.markdown("#### Powered By _Foggy_")
st.sidebar.image(image.imread(path+'profilo.jpg'), width=300)
