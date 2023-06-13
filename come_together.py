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
import io
from pydub import AudioSegment
import smtplib
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
path='/app/comics_map/'
sender=st.secrets["mail"]["mail"]
pwd=st.secrets["mail"]["mail_pwd"]
#Test_345
gmail_user = sender
gmail_pwd = pwd
st.session_state.autenticazione=False
st.set_page_config(
    page_title="Come Together",
    layout="centered",
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


col1, col2, col3 = st.columns((1,10,1))


with col1:
    st.write(' ')

with col2:
    
    st.image(image.imread(path+'Copertina2.jpg'))
    original_title = '<p style="font-family:fantasy; color:Red; font-size: 80px;">Come Together</p>'
    st.markdown(original_title, unsafe_allow_html=True)

with col3:
    st.write(' ')


# @st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return MongoClient(f"mongodb+srv://{us_name}:{us_pw}@{cl_name}.zisso.mongodb.net/test")
client = init_connection()
db = client.PresenzeComics
collection = db.Credentials
config =collection.find_one()
collection_secs = db.Security

filter = { '_id': config["_id"] }


_RELEASE = False

if not _RELEASE:
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
                collection.replace_one(filter, config)  
        except Exception as e:
            st.error(e)

    # creating a login widget
    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status:
        st.session_state.utente=username
        
        collection_friends = db.Friends
        filter_friends = { 'user': st.session_state.utente }
        try:
            security =pd.DataFrame(list(collection_secs.find(filter_friends)))
            if len(security)==0:
                pin=st.text_input("Primo accesso, inserisci un PIN di 4 cifre. Serve per cambiare password, ricordalo !")
                if pin!="":
                    sec_data={'user': username, 'pin': pin}
                    collection_secs.insert_one(sec_data)
        except:
            pass
        try:
            friends =collection_friends.find(filter_friends)
            fr=pd.DataFrame(list(friends))
            list_friend=fr.loc[0,"friend"].split(";")
        except:
            first_data={'user': st.session_state.utente, 'friend': ''}
            collection_friends.insert_one(first_data)
            friends =collection_friends.find(filter_friends)
            fr=pd.DataFrame(list(friends))
            list_friend=fr.loc[0,"friend"].split(";")

        st.session_state.autenticazione=True
        authenticator.logout('Logout', 'main')
        st.write(f'Benvenuto **{name}** :smiley:')
        st.header('Log In / Sign In')
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Change Password", expanded=False):
                    # Creating a password reset widget
                if authentication_status:
                    #st.session_state.authentication_status=authentication_status
                    try:
                        if authenticator.reset_password(username, 'Reset password'):
                            st.success('Password modified successfully')
                            collection.replace_one(filter, config)
                    except Exception as e:
                        st.error(e)
        with col2:
            with st.expander("Update Details", expanded=False):
                # Creating an update user details widget
                if authentication_status:
                    try:
                        if authenticator.update_user_details(username, 'Update user details'):
                            st.success('Entries updated successfully')
                            collection.replace_one(filter, config)
                    except Exception as e:
                        st.error(e)
        with st.container():
            st.header('Gestione Amici')
            friend = st.text_input("Username amico",key='1AB') 
            col1,col2=st.columns(2) 
            with col1:
                add=st.button('Aggiungi Amico')
                if add:
                    mydict = { "user": st.session_state.utente, "friend": fr.loc[0,"friend"]+";"+friend }
                    collection_friends.replace_one(filter_friends, mydict)
            with col2:
                dell=st.button('Elimina Amico')
                if dell:
                    stringa_amici=''
                    for amico in list_friend :
                        if amico!=friend and  amico!="":
                            stringa_amici=stringa_amici+";"+amico
                    mydict = { "user": st.session_state.utente, "friend": stringa_amici}
                    collection_friends.replace_one(filter_friends, mydict)
            

    elif authentication_status is False:
        st.session_state.autenticazione=False
        st.error('Username/password is incorrect')
    if not authentication_status:
        st.session_state.autenticazione=False
        col1,col2=st.columns(2)
        with col1:
            with st.expander("Password dimenticata?", expanded=False):
                user=st.text_input("Inserisci il tuo Username")
                filter_sec = { 'user': user}
                try:
                    security =pd.DataFrame(list(collection_secs.find(filter_sec)))
                    pin=st.text_input("Inserisci il tuo PIN")
                    if pin==security.loc[0,"pin"]:
                        st.write("pass")

                    # Creating a forgot password widget
                    try:
                        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                        if username_forgot_pw:

                            TO = email_forgot_password
                            SUBJECT = "Nuova Password"
                            TEXT = "La nuova password :"+str(random_password)+" . Assicurati di cambiarla appena possibile."
                            server = smtplib.SMTP('smtp.gmail.com')
                            server.ehlo()
                            server.starttls()
                            server.login(gmail_user, gmail_pwd)
                            BODY = '\r\n'.join(['To: %s' % TO,
                                     'From: %s' % gmail_user,
                                     'Subject: %s' % SUBJECT,
                                     '', str(TEXT)])
                            server.sendmail(gmail_user, [TO], BODY)
                            server.quit()

                            st.success('New password sent securely')
                            collection.replace_one(filter, config)
                        else:
                            st.error('Username not found')
                    except Exception as e:
                        st.error(e)
                except:
                    pass
        with col2:
            with st.expander("Username Dimenticato?", expanded=False):
                # Creating a forgot username widget
                try:
                    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                    if username_forgot_username:
                        TO = email_forgot_username
                        SUBJECT = "Username"
                        TEXT = f"Username : {username_forgot_username}"
                        server = smtplib.SMTP('smtp.gmail.com')
                        server.ehlo()
                        server.starttls()
                        server.login(gmail_user, gmail_pwd)
                        BODY = '\r\n'.join(['To: %s' % TO,
                                 'From: %s' % gmail_user,
                                 'Subject: %s' % SUBJECT,
                                 '', str(TEXT)])
                        server.sendmail(gmail_user, [TO], BODY)
                        server.quit()

                        st.success('Username sent securely')
                        collection.replace_one(filter, config)
                    else:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)










       

st.write("Area di test Ignora") 
        
        
        



from audiorecorder import audiorecorder

st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.tobytes())
    s = io.BytesIO(audio.tobytes())
    audiotr = AudioSegment.from_raw(s).export("sound.wav", format='wav')
    r = sr.Recognizer()
    with sr.AudioFile("sound.wav") as source:
        try:
            text = r.recognize_google(audio_text)
            st.write('Converting audio transcripts into text ...')
            st.write(text)
        except:
            st.write('Sorry.. run again...')
