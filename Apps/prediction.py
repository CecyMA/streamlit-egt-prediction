import streamlit as st
import pandas as pd
from Utils.func import min_max_scaling, inverse_min_max_scaling
from Utils.data import predict_egt
from Utils.send_email import send_email_alert

st.header("✈️ EGT Hot Day Margin Predictions")

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
            st.write("🔹 Scaled Input data")
            st.write(scaled_data)

            predictions = predict_egt(scaled_data)
            df["EGT Hot Day Margin"] = inverse_min_max_scaling(predictions)
            df["Alert"] = df["EGT Hot Day Margin"].apply(lambda x: "⚠️ Alert!" if x < threshold_min or x > threshold_max else "✅ Safe")

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
                            st.success(f"✅ Email sent!")
                        else:
                            st.error(f"❌ Failed to send email.")

else:
    # Ensure session state stores user inputs, prediction, and recipient email
    if "manual_input_data" not in st.session_state:
        st.session_state.manual_input_data = None
    if "scaled_prediction" not in st.session_state:
        st.session_state.scaled_prediction = None
    if "recipient_email" not in st.session_state:
        st.session_state.recipient_email = ""

    # Define input form
    with st.form(key='manual_input_form'):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            mach = st.number_input("Mach", value=0.00)
        with col2:
            fuel_flow = st.number_input("Fuel Flow", value=0.00)
        with col3:
            vib_n1 = st.number_input("Vibration N1 #1 Bearing", value=0.00)
        with col4:
            vib_n2 = st.number_input("Vibration N2 #1 Bearing", value=0.00)

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            oil_temp = st.number_input("Oil Temperature", value=0.00)
        with col6:
            egt = st.number_input("EGT", value=0.00)
        with col7:
            total_air_temp = st.number_input("Total Air Temperature", value=0.00)
        with col8:
            oil_pressure = st.number_input("Oil Pressure", value=0.00)

        col9, col10, col11, col12 = st.columns(4)
        with col9:
            oil_pressure_smooth = st.number_input("Oil Pressure Smoothed", value=0.00)
        with col10:
            altitude = st.number_input("Altitude", value=0)
        with col11:
            fan_speed = st.number_input("Indicated Fan Speed", value=0.00)
        with col12:
            thrust_derate = st.number_input("Thrust Derate", value=0.00)

        col13, col14, col15, col16 = st.columns(4)
        with col13:
            thrust_derate_smooth = st.number_input("Thrust Derate Smoothed", value=0.00)
        with col14:
            core_speed = st.number_input("Core Speed", value=0.00)
        with col15:
            oil_temp_smooth = st.number_input("Oil Temperature Smoothed", value=0.00)
        with col16:
            days_since_install = st.number_input("Days Since Install", value=0)

        submitted = st.form_submit_button(label='Predict')

    # Handle predictions when form is submitted
    if submitted:
        st.session_state.manual_input_data = pd.DataFrame([[
            mach, fuel_flow, vib_n1, vib_n2, oil_temp, egt, total_air_temp, oil_pressure,
            oil_pressure_smooth, altitude, fan_speed, thrust_derate, thrust_derate_smooth,
            core_speed, oil_temp_smooth, days_since_install
        ]], columns=input_features)

        st.write("📝 Input Data:")
        st.write(st.session_state.manual_input_data)

        scaled_data = min_max_scaling(st.session_state.manual_input_data)

        #st.write("🔹 Scaled Input data")
        #st.write(scaled_data)

        st.session_state.scaled_prediction = predict_egt(scaled_data)
        Prediction = inverse_min_max_scaling(st.session_state.scaled_prediction)

        st.write(f'🎯 EGT Hot Day Margin prediction: {Prediction[0].item():.2f}°C')

    # Check if a prediction exists and evaluate thresholds
    if st.session_state.scaled_prediction is not None:
        Prediction = inverse_min_max_scaling(st.session_state.scaled_prediction)
        
        if Prediction[0] < threshold_min or Prediction[0] > threshold_max:
            st.write("⚠️ Alert: EGT prediction exceeds safe limits!")

            # Persist recipient email in session state
            st.session_state.recipient_email = st.text_input(
                "Enter recipient email for alerts",
                value=st.session_state.recipient_email
            )

            if st.session_state.recipient_email and st.button("📧 Send Email Alert"):
                email_sent = send_email_alert(engine_id, Prediction[0].item(), threshold_min, threshold_max, st.session_state.recipient_email)

                if email_sent:
                    st.success("✅ Email sent!")
                else:
                    st.error("❌ Failed to send email")
        else:
            st.write("✅ Prediction is within safe limits. No alert needed.")




