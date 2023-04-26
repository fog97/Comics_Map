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
import smtplib
path='/app/comics_map/'

st.set_page_config(
    page_title="Come Together",
    layout="wide",
    initial_sidebar_state="expanded"
)

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit.components.v1 as components

from pymongo import MongoClient

us_name=st.secrets["mongo"]["db_username"]
us_pw=st.secrets["mongo"]["db_pswd"]
cl_name=st.secrets["mongo"]["cluster_name"]


# @st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return MongoClient(f"mongodb+srv://luca:luca@cluster0.zisso.mongodb.net/test")
client = init_connection()
db = client.PresenzeComics
collection = db.Credentials
config =collection.find_one()


_RELEASE = False

if not _RELEASE:
    #hashed_passwords = stauth.Hasher(['test']).generate()
    # Loading config file
    # Creating the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'], 
        config['cookie']['key'], 
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    with st.expander("Nuovo di qui? Registrati!", expanded=False):
        # Creating a new user registration widget
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully')
                st.write(config)
                #collection.replace_one(config, config)
        except Exception as e:
            st.error(e)

    # creating a login widget
    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
        col1,col2=st.columns(2)
        with col1:
            with st.expander("Change Password", expanded=False):
                    # Creating a password reset widget
                if authentication_status:
                    try:
                        if authenticator.reset_password(username, 'Reset password'):
                            st.success('Password modified successfully')
                            collection.insert_one(config)
                    except Exception as e:
                        st.error(e)
        with col2:
            with st.expander("Update Details", expanded=False):
                # Creating an update user details widget
                if authentication_status:
                    try:
                        if authenticator.update_user_details(username, 'Update user details'):
                            st.success('Entries updated successfully')
                            collection.insert_one(config)
                    except Exception as e:
                        st.error(e)

    elif authentication_status is False:
        st.error('Username/password is incorrect')
    if not authentication_status:
        col1,col2=st.columns(2)
        with col1:
            with st.expander("Password dimenticata?", expanded=False):
                # Creating a forgot password widget
                try:
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                    if username_forgot_pw:
                        st.success('New password sent securely')
                        collection.insert_one(config)
                    else:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)
        with col2:
            with st.expander("Username Dimenticato?", expanded=False):
                # Creating a forgot username widget
                try:
                    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                    if username_forgot_username:
                        st.success('Username sent securely')
                        email_receiver = email_forgot_username
                        collection.insert_one(config)
                    else:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)








        
        
        
        

st.header(" _Come Together_ ")

st.image(image.imread(path+'Copertina2.jpg'))




