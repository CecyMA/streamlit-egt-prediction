import streamlit as st

# page set up
st.set_page_config(page_title='EGT Hot Day Margin Prediction', layout='wide', page_icon=":material/flight_takeoff:")

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


# Authentication Setup
USER_CREDENTIALS = {"admin": "password", "user": "password"}  #Can be replaced

# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login Form that blocks access until login
if not st.session_state.authenticated:
    st.subheader("🔐 Login to Access the App")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.success("✅ Login Successful! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password")
    
    st.stop()  # 🚫 Stops execution until logged in

# Logout Button
if st.sidebar.button("🔒 Logout"):
    st.session_state.authenticated = False
    st.rerun()

# Define navigation after set_page_config()
model_page       = st.Page("Apps/models.py",     title='Models Info', icon='📊')
prediction_page  = st.Page("Apps/prediction.py", title='Make Predictions', icon='🎯')
#inter_Page       = st.Page("Apps/Intrepreat.py", title='Explainable AI', icon='🧠')

pg = st.navigation(
    {
        "Navigation Bar": [model_page, prediction_page]
    }
)

pg.run()


