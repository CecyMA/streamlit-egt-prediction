import streamlit as st

# Page configuration
st.set_page_config(page_title="Model Interpretation", layout="wide", page_icon="🧠")

import shap
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.losses import MeanSquaredError


# Load X_train for SHAP explanations
@st.cache_resource
def load_training_data():
    return pd.read_csv("X_train.csv")

X_train = load_training_data()

# Load the model
@st.cache_resource
def load_model():
    """Loads and caches the deep learning model."""
    custom_objects = {"mse": MeanSquaredError()}
    model_path = "model_deep.h5"  
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

# Ensure predictions exist
if "input_data" not in st.session_state or "prediction" not in st.session_state:
    st.warning("No prediction data found. Please make predictions first.")
else:
    prediction_value = float(st.session_state.prediction[0])
    st.write(f"🎯 **EGT Hot Day Margin Prediction:** {prediction_value:.2f}°C")

    # Convert input_data into a DataFrame
    input_df = st.session_state.input_data

    # Display input data
    st.write("📝 **Input Data Used for Prediction:**")
    st.dataframe(input_df)

    # Ensure X_train is in NumPy format for SHAP
    X_train_array = X_train.to_numpy()

    # Load the model before using it
    model_deep = load_model()

    # Initialize SHAP Deep Explainer
    explainer = shap.DeepExplainer(model_deep, X_train_array)

    # Convert input data into numpy format
    X_test_array = input_df.to_numpy()

    # Compute SHAP values
    shap_values_dl = explainer.shap_values(X_test_array)
    shap_values_dl = shap_values_dl[:, :, 0]  # Select relevant SHAP values

    # Convert TensorFlow tensor to a float
    base_value_dl = explainer.expected_value.numpy().item()

    # Create SHAP Explanation object
    explanation = shap.Explanation(
        values=shap_values_dl[0],  
        base_values=base_value_dl,  
        data=input_df.iloc[0],  
        feature_names=input_df.columns  
    )

    # Generate SHAP Waterfall Plot
    st.subheader("🔍 **SHAP Waterfall Plot for Feature Contributions**")
    fig, ax = plt.subplots(figsize=(8, 6))
    shap.plots.waterfall(explanation, show=False)
    plt.title("SHAP Waterfall Plot for Model Explanation")
    st.pyplot(fig)



# Sidebar Logout Button
if st.sidebar.button("🔒 Log Out"):
    st.session_state.clear()  # Clears all session data (logs out the user)
    st.success("Logged out successfully! Redirecting to login page...")
    st.experimental_rerun()  # Refresh the page
