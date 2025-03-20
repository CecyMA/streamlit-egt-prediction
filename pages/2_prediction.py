import streamlit as st
# Page configuration
st.set_page_config(page_title="Make Predictions", layout="wide", page_icon="🎯")

import pandas as pd
import shap
from Utils.func import min_max_scaling, inverse_min_max_scaling
from Utils.data import predict_egt
from Utils.send_email import send_email_alert


# Check authentication and redirect if not logged in
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.switch_page("main.py")  # Redirect to login

# Main Content for Predictions Page
st.title("🎯 Predictions")
st.write("Make predictions using the EGT Hot Day Margin model")

prediction_type = st.radio("Select Prediction Type:", ["File Upload", "Manual Input"])
threshold_min = st.number_input("Enter Minimum Threshold for EGT Hot Day Margin", value=10)
threshold_max = st.number_input("Enter Maximum Threshold for EGT Hot Day Margin", value=55)
engine_id = st.text_input("Enter Engine Serial Number")

input_features = ['Mach', 'Fuel Flow', 'Vibration N1 #1 Bearing',
                  'Vibration N2 #1 Bearing', 'Oil Temperature', 'EGT',
                  'Total Air Temperature', 'Oil Pressure', 'Oil Pressure Smoothed',
                  'Altitude', 'Indicated Fan Speed', 'Thrust Derate',
                  'Thrust Derate Smoothed', 'Core Speed', 'Oil Temperature Smoothed',
                  'DAYS_SINCE_INSTALL']

if prediction_type == "File Upload":
    uploaded_file = st.file_uploader("📂 Upload CSV/XLSX File", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
        st.write("✅ File Uploaded Successfully!")
        
        if "ESN" in df.columns:
            esn_data = df["ESN"]
            df = df.drop(columns=["ESN"])
        else:
            esn_data = ["Unknown"] * len(df)
        
        st.write(df.head())
        
        if "EGT Hot Day Margin" in df.columns:
            df["Alert"] = df["EGT Hot Day Margin"].apply(lambda x: "⚠️ Alert!" if x < threshold_min or x > threshold_max else "✅ Safe")
        else:
            scaled_data = min_max_scaling(df[input_features])
            predictions = predict_egt(scaled_data)
            df["EGT Hot Day Margin"] = inverse_min_max_scaling(predictions)
            df["Alert"] = df["EGT Hot Day Margin"].apply(lambda x: "⚠️ Alert!" if x < threshold_min or x > threshold_max else "✅ Safe")
            
            # Compute SHAP values
            explainer = st.session_state.get("explainer", None)
            if explainer:
                shap_values_dl = explainer.shap_values(scaled_data)
                st.session_state["X_test"] = df[input_features]
                st.session_state["shap_values_dl"] = shap_values_dl
                st.session_state["base_value_dl"] = explainer.expected_value.numpy().item()
        
        st.write("🔹 Predicted EGT Hot Day Margin & Alerts:")
        st.write(df[['EGT Hot Day Margin', 'Alert']])
        
        if (df["EGT Hot Day Margin"] < threshold_min).any() or (df["EGT Hot Day Margin"] > threshold_max).any():
            st.write("⚠️ Alert: Predictions exceed safe limits!")
            recipient_email = st.text_input("Enter recipient email for alerts", "")
            if recipient_email and st.button("📧 Send Email Alert"):
                for i, row in df.iterrows():
                    if row["EGT Hot Day Margin"] < threshold_min or row["EGT Hot Day Margin"] > threshold_max:
                        email_sent = send_email_alert(engine_id, row["EGT Hot Day Margin"], threshold_min, threshold_max, recipient_email)
                        if email_sent:
                            st.success("✅ Email sent!")
                        else:
                            st.error("❌ Failed to send email.")

else:
    if "prediction" not in st.session_state:
        st.session_state.prediction = None
    if "recipient_email" not in st.session_state:
        st.session_state.recipient_email = ""
    
    # Prediction Form
    with st.form("prediction_form", clear_on_submit=False):
        input_data = {}

        with st.container():
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                input_data["Mach"] = st.number_input("Mach", value=None, step=0.01, format="%.2f")
                input_data["Oil Temperature"] = st.number_input("Oil Temperature", value=None, step=0.01, format="%.2f")
                input_data["Oil Pressure Smoothed"] = st.number_input("Oil Pressure Smoothed", value=None, step=0.01, format="%.2f")
                input_data["Altitude"] = st.number_input("Altitude", value=None, step=1, format="%d")

            with col2:
                input_data["Fuel Flow"] = st.number_input("Fuel Flow", value=None, step=0.01, format="%.2f")
                input_data["Total Air Temperature"] = st.number_input("Total Air Temperature", value=None, step=0.01, format="%.2f")
                input_data["Core Speed"] = st.number_input("Core Speed", value=None, step=0.01, format="%.2f")
                input_data["Oil Temperature Smoothed"] = st.number_input("Oil Temperature Smoothed", value=None, step=0.01, format="%.2f")

            with col3:
                input_data["Vibration N1 #1 Bearing"] = st.number_input("Vibration N1 #1 Bearing", value=None, step=0.01, format="%.2f")
                input_data["Vibration N2 #1 Bearing"] = st.number_input("Vibration N2 #1 Bearing", value=None, step=0.01, format="%.2f")
                input_data["EGT"] = st.number_input("EGT", value=None, step=0.01, format="%.2f")
                input_data["Oil Pressure"] = st.number_input("Oil Pressure", value=None, step=0.01, format="%.2f")

            with col4:
                input_data["Indicated Fan Speed"] = st.number_input("Indicated Fan Speed", value=None, step=0.01, format="%.2f")
                input_data["Thrust Derate"] = st.number_input("Thrust Derate", value=None, step=0.01, format="%.2f")
                input_data["Thrust Derate Smoothed"] = st.number_input("Thrust Derate Smoothed", value=None, step=0.01, format="%.2f")
                input_data["DAYS_SINCE_INSTALL"] = st.number_input("DAYS_SINCE_INSTALL", value=None, step=1, format="%d")

        submitted = st.form_submit_button("Predict")

    # Handle prediction outside form
    if submitted:
        input_df = pd.DataFrame([input_data])
        st.write("📝 Input Data:")
        st.write(input_df)

        st.session_state.input_data = input_data


        scaled_data = min_max_scaling(input_df)
        st.session_state.prediction = inverse_min_max_scaling(predict_egt(scaled_data))

    # Display Prediction
    if st.session_state.prediction is not None:
        prediction_value = float(st.session_state.prediction[0])
        st.write(f'🎯 EGT Hot Day Margin prediction: {prediction_value:.2f}°C')

        # Store alert status in session state
        st.session_state.alert_needed = prediction_value < threshold_min or prediction_value > threshold_max

        if st.session_state.alert_needed:
            st.write("⚠️ Alert: Prediction exceeds safe limits!")

            # Preserve Email Input in Session State
            st.session_state.recipient_email = st.text_input("Enter recipient email for alerts", value=st.session_state.recipient_email)

            # Email Alert Form (Separate)
            with st.form("email_alert_form"):
                send_email = st.form_submit_button("📧 Send Email Alert")

                if send_email and st.session_state.recipient_email:
                    email_sent = send_email_alert(engine_id, prediction_value, threshold_min, threshold_max, st.session_state.recipient_email)
                    if email_sent:
                        st.success("✅ Email sent!")
                    else:
                        st.error("❌ Failed to send email.")
        else:
            st.write("✅ Prediction is within safe limits. No alert needed.")

