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
    #hashed_passwords = stauth.Hasher(['test']).generate()
    # Loading config file
    with open(path+'config.yaml') as file:
        config_str = str(yaml.load(file, Loader=SafeLoader))
    import ast
    config=ast.literal_eval(config_str)


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
                    # Saving config file
                with open(path+'config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                import base64
                from github import Github
                from github import InputGitTreeElement

                import yaml
                from yaml.loader import SafeLoader
                from github import Github
                # Replace <ACCESS_TOKEN> with your personal access token
                ACCESS_TOKEN = st.secrets["git"]["git_pwd"].replace("'","")
                st.write(st.secrets["git"]["git_pwd"].replace("'",""))
                # Replace <REPO_NAME> with the name of the repository where you want to push the file
                REPO_NAME = 'fog97/Comics_Map'
                # Replace <FILE_NAME> with the name of the file you want to push
                FILE_NAME = 'config.yaml'
                # Replace <FILE_CONTENT> with the contents of the file you want to push
                with open(path+'config.yaml') as file:
                    config = yaml.load(file, Loader=SafeLoader)
                FILE_CONTENT = str(config)
                # Create a PyGithub instance using your access token
                g = Github(ACCESS_TOKEN)
                # Get the repository where you want to push the file
                repo = g.get_repo(REPO_NAME)
                file = repo.get_contents(FILE_NAME)
                repo.update_file(FILE_NAME, "update_configs",FILE_CONTENT, file.sha)
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
                        with open(path+'config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        import base64
                        from github import Github
                        from github import InputGitTreeElement

                        import yaml
                        from yaml.loader import SafeLoader
                        from github import Github
                        # Replace <ACCESS_TOKEN> with your personal access token
                        ACCESS_TOKEN = st.secrets["git"]["git_pwd"].replace("'","")
                        st.write(st.secrets["git"]["git_pwd"].replace("'",""))
                        # Replace <REPO_NAME> with the name of the repository where you want to push the file
                        REPO_NAME = 'fog97/Comics_Map'
                        # Replace <FILE_NAME> with the name of the file you want to push
                        FILE_NAME = 'config.yaml'
                        # Replace <FILE_CONTENT> with the contents of the file you want to push
                        with open(path+'config.yaml') as file:
                            config = yaml.load(file, Loader=SafeLoader)
                        FILE_CONTENT = str(config)
                        # Create a PyGithub instance using your access token
                        g = Github(ACCESS_TOKEN)
                        # Get the repository where you want to push the file
                        repo = g.get_repo(REPO_NAME)
                        file = repo.get_contents(FILE_NAME)
                        repo.update_file(FILE_NAME, "update_configs",FILE_CONTENT, file.sha)

                    except Exception as e:
                        st.error(e)
        with col2:
            with st.expander("Update Details", expanded=False):
                # Creating an update user details widget
                if authentication_status:
                    try:
                        if authenticator.update_user_details(username, 'Update user details'):
                            st.success('Entries updated successfully')
                        with open(path+'config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        import base64
                        from github import Github
                        from github import InputGitTreeElement

                        import yaml
                        from yaml.loader import SafeLoader
                        from github import Github
                        # Replace <ACCESS_TOKEN> with your personal access token
                        ACCESS_TOKEN = st.secrets["git"]["git_pwd"].replace("'","")
                        st.write(st.secrets["git"]["git_pwd"].replace("'",""))
                        # Replace <REPO_NAME> with the name of the repository where you want to push the file
                        REPO_NAME = 'fog97/Comics_Map'
                        # Replace <FILE_NAME> with the name of the file you want to push
                        FILE_NAME = 'config.yaml'
                        # Replace <FILE_CONTENT> with the contents of the file you want to push
                        with open(path+'config.yaml') as file:
                            config = yaml.load(file, Loader=SafeLoader)
                        FILE_CONTENT = str(config)
                        # Create a PyGithub instance using your access token
                        g = Github(ACCESS_TOKEN)
                        # Get the repository where you want to push the file
                        repo = g.get_repo(REPO_NAME)
                        file = repo.get_contents(FILE_NAME)
                        repo.update_file(FILE_NAME, "update_configs",FILE_CONTENT, file.sha)

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
                        with open(path+'config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        import base64
                        from github import Github
                        from github import InputGitTreeElement

                        import yaml
                        from yaml.loader import SafeLoader
                        from github import Github
                        # Replace <ACCESS_TOKEN> with your personal access token
                        ACCESS_TOKEN = st.secrets["git"]["git_pwd"].replace("'","")
                        st.write(st.secrets["git"]["git_pwd"].replace("'",""))
                        # Replace <REPO_NAME> with the name of the repository where you want to push the file
                        REPO_NAME = 'fog97/Comics_Map'
                        # Replace <FILE_NAME> with the name of the file you want to push
                        FILE_NAME = 'config.yaml'
                        # Replace <FILE_CONTENT> with the contents of the file you want to push
                        with open(path+'config.yaml') as file:
                            config = yaml.load(file, Loader=SafeLoader)
                        FILE_CONTENT = str(config)
                        # Create a PyGithub instance using your access token
                        g = Github(ACCESS_TOKEN)
                        # Get the repository where you want to push the file
                        repo = g.get_repo(REPO_NAME)
                        file = repo.get_contents(FILE_NAME)
                        repo.update_file(FILE_NAME, "update_configs",FILE_CONTENT, file.sha)

                    # add pin to sohw PWDRandom password to be transferred to user securely
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
                        with open(path+'config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        import base64
                        from github import Github
                        from github import InputGitTreeElement

                        import yaml
                        from yaml.loader import SafeLoader
                        from github import Github
                        # Replace <ACCESS_TOKEN> with your personal access token
                        ACCESS_TOKEN = st.secrets["git"]["git_pwd"].replace("'","")
                        st.write(st.secrets["git"]["git_pwd"].replace("'",""))
                        # Replace <REPO_NAME> with the name of the repository where you want to push the file
                        REPO_NAME = 'fog97/Comics_Map'
                        # Replace <FILE_NAME> with the name of the file you want to push
                        FILE_NAME = 'config.yaml'
                        # Replace <FILE_CONTENT> with the contents of the file you want to push
                        with open(path+'config.yaml') as file:
                            config = yaml.load(file, Loader=SafeLoader)
                        FILE_CONTENT = str(config)
                        # Create a PyGithub instance using your access token
                        g = Github(ACCESS_TOKEN)
                        # Get the repository where you want to push the file
                        repo = g.get_repo(REPO_NAME)
                        file = repo.get_contents(FILE_NAME)
                        repo.update_file(FILE_NAME, "update_configs",FILE_CONTENT, file.sha)
                        #add pin to show new USRNM
                    else:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)








        
        
        
        

st.header(" _Come Together_ ")

st.image(image.imread(path+'Copertina2.jpg'))




