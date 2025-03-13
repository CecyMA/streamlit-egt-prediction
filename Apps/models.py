import streamlit as st

#st.set_page_config(page_title="EGT Hot Day Margin Prediction - Overview", page_icon="✈️")

st.title("📊 EGT Hot Day Margin Prediction App Overview")
st.write("This application helps aviation professionals monitor and predict Exhaust Gas Temperature (EGT) Hot Day Margin to ensure engine health and detect potential performance issues.")

st.header("📌 How It Works")
st.subheader("1️⃣ Choose Your Input Method")
st.write("📂 File Upload – Upload a CSV/XLSX file containing engine parameters.")
st.write("📝 Manual Input – Enter individual engine parameters for a single prediction.")

st.subheader("2️⃣ Set Safety Thresholds")
st.write("Before making a prediction, define the acceptable EGT Hot Day Margin range:")
st.write("Minimum Threshold - default: 10°C")
st.write("Maximum Threshold - default: 55°C")
st.write("If the predicted EGT margin falls outside this range, the app will generate an email alert.")

st.subheader("3️⃣ Upload or Enter Data")
st.markdown("📂 File Upload Mode")
st.write("1. Upload a CSV or Excel file containing engine data.")
st.write("2. The app will preprocess the data and display the first few rows.")
st.write("3. If EGT Hot Day Margin is not already in the file, the app predicts it.")
st.write("4. Alerts are generated for any values outside the safe range.")
st.write("5. Users can send email alerts for engines exceeding safe limits.")

st.markdown("📝 Manual Input Mode")
st.write("1. Enter engine parameters such as Mach, Fuel Flow, Vibration, Oil Temperature, EGT, and Altitude etc.")
st.write("2. Submit the form to get an EGT Hot Day Margin prediction")
st.write("3. If the prediction is outside safe limits, users can send an email alert.")

st.subheader("4️⃣ Predictions and Alerts")
st.write(" The app highlights ✅safe and ⚠️critical predictions")
st.write("Email alerts can be sent to notify maintenance teams of critical predictions.")

st.header("📧 Email Alerts")
st.write("If the EGT Hot Day Margin predictions exceed the defined safety thresholds, users can send an email alert by:")
st.write("1. Entering the Engine Serial Number (ESN).")
st.write("2. Providing a recipient email.")
st.write("3. Clicking the *📧 Send Email Alert* button.")

st.success("This tool is designed to assist maintenance teams, engineers, and operators in monitoring engine performance efficiently and proactively.")
    

