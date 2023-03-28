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
email_sender=st.secrets["mail"]["mail"]
email_password=st.secrets["mail"]["mail_pwd"]

_RELEASE = False

if not _RELEASE:
    hashed_passwords = stauth.Hasher(['test']).generate()
    # Loading config file
    with open(path+'config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

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
                    except Exception as e:
                        st.error(e)
        with col2:
            with st.expander("Change Password", expanded=False):
                # Creating an update user details widget
                if authentication_status:
                    try:
                        if authenticator.update_user_details(username, 'Update user details'):
                            st.success('Entries updated successfully')
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
                        st.write(email_forgot_password)
                        email_receiver = email_forgot_password
                        subject = "PWD Come Together"
                        body = "Ciao! Ecco la tua nuova password! Cambiala al primo utilizzo!"
                        msg = f"Subject: {subject}\n{body}\n{random_password}"
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(email_sender,email_password)
                        server.sendmail(email_sender,email_receiver,msg)
                        # Random password to be transferred to user securely
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
                        st.write(email_forgot_username)
                        subject = "Username Come Together"
                        body = "Ciao! Ecco il tuo Username!"
                        msg = f"Subject: {subject}\n{body}\n{username_forgot_username}"
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(email_sender,email_password)
                        server.sendmail(email_sender,email_receiver,msg)
                    else:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)







    # Saving config file
    with open(path+'config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

    # Alternatively you may use st.session_state['name'], st.session_state['authentication_status'], 
    # and st.session_state['username'] to access the name, authentication_status, and username. 

    # if st.session_state['authentication_status']:
    #     authenticator.logout('Logout', 'main')
    #     st.write(f'Welcome *{st.session_state["name"]}*')
    #     st.title('Some content')
    # elif st.session_state['authentication_status'] is False:
    #     st.error('Username/password is incorrect')
    # elif st.session_state['authentication_status'] is None:
    #     st.warning('Please enter your username and password')
st.header(" _Come Together_ ")

st.image(image.imread(path+'Copertina2.jpg'))

with st.sidebar:
    st.markdown("#### Powered By _Foggy_")
st.sidebar.image(image.imread(path+'profilo.jpg'), width=300)



import base64
from github import Github
from github import InputGitTreeElement

import yaml
from yaml.loader import SafeLoader
from github import Github
# Replace <ACCESS_TOKEN> with your personal access token
ACCESS_TOKEN = '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'
# Replace <REPO_NAME> with the name of the repository where you want to push the file
REPO_NAME = 'Comics_Map'
# Replace <FILE_NAME> with the name of the file you want to push
FILE_NAME = 'C:\\Users\\lucaf\\OneDrive\\Desktop\\Esercizi\\Comics_Map\\config.yaml'
# Replace <FILE_CONTENT> with the contents of the file you want to push
with open('C:\\Users\\lucaf\\OneDrive\\Desktop\\Esercizi\\Comics_Map\\config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
FILE_CONTENT = config
# Create a PyGithub instance using your access token
g = Github(ACCESS_TOKEN)
# Get the repository where you want to push the file
repo = g.get_repo(REPO_NAME)
# Create a new file in the repository
new_file = repo.create_file(FILE_NAME, "Nuove Config", FILE_CONTENT)
# Print the URL of the new file
print(new_file.html_url)
