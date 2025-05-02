import streamlit as st
# Page configuration
st.set_page_config(page_title="Model Interpretation", layout="wide", page_icon="🧠")

import shap
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.losses import MeanSquaredError
from Utils.func import min_max_scaling, inverse_min_max_scaling

# Load the training data
@st.cache_resource
def load_training_data():
    return pd.read_csv("X_train.csv")

X_train = load_training_data()

# Load the deep learning model
@st.cache_resource
def load_model():
    """Loads and caches the deep learning model."""
    custom_objects = {"mse": MeanSquaredError()}
    model_path = "model_deep.h5"
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

# Ensure input data and prediction exist
if "input_data" not in st.session_state or "prediction" not in st.session_state:
    st.warning("No prediction data found. Please make predictions first.")
else:
    prediction_value = float(st.session_state.prediction[0])  # Prediction from the model
    st.write(f"EGT Hot Day Margin Prediction: {prediction_value:.2f}°C")

    # Convert input data into DataFrame
    input_df = st.session_state.input_data

    # Display input data
    st.write("📝 Input Data Used for Prediction:")
    st.dataframe(input_df)

input_df_scaled = min_max_scaling(input_df)
# Load the model
model_deep = load_model()

# SHAP setup
X_train_array = X_train.to_numpy()
X_test_array = input_df_scaled.to_numpy()

# Initialize SHAP Deep Explainer
explainer = shap.DeepExplainer(model_deep, X_train_array)

#SHAP values
shap_values_dl = explainer.shap_values(X_test_array)
shap_values_dl = shap_values_dl[0].flatten() # Select relevant SHAP values


# TensorFlow tensor to a float
base_value_dl = explainer.expected_value.numpy().item()
# Unscale the base value (f(x)) for the SHAP plot
#unscaled_base_value_dl = inverse_min_max_scaling(base_value_dl)

# SHAP Explanation object
explanation = shap.Explanation(
        values=shap_values_dl,  
        base_values= base_value_dl,
        data=input_df.iloc[0],  
        feature_names=input_df.columns  
    )



# SHAP Waterfall Plot
st.subheader("SHAP Waterfall Plot for Feature Contributions")
fig, ax = plt.subplots(figsize=(8, 6))
shap.plots.waterfall(explanation)
plt.title("SHAP Waterfall Plot for Model Explanation")
st.pyplot(fig)

# Sidebar Logout Button
if st.sidebar.button("🔒 Log Out"):
    st.session_state.clear()  # Clears all session data (logs out the user)
    st.success("Logged out successfully! Redirecting to login page...")
    st.rerun()  # Refresh the page
