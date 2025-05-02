# Set page config 
import streamlit as st
st.set_page_config(page_title="Login", page_icon="🔐")

# Authentication Check
# Auntentication check
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Login to Access the App")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "Cmainga" and password == "password123":
            st.session_state.authenticated = True
            st.success("✅ Login Successful! Redirecting...")
            st.rerun()  # Refresh the app to reload the authenticated state 
        else:
            st.error("❌ Invalid Username or Password")

    st.stop()  # Prevent further execution

st.switch_page("pages/1_overview.py")